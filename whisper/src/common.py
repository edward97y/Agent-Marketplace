import os
import gc
import numpy as np
import torch
import whisper
import jiwer
import pandas as pd
from datasets import load_dataset, Audio
from transformers.models.whisper.english_normalizer import BasicTextNormalizer  # kept from earlier, independent of HF model
from tqdm.auto import tqdm

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------
LANG       = "ar_eg"          # FLEURS code; try "en_us", "fr_fr", "de_de", ...
SPLIT      = "test"
MODEL_SIZES = ["tiny", "small"]   # openai-whisper model sizes: tiny, base, small, medium, large, turbo
MAX_SAMPLES = None            # e.g. 50 for a quick smoke test, None for full split


def collect_valid_indices(ds) -> list[int]:
    valid, corrupt = [], []
    for i in tqdm(range(len(ds)), desc="Checking audio decodability"):
        try:
            _ = ds[i]["audio"]["array"]
            valid.append(i)
        except Exception as e:
            corrupt.append((i, ds[i].get("id"), str(e).splitlines()[0][:120]))
    if corrupt:
        print(f"\n{len(corrupt)} corrupt clip(s) will be skipped:")
        for idx, cid, msg in corrupt:
            print(f"   idx={idx}  id={cid}  → {msg}")
    print(f"\nUsable utterances: {len(valid)}/{len(ds)}")
    return valid

def prepare_audio(audio_array: np.ndarray, sr: int = 16_000) -> np.ndarray:
    """
    Ensure float32, mono, 16 kHz, range [-1, 1].
    FLEURS audio is already in this format, but this guard makes the
    notebook safe if you later swap datasets.
    """
    arr = np.asarray(audio_array, dtype=np.float32)
    if arr.ndim > 1:
        arr = arr.mean(axis=-1)          # downmix to mono
    if sr != 16_000:
        import librosa
        arr = librosa.resample(arr, orig_sr=sr, target_sr=16_000)
    # If values look like int16 range, normalise
    if np.abs(arr).max() > 1.5:
        arr = arr / 32768.0
    return np.clip(arr, -1.0, 1.0)

def transcribe_one(model, audio_array: np.ndarray, language: str) -> str:
    """
    audio_array : float32 NumPy array, 16 kHz, mono, [-1, 1].
    Returns raw transcription string.
    """
    audio = prepare_audio(audio_array)
    # OpenAI's transcribe accepts a NumPy array directly.
    # Explicit language avoids auto-detection overhead and wrong-language outputs.
    result = model.transcribe(
        audio,
        language=language.split("_")[0],   # "ar_eg" -> "ar"
        task="transcribe",
        fp16=False,                        # CPU: no FP16
        verbose=False,
    )
    return result["text"].strip()


from whisper.model import Whisper, ModelDimensions

def load_from_pt(size: str, device: str = "cpu") -> Whisper:
    pt = MODEL_DIR / f"whisper_{size}.pt"
    ckpt = torch.load(pt, map_location=device, weights_only=True)
    model = Whisper(ckpt["dims"])
    model.load_state_dict(ckpt["model_state_dict"])
    return model.to(device).eval()

def evaluate_model(model_size: str, language: str, ds, indices: list[int]):
    print(f"\nLoading {MODEL_DIR.name}/whisper_{model_size}.pt …")
    model = load_from_pt(model_size, DEVICE)

    hypotheses, references = [], []

    for i in tqdm(indices, desc=f"Evaluating whisper-{model_size}"):
        audio = ds[i]["audio"]["array"]
        ref   = ds[i]["transcription"]
        try:
            hyp = transcribe_one(model, audio, language)
        except Exception as e:
            print(f"\nTranscription failed at idx={i}: {e}")
            continue
        hypotheses.append(normalizer(hyp))
        references.append(normalizer(ref))

    wer_value = jiwer.wer(references, hypotheses) * 100.0
    return wer_value, hypotheses, references