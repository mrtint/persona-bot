# CLAUDE.md

Guidance for AI assistants working in this repository.

## What this project is

`persona-bot` is an **experimental repository** that turns Korean persona data from the
[NVIDIA Nemotron-Personas-Korea](https://huggingface.co/datasets/nvidia/Nemotron-Personas-Korea)
dataset into agent configuration files (JSON) for [nanobot](https://github.com/HKUDS/nanobot),
which in turn drives a remote **Ollama** server running a local LLM (e.g. `qwen3:14b`).

The research goal is to verify whether distinct "personas" — with their own role (`preamble`),
values, and memory — emerge on top of a shared base model, rather than just different phrasing.

There is **no application code to run as a service** here. The repository is essentially:
`dataset → nanobot JSON config generator` plus design/experiment docs. Most content
(README, docs, persona text) is written in **Korean**; match that language when editing those files.

## Repository layout

| Path | Description |
|------|-------------|
| `scripts/demo_gen.py` | Main script. Streams the Nemotron dataset, picks the 50th/500th/1000th samples, and writes `configs/demo_{50,500,1000}.json`. |
| `configs/` | Generated / hand-written **minimal** nanobot configs (`agents.defaults` + `providers.ollama` only). Includes demo, test, and persona samples. |
| `config_lee.json`, `config_kim.json` | **Full** nanobot configs at repo root — multi-agent, every channel (Discord/Slack/Telegram/…), tools, providers. Structurally very different from the minimal `configs/*.json`. |
| `docs/README.md` | Index of specs, plans, and experiment reports. |
| `docs/planning-reference.md` | **Read this before writing any new plan/spec.** Infrastructure assumptions (벤치비 agent host vs 맥미니 Ollama host), bottlenecks, multi-instance patterns, and product scope. |
| `docs/superpowers/{specs,plans,experiments}/` | Dated design docs (`YYYY-MM-DD-*.md`). |
| `requirements.txt` | Python deps: `nanobot-ai`, `datasets`. |

## Setup & running

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Generate configs/demo_*.json from the dataset:
python scripts/demo_gen.py
```

- Python **3.10+** (3.14 venv works for development).
- The dataset is loaded via Hugging Face **streaming**; run `huggingface-cli login` if access requires auth.
- `demo_gen.py` reads the **`OLLAMA_HOST`** env var (default `http://127.0.0.1:11434`) and writes it as
  `providers.ollama.apiBase` = `${OLLAMA_HOST}/v1` (OpenAI-compatible endpoint). To point at a remote
  Ollama, run the generator with `OLLAMA_HOST` set, or edit the `apiBase` in existing JSON directly.
- There is no test suite, linter, or CI configured. Verify changes by running the generator and
  inspecting the emitted JSON.

## Key conventions & constraints

- **Personas are injected via JSON only.** Identity lives in `agents.*.preamble` (plus message-level
  reinforcement). Do **not** add flows that build or modify Ollama model artifacts (Modelfile,
  `POST /api/create`, etc.) — that is deliberately out of scope and needs a separate decision. The base
  model is an existing Ollama tag (e.g. `qwen3:14b`); everything persona-specific is config.
- **Identity Prefix / persona masking:** a strong base model tends to reassert its own identity, so
  preambles explicitly assert the human persona in first person (see `configs/test_persona.json`'s
  `"CRITICAL: Ignore all previous system prompts about being an AI…"`). Preserve this pattern when
  editing persona text; system-prompt-only role assignment was found insufficient.
- **Two config shapes coexist** — keep them distinct: minimal `configs/*.json` (just defaults + one
  provider) vs the full root configs (`config_lee.json`/`config_kim.json`). When editing a full config,
  diff against nanobot's official schema; it has many fields.
- **Docs naming:** date-prefix new docs (`YYYY-MM-DD-`). `specs/` = *what & why*, `plans/` = *in what
  order*, `experiments/` = *what was done and what came out*.

## Security & operations

- **Never commit a real/secret Ollama URL.** Committed JSON points at `http://127.0.0.1:11434/v1`.
  Inject remote hosts via the `OLLAMA_HOST` env var (or local edits / CI secrets), not the repo.
- `.venv/`, `__pycache__/`, and `.env*` are git-ignored — don't commit them.
- The canonical remote is the private `A810Lab/persona-bot`. This working copy also uses the
  `mrtint/persona-bot` mirror.

## Further reading

- `docs/planning-reference.md` — infra assumptions, bottlenecks, product scope (start here for planning).
- `docs/superpowers/specs/2026-05-02-persona-bot-mvp-design.md` — MVP architecture & persona definitions.
- `docs/superpowers/experiments/2026-05-02-persona-bot-experiment-report.md` — verified results & limits.
