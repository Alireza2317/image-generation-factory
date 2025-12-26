# Image Generation Factory

This project automates batch image generation using large language models (LLMs) to brainstorm ideas and AI artists to create the images.

## Features

*   **Dynamic Image Generation**: Generates images based on meta-prompts using selected AI brains and artists.
*   **Configurable Workers**: Easily switch between different LLM brains (Ollama, Gemini) and image generation artists (Banana, Fooocus).
*   **Metadata Management**: Automatically saves generated image metadata to a CSV file.
*   **Server Management**: Optionally starts and stops Ollama and Fooocus services as needed.

## Setup

To get this project up and running, follow these steps:

### 1. Python Environment

This project requires Python 3.12 or newer. We recommend using `uv` for environment management.

```bash
# Create a virtual environment with Python 3.12
uv venv python=3.12

# Install project dependencies
uv sync
```

### 2. Configuration File (`.env`)

Create a `.env` file in the root of your project to configure API keys, model paths, and other settings. You can find an example in `.env.example`. Key settings include:

*   `ACTIVE_BRAIN`: Set to `ollama` or `gemini`.
*   `ACTIVE_ARTIST`: Set to `banana` or `fooocus`.
*   **Ollama**: `OLLAMA__URL`, `OLLAMA__MODEL`
*   **Fooocus**: `FOOOCUS__URL`, `FOOOCUS__CHECKPOINT`, `FOOOCUS__PATH` (the absolute path to your Fooocus installation directory)
*   **Banana**: `BANANA__API_KEY`, `BANANA__MODEL`

Example `.env`:

```env
ACTIVE_BRAIN=gemini
ACTIVE_ARTIST=banana

OLLAMA__URL="http://127.0.0.1:11434"
OLLAMA__MODEL="llama3.2"

FOOOCUS__URL="http://127.0.0.1:8888"
FOOOCUS__PATH="/path/to/your/Fooocus-API"

BANANA__API_KEY="your_banana_api_key"
BANANA__MODEL="gemini-2.5-flash-image"
```

### 3. Ollama and Fooocus (if active)

If you set `ACTIVE_BRAIN=ollama` or `ACTIVE_ARTIST=fooocus` in your `.env` file, ensure these services are either running or correctly configured for the project to start them automatically. For Fooocus, make sure `FOOOCUS__PATH` points to the root of your Fooocus installation where its `venv` and `main.py` reside.

## Usage

To run the image generation pipeline, execute the `main.py` script:

```bash
uv run main.py
```

The script will:

1.  **Brainstorm** image ideas using the `active_brain` (e.g., Ollama).
2.  **Generate images** using the `active_artist` (e.g., Fooocus) based on the brainstormed ideas and `paint` configurations from `settings.py`.
3.  **Save metadata** about the generated images to `metadata.csv`.
4.  **Save images** to the `./images` folder by default.

### Customizing Image Generation

*   **Meta-Prompts**: Define your image generation themes in text files within the `prompts/meta_prompts/` directory (e.g., `niche1.txt`). Each file acts as a meta-prompt for the LLM to generate specific image ideas.
*   **Painting Settings**: Adjust parameters like `aspect_ratio`, `image_size`, `styles`, `negative_prompt`, `guidance_scale`, `N_images`, and `performance` in the `settings.py` file under the `PaintConfig` class, or override them via environment variables in your `.env` (e.g., `PAINT__IMAGE_SIZE="1024*1024"`).
