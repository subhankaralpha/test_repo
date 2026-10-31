# Contributing

Thanks for your interest in contributing! This document explains how to set up a
local environment, run the benchmark scripts, and submit pull requests.

See [README.md](README.md) for a general overview of the repository.

## Repository Layout

| File | Purpose |
| --- | --- |
| `bench_llm.py` | Benchmarks LLM-based OCR of PDF documents via the Google Gemini API (`gemini-2.5-flash`). |
| `bench_embed.py` | Embedding benchmark (placeholder, not yet implemented). |
| `bench_retrieval.py` | Retrieval benchmark (placeholder, not yet implemented). |
| `bench_document_ingest.py` | Document ingestion benchmark (placeholder, not yet implemented). |

## Setup Steps

### 1. Prerequisites

- Python 3.10 or newer
- `git`
- A Google Gemini API key (needed for `bench_llm.py`)

### 2. Clone the repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 3. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate
```

### 4. Install dependencies

The repository does not yet ship a `requirements.txt`. Install the packages used by
the benchmark scripts directly:

```bash
pip install --upgrade pip
pip install google-genai pyyaml
```

If you add a new third-party dependency, please add it to a `requirements.txt`
(creating one if needed) in the same pull request.

### 5. Configure environment variables

`bench_llm.py` reads the Gemini API key from the environment:

```bash
export GEMINI_API_KEY="your-api-key"
```

Never commit API keys or other secrets. If you use a `.env` file, make sure it is
listed in `.gitignore`.

### 6. Provide the OCR prompt

`bench_llm.py` loads its OCR prompt from `prompts/ocr.yaml`, resolved relative to
the **parent** of the directory containing the script
(`Path(__file__).resolve().parent.parent / "prompts" / "ocr.yaml"`). The file must
contain a `template` key:

```yaml
template: |
  Extract all text from the attached PDF, preserving reading order.
```

### 7. Run the benchmarks

The benchmark modules currently expose functions rather than a command-line entry
point. For example, to exercise the Gemini OCR path from `bench_llm.py`:

```python
import asyncio
import io

from bench_llm import get_response_from_gemini

with open("sample.pdf", "rb") as f:
    stream = io.BytesIO(f.read())

result = asyncio.run(get_response_from_gemini(stream))
print(result)
```

On failure the function returns a dict of the form
`{"error": "get_response_from_gemini_error", "detail": "..."}` instead of raising.
Transient Gemini errors (HTTP 429/503, "resource exhausted", etc.) are retried with
exponential backoff.

When adding a new benchmark, follow the `bench_<area>.py` naming convention and,
ideally, add an `if __name__ == "__main__":` block so it can be run with
`python bench_<area>.py`.

## Pull Request Guidelines

### Branching

- Branch off `main` and keep branches focused on a single change.
- Use descriptive branch names, e.g. `feature/embedding-benchmark` or
  `fix/gemini-retry-backoff`.

### Code style

- Follow [PEP 8](https://peps.python.org/pep-0008/). Running a formatter/linter
  such as `black` and `ruff` before committing is recommended.
- Use type hints on public functions (e.g. `def load_ocr_prompt() -> str:`).
- Use the `logging` module (`logger = logging.getLogger(__name__)`) rather than
  `print` for diagnostic output.
- Keep tunables as module-level constants (e.g. `_GEMINI_MAX_RETRIES`) instead of
  hard-coded values inside functions.
- Read secrets and configuration from environment variables; never hard-code them.
- Use `pathlib.Path` for file paths.
- Clean up external resources (uploaded files, clients) in `finally` blocks, as
  `bench_llm.py` does.

### Commit messages

- Write the subject line in the imperative mood, at most ~72 characters
  (e.g. `Add retrieval benchmark for top-k recall`).
- Separate the subject from the body with a blank line.
- Use the body to explain *what* changed and *why*, not just *how*.
- Keep each commit to one logical change.

### Pull request process

1. Make sure your branch is up to date with `main`.
2. Verify your changes run locally (and that any affected benchmark still works).
3. Open a pull request against `main` with:
   - A clear title summarizing the change.
   - A description of what changed and why, plus how you tested it.
   - Benchmark results (before/after numbers) when the change affects performance.
   - Links to any related issues.
4. Keep pull requests small and focused; split unrelated changes into separate PRs.
5. Address review feedback with follow-up commits; a maintainer will merge once
   the PR is approved.
6. Update `README.md` or this file if your change affects setup or usage.

## Reporting Issues

When opening an issue, include steps to reproduce, the expected and actual
behavior, your Python version and OS, and relevant log output (with secrets
redacted).
