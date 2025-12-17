from typing import Any
from core.models import ImageIdea


DEFAULT_CATEGORY_NUMBER = 8  # Graphical Resources


class IdeaMapper:
	"""
	Responsible for converting raw, potentially messy jsons
	into clean, validated ImageConcept objects.

	    Raises ValueError if the data is invalid.
	"""

	@staticmethod
	def from_llm_json(raw_data: dict[str, Any]) -> ImageIdea:
		"""
		Parses JSON from an LLM. Handles missing keys, bad types,
		and formatting issues.
		"""

		# removing extra quotes and spaces
		prompt: str = raw_data.get("prompt", "").strip().strip('"')
		if not prompt:
			raise ValueError('Invalid data: missing "prompt" field.')

		title: str = raw_data.get("title", "").strip().strip('"')
		if not prompt:
			raise ValueError('Invalid data: missing "title" field.')

		raw_keywords: str | list[str] = raw_data.get("keywords", "").strip().strip('"')
		if isinstance(raw_keywords, list):
			# convert to comma-seperated str
			keywords: str = ",".join(raw_keywords)
		else:
			keywords: str = raw_keywords.strip()

		# handling category, should be int

		try:
			category: int = int(raw_data.get("category", DEFAULT_CATEGORY_NUMBER))
		except (ValueError, TypeError):
			category: int = DEFAULT_CATEGORY_NUMBER

		return ImageIdea(
			prompt=prompt,
			title=title,
			keywords=keywords,
			category=category,
		)
