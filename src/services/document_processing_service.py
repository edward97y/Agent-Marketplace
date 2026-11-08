import asyncio
import io
import json
from pathlib import Path
from fastapi import UploadFile
from pypdf import PdfReader
from pypdf.errors import PyPdfError
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .base_service import Base


class DocumentProcessingService(Base):
    """read an uploaded file -> plain text -> chunks ready to be embedded"""

    SUPPORTED_EXTENSIONS = {".txt", ".md", ".csv", ".json", ".pdf"}

    def __init__(self):
        super().__init__()
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.settings.RAG_CHUNK_SIZE,
            chunk_overlap=self.settings.RAG_CHUNK_OVERLAP,
            # try to cut on paragraphs, then lines, then sentences (english + arabic punctuation)
            separators=["\n\n", "\n", ". ", "? ", "! ", "؟ ", "، ", " ", ""],
        )

    def _read_pdf(self, data: bytes) -> str:
        reader = PdfReader(io.BytesIO(data))
        return "\n\n".join(page.extract_text() or "" for page in reader.pages)

    def _read_json(self, data: bytes) -> str:
        # pretty print so the splitter can cut on new lines
        return json.dumps(json.loads(data.decode("utf-8-sig")), ensure_ascii=False, indent=2)

    async def extract_text(self, file: UploadFile) -> str:
        filename = file.filename or ""
        if len(filename) > 255:
            raise ValueError("File name is too long (maximum 255 characters)")
        extension = Path(filename).suffix.lower()
        self.logger.info(f"start extracting text from a {extension} file")

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type '{extension}'. "
                f"Supported types: {', '.join(sorted(self.SUPPORTED_EXTENSIONS))}"
            )

        data = await file.read()

        max_bytes = self.settings.RAG_MAX_FILE_SIZE_MB * 1024 * 1024
        if len(data) > max_bytes:
            raise ValueError(f"File is larger than {self.settings.RAG_MAX_FILE_SIZE_MB} MB")

        try:
            if extension == ".pdf" :
                # pdf parsing is cpu work, run it in a thread so we don't block the event loop
                text = await asyncio.to_thread(self._read_pdf, data)
            elif extension == ".json":
                text = self._read_json(data)
            else:
                text = data.decode("utf-8-sig")
        except (UnicodeDecodeError, json.JSONDecodeError, PyPdfError) as error:
            raise ValueError(f"Could not read the file: {error}") from error

        # postgres text columns can not store NUL characters
        text = text.replace("\x00", "").strip()

        self.logger.info("finish extracting text")
        return text

    def split_text(self, text: str) -> list[str]:
        chunks = [chunk.strip() for chunk in self.splitter.split_text(text)]
        return [chunk for chunk in chunks if chunk]
