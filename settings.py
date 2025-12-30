from pathlib import Path
from typing import Any
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import StrEnum


class BrainType(StrEnum):
	OLLAMA = "ollama"
	GEMINI = "gemini"


class ArtistType(StrEnum):
	BANANA = "banana"
	FOOOCUS = "fooocus"


class Performance(StrEnum):
	XSPEED = "Extreme Speed"
	SPEED = "Speed"
	QUALITY = "Quality"


class PipelineType(StrEnum):
	META = "meta"
	WILDCARD = "wildcard"


class GeminiConfig(BaseModel):
	model: str = "gemini-2.5-flash"


class OllamaConfig(BaseModel):
	url: str = "http://127.0.0.1:11434"
	model: str = "llama3.2"


class BananaConfig(BaseModel):
	api_key: str
	model: str = "gemini-2.5-flash-image"
	gpu_slug: str = "a100-80gb"
	gpu_type: str = "A100"


class FooocusConfig(BaseModel):
	url: str = "http://127.0.0.1:8888"
	checkpoint: str = "juggernautXL_v8Rundiffusion.safetensors"
	path: Path


class Settings(BaseSettings):
	active_brain: BrainType = BrainType.GEMINI
	active_artist: ArtistType = ArtistType.BANANA
	active_pipeline: PipelineType = PipelineType.WILDCARD

	metadata_image_extension: str = "jpg"

	csv_path: Path = Path("./metadata")
	meta_prompts_path: Path = Path("./prompts/meta_prompts")
	wildcards_path: Path = Path("./prompts/wildcards")
	wildcard_prompts_path: Path = Path("./prompts/wildcard_prompts")
	niche_configs_path: Path = Path("./prompts/niche_configs")
	instruction_path: Path = Path("./prompts/instructions")
	log_path: Path = Path("./log")

	gemini: GeminiConfig = GeminiConfig()
	ollama: OllamaConfig = OllamaConfig()

	banana: BananaConfig
	fooocus: FooocusConfig

	model_config = SettingsConfigDict(
		env_file=".env",
		env_file_encoding="utf-8",
		env_nested_delimiter="__",
		extra="ignore",
	)

	def model_post_init(self, __context: Any) -> None:
		"""Ensuring all paths exist"""

		# all paths to check
		paths: list[Path] = [
			item for item in self.model_dump().values() if isinstance(item, Path)
		]

		for path in paths:
			path.mkdir(parents=True, exist_ok=True)


# Singleton Instance
settings = Settings()  # type: ignore
