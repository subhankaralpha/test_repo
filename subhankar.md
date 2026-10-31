# Subhankar

> Maintainer and original author of this repository.

This profile is built from what the repository itself shows: commit history, authorship, and the code that was contributed. Anything that can't be verified from the repo is marked _TBD_ so Subhankar or a teammate can fill it in.

---

## At a Glance

| Field            | Details                                              |
| ---------------- | ---------------------------------------------------- |
| **Name**         | Subhankar                                            |
| **GitHub handle**| `subhankaralpha`                                     |
| **Email**        | subhankar@octamem.com                                |
| **Organization** | OctaMem                                              |
| **Role**         | Repository owner and primary contributor             |
| **Active since** | June 28, 2026 (first commit to this repository)      |
| **Location**     | _TBD_                                                |

---

## Background

Subhankar works at **OctaMem**, as their `octamem.com` email address shows. They set up this repository as a **testing and benchmarking workspace**. The README describes it simply as a "Testing repo".

More background (education, previous roles, years of experience) is _TBD_.

---

## Role in the Project

Subhankar is the **creator and sole committer** of the repository so far. Their responsibilities include:

- **Repository setup**: created the project and its initial `README.md`.
- **Benchmark design**: laid out the benchmark suite structure, with separate modules for each stage of the pipeline.
- **LLM integration**: wrote the working Gemini-based benchmark (`bench_llm.py`).
- **Ownership and direction**: decides what the benchmark suite measures and how it grows.

---

## Contributions

### Commit History

| Date (2026)     | Commit                 | Summary                                            |
| --------------- | ---------------------- | -------------------------------------------------- |
| Jun 28, 23:41   | `ab6197f`              | Added the benchmark files (initial upload)         |
| Jun 28, 23:42   | `4e806cc`              | Created `README.md`                                |

### Files Authored

| File                        | Status        | Purpose                                                        |
| --------------------------- | ------------- | -------------------------------------------------------------- |
| `bench_llm.py`              | Implemented   | Benchmarks LLM-based OCR on PDF documents using Google Gemini  |
| `bench_document_ingest.py`  | Placeholder   | Planned benchmark for document ingestion                       |
| `bench_embed.py`            | Placeholder   | Planned benchmark for embedding generation                     |
| `bench_retrieval.py`        | Placeholder   | Planned benchmark for retrieval quality and performance        |
| `README.md`                 | Implemented   | Project description                                            |

### Highlight: `bench_llm.py`

This module shows how Subhankar approaches production-minded engineering:

- **Async I/O**: uses `asyncio` with the async Google GenAI client (`client.aio`) for uploads and generation.
- **Resilient retries**: retries transient errors (HTTP `503`/`429`, "unavailable", "resource exhausted") up to 6 times with **exponential backoff**, starting at a 2-second delay.
- **Resource cleanup**: a `finally` block always deletes the uploaded file from Gemini storage, even when something fails.
- **Externalized prompts**: the OCR prompt lives in a YAML template (`prompts/ocr.yaml`) instead of being hard-coded.
- **Structured error reporting**: failures come back as structured dictionaries (`{"error": ..., "detail": ...}`) instead of raw exceptions, so benchmark runs can keep going.
- **Secrets hygiene**: the API key is read from the `GEMINI_API_KEY` environment variable.

---

## Areas of Expertise

Based on the work in this repository:

- **Python**: modern async Python, logging, `pathlib`, YAML configuration.
- **LLM and GenAI integration**: Google Gemini (`gemini-2.5-flash`), multimodal (PDF) inputs, prompt management.
- **Document AI / OCR**: LLM-driven text extraction from PDF documents.
- **Retrieval and RAG pipelines**: the benchmark layout (ingest → embed → retrieve → LLM) follows a retrieval-augmented generation stack, which fits OctaMem's memory-focused work.
- **Reliability engineering**: retry policies, backoff strategies, graceful failure handling.
- **Performance benchmarking**: breaking a pipeline into stages that can be measured independently.

---

## Working Style

- **Modular**: each pipeline stage gets its own benchmark file.
- **Scaffolds first**: creates placeholder modules early so the overall structure is clear before every part is built.
- **Robust**: plans for unreliable external APIs from the start.

---

## Contact

- **Email:** subhankar@octamem.com
- **GitHub:** [`subhankaralpha`](https://github.com/subhankaralpha)

---

## To Be Completed

Subhankar can fill in these sections, which can't be derived from the repository:

- [ ] Professional background and previous roles
- [ ] Education
- [ ] Location / time zone
- [ ] Specific title at OctaMem
- [ ] Interests outside of work
- [ ] Preferred communication channels
