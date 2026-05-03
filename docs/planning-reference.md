# 작업 계획 참고 자료

새 플랜·스펙·이슈를 쓸 때 **전제(인프라·병목·저장소 범위)**를 맞추기 위한 요약입니다. 세부 구현은 각 날짜별 `superpowers/` 문서와 루트 [`README.md`](../README.md)를 따릅니다.

---

## 1. 용어: 벤치비와 맥미니

| 이름 | 하드웨어(전제) | 역할 |
|------|----------------|------|
| **벤치비** | Intel N100, RAM **16GB**, 저장소 **512GB** | **에이전트 구동용** — nanobot 게이트웨이/CLI 등. 여기서는 **추론을 하지 않고** 맥미니의 Ollama에 HTTP로 요청합니다. |
| **맥미니** | Apple **M4**, RAM **24GB**, 저장소 **512GB** | **Ollama 전용** — LLM 가중치·동시 추론·KV 캐시 등 **실제 토큰 생성 부하**의 중심. |

네트워크는 같은 LAN 등 **지연·대역이 충분한 구간**을 가정합니다. 플랜에 “오프라인 맥미니”·“공인망만 있는 벤치비” 같은 예외가 있으면 별도로 명시합니다.

---

## 2. 병목을 어디에 두고 계획할지

### 벤치비 (에이전트 호스트)

- **CPU(N100)**보다 **RAM·동시 연결·프로세스 수**가 먼저 의미 있습니다.
- nanobot **게이트웨이**(디스코드/텔레그램 등)는 프로세스당 메모리·웹소켓 부담이 **CLI만 도는 인스턴스**보다 큽니다. “에이전트 N개” 플랜에는 **종류(게이트웨이 vs 배치 CLI)**를 구분해 적는 것이 좋습니다.
- 상한을 숫자로 고정하기 어렵다면, 플랜에 **검증 방법**(예: `free -h`, 프로세스 수 늘릴 때 OOM 여부)을 적어 두면 됩니다.

### 맥미니 (Ollama)

- **동시에 활성인 채팅 completion** 수·**컨텍스트 길이**·**모델(예: 14B Q4)**이 처리량을 가늠합니다.
- 에이전트(벤치비)가 많아도 **대부분 유휴**면 맥미니는 순차 처리로도 버틸 수 있고, **여러 세션이 동시에 긴 생성**을 하면 대기·지연이 납니다.
- 플랜에 “동시 몇 세션까지 SLA”가 있으면 **맥미니 기준**으로 적습니다.

---

## 3. nanobot 여러 인스턴스 (요약)

- **인스턴스를 나누는 단위:** `--config` 경로와(초기화 시) `--workspace`를 **인스턴스마다 분리**.
- **게이트웨이를 여러 개:** `nanobot gateway --config <경로>` 를 쓰고, 포트가 겹치면 **`--port`**로 분리.
- **CLI로 특정 설정만:** `nanobot agent -c <config.json> -m "..."`  
- 공식 가이드: [nanobot multiple-instances](https://github.com/hkuds/nanobot/blob/main/docs/multiple-instances.md)

플랜에 “페르소나별 완전 분리(설정·메모리·포트)”가 필요하면 위 패턴을 명시합니다.

---

## 4. 이 저장소의 제품 범위 (계획 시 제약)

다음은 **의도적으로 하지 않는 것**입니다. 플랜에 다시 넣으려면 별도 의사결정이 필요합니다.

- Ollama **Modelfile** / **`POST /api/create`** 등으로 **모델 아티팩트를 만들거나 수정**하는 흐름
- 베이스 모델은 **맥미니 Ollama에 이미 있는 태그**(예: `qwen3:14b`)를 쓰고, 페르소나는 **`agents.*.preamble` 등 JSON 설정**으로만 주입

구현 축은 [`scripts/demo_gen.py`](../scripts/demo_gen.py)처럼 **데이터셋 → nanobot JSON**이며, Ollama 주소는 생성 시 **`OLLAMA_HOST`** 환경 변수(기본 `http://127.0.0.1:11434`)로 반영합니다.

---

## 5. 데이터·모델 전제

- 페르소나 소스 데이터셋: **`nvidia/Nemotron-Personas-Korea`** (Hugging Face `datasets`, 스트리밍)
- nanobot·Ollama 연동은 프로젝트 설정 예시와 같이 **OpenAI 호환 `apiBase`** (`…/v1`) 패턴

---

## 6. 관련 내부 문서

| 문서 | 참고 시점 |
|------|------------|
| [superpowers/specs/2026-05-02-persona-bot-mvp-design.md](superpowers/specs/2026-05-02-persona-bot-mvp-design.md) | 페르소나 MVP 목표·시나리오 |
| [superpowers/plans/2026-05-02-persona-bot-mvp.md](superpowers/plans/2026-05-02-persona-bot-mvp.md) | MVP 단계 작업 |
| [superpowers/plans/2026-05-02-persona-generator.md](superpowers/plans/2026-05-02-persona-generator.md) | 생성기( JSON 출력 ) 플랜 — 모델 파일 수정 없음 |
| [superpowers/experiments/2026-05-02-persona-bot-experiment-report.md](superpowers/experiments/2026-05-02-persona-bot-experiment-report.md) | 이미 검증된 결론·한계 |

---

## 7. 플랜 문서에 넣기 좋은 체크리스트 (복붙용)

- [ ] 대상 장비가 **벤치비 / 맥미니 / 둘 다** 중 어디인가?
- [ ] 부하는 **에이전트 프로세스**인가, **Ollama 동시 추론**인가?
- [ ] nanobot은 **단일 `config.json`**인가, **인스턴스 분리(`--config` / `--workspace` / `--port`)**인가?
- [ ] 페르소나 주입은 **JSON `preamble`만**으로 충분한가? (모델 커스텀 필요 시 → 별도 결정)
- [ ] `OLLAMA_HOST`·`apiBase`는 **비밀 URL을 저장소에 커밋하지 않는가?**

이 섹션은 필요에 따라 플랜 상단에 그대로 옮겨 써도 됩니다.
