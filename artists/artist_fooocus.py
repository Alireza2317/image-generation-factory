import requests
import shutil
from typing import Any
from pathlib import Path
from artists.base_artist import Artist


def get_real_images_paths(
    api_response: list[dict[str, Any]], fooocus_root_path: Path
) -> list[Path]:
    """
        Parses the API response to find where the file was saved on disk.
    Requires the root path of the Fooocus installation.
    """
    paths: list[Path] = []

    for entry in api_response:
        url_parts: list[str] = entry.get("url").split("/")
        ugly_image_name: str = url_parts[-1]
        date_directory_name: str = url_parts[-2]

        paths.append(
            fooocus_root_path
            / "outputs"
            / "files"
            / date_directory_name
            / ugly_image_name
        )

    return paths


def move_rename_images(
    real_paths: list[Path], base_image_name: str, output_dir: Path | None = None
) -> None:
    """
        Moves images to the final destination folder and renames them.
    output_dir: The folder to put the final images
    """
    if not output_dir:
        output_dir = real_paths[0].parent  # using the same directory

    # ensure path existance
    output_dir.mkdir(parents=True, exist_ok=True)

    if len(real_paths) == 1:
        new_path = output_dir / f"{base_image_name}{real_paths[0].suffix}"
        shutil.move(str(real_paths[0].resolve()), str(new_path.resolve()))
        print(f"✅ Saved to: {new_path}")
    else:
        for i, path in enumerate(real_paths, start=1):
            new_path = output_dir / f"{base_image_name}_{i}{path.suffix}"
            shutil.move(str(path.resolve()), str(new_path.resolve()))
            print(f"✅ Saved to: {new_path}")


class FooocusArtist(Artist):
    def paint(self, prompt: str, image_name: str, paint_cfg: dict[str, Any]) -> bool:
        """
        image_name: Desired filename WITHOUT extension.
        paint_cfg: Per-image settings (aspect_ratio, style, etc.)
        """
        base_url: str = self.config.get("url", "http://127.0.0.1:8888")
        url: str = base_url.rstrip("/") + "/v1/generation/text-to-image"

        seed: int = paint_cfg.get("seed", -1)
        n_images: int = 1
        base_model: str = paint_cfg.get(
            "checkpoint", "juggernautXL_v8Rundiffusion.safetensors"
        )
        performance: str = paint_cfg.get("performance", "Extreme Speed")
        ar: str = paint_cfg.get("aspect_ratio", "1344*768")

        styles = [
            "Fooocus V2",
        ]
        sdxl_offset_lora: dict[str, Any] = {
            "enabled": True,
            "model_name": "sd_xl_offset_example-lora_1.0.safetensors",
            "weight": 0.1,
        }

        basic_payload_params: dict[str, Any] = {
            "advanced_params": {"disable_preview": True},
            "require_base64": False,
            "async_process": False,
            "sharpness": 2,
            "guidance_scale": 4,
            "image_number": n_images,
            "refiner_model_name": "None",
            "refiner_swith": 0.5,
        }

        payload: dict[str, Any] = {
            "prompt": prompt,
            "negative_prompt": paint_cfg.get(
                "negative_prompt", "watermark,signiture,logo,text"
            ),
            "style_selections": styles,
            "performance_selection": performance,
            "aspect_ratios_selection": ar,
            "image_seed": seed,
            "base_model_name": base_model,
            "loras": [
                sdxl_offset_lora,
            ],
        }
        payload.update(basic_payload_params)

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()

        except requests.HTTPError as e:
            print(f"Fooocus Error: {e}")
            return False

        data = response.json()

        if response.status_code == 200 and data:
            print(f"Successful: {data}")

            # get generated images paths from data
            real_images_paths: list[Path] = get_real_images_paths(
                data, self.config.get("fooocus_path")
            )

            # move and rename images to the desired location and name
            # use default dir
            move_rename_images(real_images_paths, image_name)

            return True

        print(f"API Error {response.status_code}: {response.text}")
        print(f"Retrieved data: {data}")
        return False


if __name__ == "__main__":
    from config import FOOOCUS_CONFIG

    artist = FooocusArtist(FOOOCUS_CONFIG)
    artist.paint("water color painting of a dog", "watercolor_dog", {})
