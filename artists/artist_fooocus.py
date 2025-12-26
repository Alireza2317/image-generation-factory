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
		if not entry.get("url"):
			raise ValueError("Response did not contain `url` key!")

		url_parts: list[str] = entry["url"].split("/")
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
	real_paths: list[Path], base_image_name: str, output_dir: Path
) -> None:
	"""
	Moves images to the final destination folder and renames them.
	output_dir: The folder to put the final images
	"""

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
	def paint(
		self, prompt: str, image_name_stem: str, paint_cfg: dict[str, Any]
	) -> bool:
		base_url: str = self.config["url"].rstrip("/")
		url: str = f"{base_url}/v1/generation/text-to-image"

		seed: int = paint_cfg["seed"]
		n_images: int = paint_cfg["N_images"]
		base_model: str = self.config["checkpoint"]
		performance: str = str(paint_cfg["performance"])
		image_size: str = paint_cfg["image_size"]

		styles: list[str] = paint_cfg["styles"]

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
			"image_number": n_images,
			"refiner_model_name": "None",
			"refiner_swith": 0.5,
		}

		payload: dict[str, Any] = {
			"prompt": prompt,
			"negative_prompt": paint_cfg["negative_prompt"],
			"style_selections": styles,
			"performance_selection": performance,
			"aspect_ratios_selection": image_size,
			"image_seed": seed,
			"base_model_name": base_model,
			"loras": [
				sdxl_offset_lora,
			],
			"guidance_scale": paint_cfg["guidance_scale"],
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
			# get generated images paths from data
			real_images_paths: list[Path] = get_real_images_paths(
				data, self.config["path"]
			)

			# move and rename images to the desired location and name
			# use default dir
			output_dir: Path = paint_cfg["output_folder"]
			move_rename_images(real_images_paths, image_name_stem, output_dir)

			return True

		print(f"API Error {response.status_code}: {response.text}")
		print(f"Retrieved data: {data}")
		return False
