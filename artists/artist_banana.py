from pathlib import Path
from typing import Any
from artists.base_artist import Artist
from google import genai
from google.genai.types import (
	GenerateContentResponse, GenerateContentConfig, ImageConfig
)

class BananaArtist(Artist):
    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.client = genai.Client()

    def paint(self, prompt: str, image_name: str, paint_cfg: dict[str, Any]) -> bool:
        try:
            # generate the image
            model: str = self.config.get("model", "")
            ar: str = paint_cfg.get("aspect_ratio", "1024x1024")
            image_response: GenerateContentResponse = (
                self.client.models.generate_content(
                    model=model,
                    contents=[prompt],
                    config=GenerateContentConfig(
                        image_config=ImageConfig(
                            aspect_ratio=ar,
                            # image_size='1K'
                        )
                    ),
                )
            )
        except Exception as e:
            print(f"Banana Error: {e}")
            return False

        if image_response.parts is None:
            print("Banana Error: No proper response!")
            return False

        for part in image_response.parts:
            image = part.as_image()
            if image is not None:
                output_dir: Path = paint_cfg.get("output_dir", Path("."))
                output_image_path: Path = output_dir / image_name
                image.save(str(output_image_path.resolve()))
                break
        else:
            print("Banana Error: No image was generated!")
            return False

        return True