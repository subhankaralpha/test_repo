import asyncio
import os
import io
import time
import yaml
import logging
from pathlib import Path

from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

_GEMINI_MAX_RETRIES = 6
_GEMINI_RETRY_INITIAL_DELAY_SEC = 2.0


def _gemini_error_is_transient(exc: BaseException) -> bool:
    msg = str(exc).lower()
    return (
        "503" in msg
        or "429" in msg
        or "unavailable" in msg
        or "resource exhausted" in msg
        or "try again" in msg
    )

_REPO_ROOT = Path(__file__).resolve().parent.parent
_OCR_PROMPT_PATH = _REPO_ROOT / "prompts" / "ocr.yaml"


def load_ocr_prompt() -> str:
    with open(_OCR_PROMPT_PATH, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)["template"]


async def get_response_from_gemini(output_stream: io.BytesIO):
    logger.info("Getting response from Gemini")
    client = None
    uploaded_file = None
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        uploaded_file = await client.aio.files.upload(file=output_stream, config={"mime_type": "application/pdf"})

        # Wait for the file to be processed by Google
        while uploaded_file.state.name == "PROCESSING":
            print(".", end="")
            time.sleep(2)
            uploaded_file = client.files.get(name=uploaded_file.name)

        if uploaded_file.state.name == "FAILED":
            raise ValueError("File failed to process")

        ocr_prompt = load_ocr_prompt()

        for attempt in range(_GEMINI_MAX_RETRIES):
            try:
                response = await client.aio.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        types.Part.from_uri(file_uri=uploaded_file.uri, mime_type="application/pdf"),
                        ocr_prompt,
                    ],
                )
                return response.text
            except Exception as e:
                if attempt < _GEMINI_MAX_RETRIES - 1 and _gemini_error_is_transient(e):
                    delay = _GEMINI_RETRY_INITIAL_DELAY_SEC * (2**attempt)
                    logger.warning(
                        "Gemini transient error (attempt %s/%s), retrying in %.1fs: %s",
                        attempt + 1,
                        _GEMINI_MAX_RETRIES,
                        delay,
                        e,
                    )
                    await asyncio.sleep(delay)
                    continue
                logger.error(f"Error in get_response_from_gemini: {e}")
                return {"error": "get_response_from_gemini_error", "detail": str(e)}
    except Exception as e:
        logger.error(f"Error in get_response_from_gemini: {e}")
        return {"error": "get_response_from_gemini_error", "detail": str(e)}
    finally:
        if client is not None and uploaded_file is not None:
            try:
                await client.aio.files.delete(name=uploaded_file.name)
            except Exception as e:
                logger.error(f"Error in deleting file: {e}")
