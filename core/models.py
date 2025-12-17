from dataclasses import dataclass


@dataclass
class ImageIdea:
	"""
	A Standard container for the image idea.
	every Brain must return this object as a response.
	"""

	prompt: str
	title: str
	keywords: str  # comma-seperated keywords like "kw1,kw2,kw3"
	category: int
	filename_stem: str
