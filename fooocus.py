import requests

BASE_MODEL = "juggernautXL_v8Rundiffusion.safetensors"
PERFORMANCE = "Extreme Speed"  # Quality, Speed, Extreme Speed
AR = "1344*768"
N = 2
STYLES = [
    "Fooocus V2",
]


def generate_image(prompt: str) -> None:
    URL = "http://127.0.0.1:8888/v1/generation/text-to-image"

    payload = {
        "prompt": prompt,
        "negative_prompt": "watermark,y signiture, logo, text",
        "style_selections": STYLES,
        "performance_selection": PERFORMANCE,
        "aspect_ratios_selection": AR,
        "image_number": N,
        "image_seed": -1,
        "sharpness": 2,
        "guidance_scale": 4,
        "base_model_name": BASE_MODEL,
        "refiner_model_name": "None",
        "refiner_swith": 0.5,
        "loras": [
            {
                "model_name": "sd_xl_offset_example-lora_1.0.safetensors",
                "weight": 0.1,
                "enabled": True,
            },
        ],
        "advanced_params": {"disable_preview": True},
        "require_base64": False,
        "async_process": False,
    }

    try:
        response = requests.post(URL, json=payload)

        data = response.json()

        if response.status_code == 200:
            if data:
                print(f"Successful: {data}")
            else:
                print("Successful request. But Image generation was failed!")
        else:
            print(f"API Error: {response.text}")

    except Exception as e:
        print(f"Fooocus Error: {e}")
