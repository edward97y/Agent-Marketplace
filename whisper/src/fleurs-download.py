
from datasets import load_dataset

# Download Google FLEURS Arabic (Egypt)
dataset = load_dataset(
    "google/fleurs",
    "ar_eg"
)

# Save all splits locally
dataset.save_to_disk("data/fleurs_ar_eg")

print(dataset)

for split, data in dataset.items():
    print(f"{split}: {len(data)} samples")
