from abc import ABC, abstractmethod

class Brain(ABC):
	@abstractmethod
	def get_response(self, meta_prompt: str) -> dict[str, str] | None:
		'''
		Takes a meta prompt, which ideally has clear instructions for
		the llm to output a json(dict) like this:
		
		{
			"prompt": str,
			"title": str,
			"keywords": str,
			"category": str
		}
		
		returns None in case of failiure
		'''
		pass

	def validate_json(self, output: dict[str, str]) -> bool:
		'''
		Checks if the output is really a valid json with desired keys.
		'''
		required_keys: tuple[str, ...] = (
			'prompt',
			'title',
			'keywords',
			'category'
		)

		return all(key in output for key in required_keys)