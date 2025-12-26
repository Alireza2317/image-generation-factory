from pathlib import Path
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import StrEnum


class BrainType(StrEnum):
	OLLAMA = "ollama"
	GEMINI = "gemini"


class ArtistType(StrEnum):
	BANANA = "banana"
	FOOOCUS = "fooocus"


class FooocusConfig(BaseModel):
	url: str = "http://127.0.0.1:8888"
	checkpoint: str = "juggernautXL_v8Rundiffusion.safetensors"
	path: Path


class OllamaConfig(BaseModel):
	url: str = "http://127.0.0.1:11434"
	model: str = "llama3.2"


class BananaConfig(BaseModel):
	api_key: str
	model: str = "gemini-2.5-flash-image"
	gpu_slug: str = "a100-80gb"
	gpu_type: str = "A100"


class PaintConfig(BaseModel):
	"""Default settings for the painting jobs."""

	aspect_ratio: str = "16:9"
	image_size: str = "1344*720"
	styles: list[str] = Field(default_factory=lambda: ["Fooocus V2"])
	negative_prompt: str = "low quality, text, watermark, ugly, signiture"
	guidance_scale: int = 4
	output_folder: Path = Path("./images")


class Settings(BaseSettings):
	active_brain: BrainType = BrainType.GEMINI
	active_artist: ArtistType = ArtistType.BANANA
	csv_path: Path = Path("./metadata.csv")
	meta_prompts_path: Path = Path("./prompts/meta_prompts")

	fooocus: FooocusConfig
	banana: BananaConfig
	ollama: OllamaConfig = OllamaConfig()
	paint: PaintConfig = PaintConfig()

	model_config = SettingsConfigDict(
		env_file=".env",
		env_file_encoding="utf-8",
		env_nested_delimiter="__",
		extra="ignore",
	)


# Singleton Instance
settings = Settings()  # type: ignore
