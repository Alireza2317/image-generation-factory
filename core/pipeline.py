from typing import Any
from artists.base_artist import Artist
from brains.base_brain import Brain
from core.csv_manager import AdobeCsvManager
from core.models import ImageIdea


class ProductionPipeline:
	def __init__(
		self, brain: Brain, artist: Artist, csv_manager: AdobeCsvManager
	) -> None:
		self.brain = brain
		self.artist = artist
		self.csv_manager = csv_manager

	def run_job(
		self, meta_prompt: str, image_name_stem: str, paint_config: dict[str, Any]
	) -> bool:
		"""Runs the full cycle for one single batch of images."""

		print("🧠 Brainstorming... ", end="")
		image_idea: ImageIdea | None = self.brain.get_response(meta_prompt)

		if image_idea is None:
			print("❌ LLM failed to generate idea!")
			return False

		print("✅ Idea generated.")

		print("🎨 Painting ... ", end="")
		success_paint: bool = self.artist.paint(
			image_idea.prompt, image_name_stem=image_name_stem, paint_cfg=paint_config
		)

		if not success_paint:
			print("❌ Artist failed to generate image!")
			return False

		print("✅ Image generated.")

		print("Writing Metadata ... ", end="")
		try:
			if (n := paint_config.get("N_images", 1)) == 1:
				self.csv_manager.save_record(
					image_idea, final_filename=f"{image_name_stem}.png"
				)
			else:
				for i in range(1, n + 1):
					self.csv_manager.save_record(
						image_idea, final_filename=f"{image_name_stem}_{i}.png"
					)
		except Exception as e:
			print(f"❌ Failed to write the metadata! {e}")
			return False

		print("✅ Metadata saved.")
		print("✅ Finished cycle.")
		return True
