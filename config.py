import os
from pathlib import Path
from typing import Any
from dotenv import load_dotenv

load_dotenv()

# --- GENERAL ---
ACTIVE_BRAIN = "ollama"  # 'gemini' or 'ollama'
ACTIVE_ARTIST = "fooocus"  # 'banana' or 'fooocus'
CSV_PATH = Path(os.getenv("CSV_PATH", "./metadata.csv"))
META_PROMPTS_PATH = Path(".") / "prompts" / "meta_prompts"

# --- SPECIFIC CONFIGS ---
OLLAMA_CONFIG: dict[str, Any] = {
	"model": "llama3.2",
	"url": os.getenv("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
	+ "/api/generate",
}

FOOOCUS_CONFIG: dict[str, Any] = {
	"url": os.getenv("FOOOCUS_URL", "http://127.0.0.1:8888"),
	"fooocus_path": Path(os.getenv("FOOOCUS_API_PATH")),
	"checkpoint": "juggernautXL_v8Rundiffusion.safetensors",
}

BANANA_CONFIG: dict[str, Any] = {
	"api_key": os.getenv("GEMINI_API_KEY"),
	"gpu_type": "A100",
	"timeout": 300,
	"model": "gemini-2.5-flash-image-preview",
}

PAINT_CONFIG: dict[str, Any] = {
	"aspect_ratio": "16:9",
	"image_size": "1344*720",
	"styles": ["Fooocus V2"],
	"negative_prompt": "low quality, ugly, deformed, watermark, signiture, logo",
	"guidance_scale": 4,
	"output_dir": Path("./images"),
}
