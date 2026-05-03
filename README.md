# persona-bot

한국어 페르소나 데이터([NVIDIA Nemotron-Personas-Korea](https://huggingface.co/datasets/nvidia/Nemotron-Personas-Korea))와 원격 **Ollama**를 연결해, [nanobot](https://github.com/HKUDS/nanobot)용 에이전트 설정(JSON)을 만들거나 Ollama 커스텀 모델을 생성하는 실험용 저장소입니다.

## 목적

- 로컬 LLM 위에서 **역할(preamble)과 기억**을 바탕으로 “서로 다른 인격”이 드러나는지 검증합니다.
- 설계·실험 기록은 [`docs/`](docs/README.md) 아래에 모아 두었습니다.

## 사전 요구사항

- Python 3.10 이상 권장 (개발 시 3.14 venv 사용 가능)
- Hugging Face에 로그인하거나, `nvidia/Nemotron-Personas-Korea` 데이터셋에 접근 가능한 환경
- Ollama 서버에 `qwen3:14b`(또는 스크립트·설정과 동일한 베이스 모델)가 있어야 합니다
- nanobot을 쓰려면 별도로 [`nanobot-ai`](https://pypi.org/project/nanobot-ai/) 패키지 및 nanobot 문서의 CLI 사용법이 필요합니다

## 설치

저장소 루트에서 가상환경을 만든 뒤 의존성을 설치합니다.

```bash
cd /path/to/persona-bot
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Hugging Face 데이터셋을 스트리밍으로 받으므로, 필요 시 `huggingface-cli login`으로 인증합니다.

## 저장소 구조

| 경로 | 설명 |
|------|------|
| [`scripts/demo_gen.py`](scripts/demo_gen.py) | 데이터셋에서 50·500·1000번째 샘플을 뽑아 `configs/demo_*.json` nanobot 설정을 생성 |
| [`scripts/persona_gen.py`](scripts/persona_gen.py) | 스트리밍 첫 샘플로 짧은 시스템 프롬프트를 만들고 Ollama `POST /api/create`로 커스텀 모델 생성 시도 |
| [`configs/`](configs/) | 데모·테스트용 nanobot 설정 (에이전트 `defaults` + `providers.ollama`) |
| [`config_lee.json`](config_lee.json), [`config_kim.json`](config_kim.json) | MVP 실험용으로 보이는 **풀 nanobot 설정**(다중 에이전트, 채널, 도구 등). 루트의 짧은 데모 JSON과 성격이 다릅니다 |
| [`Modelfile_temp`](Modelfile_temp) | Ollama `Modelfile` 예시 (`FROM` + `SYSTEM`) |
| [`docs/`](docs/README.md) | 스펙·플랜·실험 보고서 인덱스 |

## 스크립트 사용법

### nanobot 설정 JSON 생성 (`demo_gen.py`)

```bash
python scripts/demo_gen.py
```

- 출력: `configs/demo_50.json`, `configs/demo_500.json`, `configs/demo_1000.json`
- 각 파일의 `agents.defaults.preamble`에 이름·나이·직업·배경이 한국어로 들어갑니다.
- `providers.ollama.apiBase`는 스크립트에 고정된 Ollama 주소입니다. **본인 서버 주소로 반드시 수정**하세요.

### Ollama 커스텀 모델 생성 (`persona_gen.py`)

```bash
python scripts/persona_gen.py
```

- 데이터셋 **첫 번째** 스트리밍 샘플의 이름을 사용해 `persona_final`이라는 이름으로 모델 생성을 요청합니다.
- Ollama 베이스 URL은 환경 변수 **`OLLAMA_HOST`**로 지정합니다(기본값 `http://127.0.0.1:11434`). 예: `OLLAMA_HOST=http://192.168.1.10:11434 python scripts/persona_gen.py`

## 설정 파일에서 자주 바꾸는 값

nanobot 쪽 최소 예시(`configs/*.json`)는 대략 다음 형태입니다.

- **`agents.defaults.provider`**: `ollama`
- **`agents.defaults.model`**: 예) `qwen3:14b`
- **`agents.defaults.preamble`**: 역할·말투·금지 사항(예: 1인칭, AI라고 하지 않기 등)
- **`agents.defaults.max_turns`**: 대화 턴 상한
- **`providers.ollama.apiBase`**: OpenAI 호환 엔드포인트, 보통 `http://<호스트>:11434/v1`

`config_lee.json`처럼보낸 전체 설정은 필드가 많으므로, nanobot 공식 문서와 함께 diff로 비교하는 것이 안전합니다.

## 보안·운영 참고

- 커밋된 JSON 예시는 **`http://127.0.0.1:11434/v1`** 를 가리킵니다. 원격 Ollama를 쓰면 각 JSON의 `apiBase`를 직접 바꾸거나, `demo_gen.py`를 `OLLAMA_HOST`와 함께 실행해 설정을 다시 생성하세요.
- 스크립트는 **`OLLAMA_HOST`** 환경 변수를 읽습니다. 비밀 URL은 저장소에 넣지 말고 로컬 환경이나 CI 시크릿으로만 주입하세요.
- `.venv/`는 `.gitignore`에 포함되어 있으며 Git에 올리지 않습니다.

## GitHub

정식 저장소: **[https://github.com/A810Lab/persona-bot](https://github.com/A810Lab/persona-bot)** (`origin`, **private** — A810Lab 조직 멤버만 클론/접근 가능).

개인 계정 쪽 미러를 두려면 원격을 추가한 뒤 푸시하면 됩니다.

```bash
git remote add mrtint https://github.com/mrtint/persona-bot.git
git push mrtint main
```

새 저장소를 처음 연결할 때는 예를 들어 다음과 같습니다.

```bash
git remote add origin https://github.com/A810Lab/persona-bot.git
git push -u origin main
```

[GitHub CLI](https://cli.github.com/)로 조직 저장소를 만들 때는 예를 들어 `gh repo create A810Lab/persona-bot --public` 후 위와 같이 `git remote add` / `git push`를 사용합니다.

## 더 읽을 곳

- [문서 목차 (`docs/README.md`)](docs/README.md)
- [MVP 설계 스펙](docs/superpowers/specs/2026-05-02-persona-bot-mvp-design.md)
- [실험 보고서](docs/superpowers/experiments/2026-05-02-persona-bot-experiment-report.md)
