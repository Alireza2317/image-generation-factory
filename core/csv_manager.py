import csv
from pathlib import Path
from core.models import ImageIdea
from settings import settings


class AdobeCsvManager:
	def __init__(self, filepath: Path) -> None:
		self.filepath = filepath
		self._ensure_path()
		self._ensure_header()

	def _ensure_path(self) -> None:
		"""Creates the directory if it doesn't exist."""
		self.filepath.parent.mkdir(parents=True, exist_ok=True)

	def _ensure_header(self) -> None:
		"""Creates the file with Adobe headers if it doesn't exist."""
		if not self.filepath.exists():
			with open(self.filepath, mode="w", newline="", encoding="utf-8") as file:
				writer = csv.writer(file, delimiter=",")
				writer.writerow(
					["Filename", "Title", "Keywords", "Category", "Releases"]
				)

	def save_record(self, image_idea: ImageIdea, final_filename: str) -> None:
		"""
		Appends a single record to the csv metadata file.
		"""

		with open(self.filepath, mode="a", newline="", encoding="utf-8") as file:
			writer = csv.writer(file, delimiter=",")
			writer.writerow(
				[
					final_filename,
					image_idea.title,
					image_idea.keywords,
					image_idea.category,
					"",  # empty for releases column
				]
			)

	def save_job_metadata(
		self,
		image_idea: ImageIdea,
		image_name_stem: str,
		n_images: int,
	) -> bool:
		"""
		Saves metadata for a job, and handles multiple images names, and calls
		save_record for each.
		"""

		print("🗒️ Writing Metadata ... ", end="")
		try:
			metadata_image_ext = settings.metadata_image_extension
			if n_images == 1:
				self.save_record(
					image_idea,
					final_filename=f"{image_name_stem}.{metadata_image_ext}",
				)
			else:
				n_digits = len(str(n_images))
				print("Saved record for image number ", end="")
				for i in range(1, n_images + 1):
					self.save_record(
						image_idea,
						final_filename=f"{image_name_stem}_{i:0{n_digits}}.{metadata_image_ext}",
					)
					print(f"{i}", end=", " if i < n_images else ".\n")
			print("✅ Metadata saved.")
			return True
		except Exception as e:
			print(f"❌ Failed to write the metadata! {e}")
			return False
