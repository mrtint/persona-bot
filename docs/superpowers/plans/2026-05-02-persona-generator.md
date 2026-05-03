# 인격체 생성기 (Persona Generator) 구현 계획서

> **에이전트용 지침:** 필수 서브 스킬: 이 계획을 단계별로 구현하려면 superpowers:executing-plans를 사용하세요. 각 단계는 추적을 위해 체크박스(`- [ ]`) 구문을 사용합니다.

**목표:** NVIDIA 한국인 페르소나 데이터셋을 `nanobot` 설정 파일로 자동 변환하는 Python 도구 구축. (Ollama **모델 파일·Modelfile·`/api/create` 등은 사용하지 않음** — 베이스 모델은 서버에서 그대로 두고, JSON의 `preamble`만 주입.)

**아키텍처:**
1. `datasets` 라이브러리로 데이터셋 스트리밍 로드.
2. 샘플 필드(`name`, `age`, `occupation`, `cultural_background` 등)로 **템플릿 기반 preamble** 구성.
3. nanobot 호환 JSON으로 저장. Ollama 주소는 `OLLAMA_HOST` 환경 변수로 `apiBase`에 반영.

**기술 스택:** Python, datasets, nanobot.

**구현 참고:** 현재 저장소의 [`scripts/demo_gen.py`](../../../scripts/demo_gen.py)가 위 흐름의 축소 구현(고정 인덱스 50·500·1000)입니다.

---

### 작업 1: 라이브러리 설치 및 기초 코드 작성

**관련 파일:**
- [`scripts/demo_gen.py`](../../../scripts/demo_gen.py)
- [`requirements.txt`](../../../requirements.txt)

- [ ] **단계 1: 패키지 설치**
```text
datasets
```
실행: `pip install -r requirements.txt`

- [ ] **단계 2: 기초 데이터 로드 코드 작성**
`demo_gen.py`와 같이 데이터셋을 불러와 샘플을 순회·출력하는 코드를 유지·확장합니다.
```python
from datasets import load_dataset

def get_sample():
    ds = load_dataset("nvidia/Nemotron-Personas-Korea", split="train", streaming=True)
    sample = next(iter(ds))
    print(f"Name: {sample['name']}, Job: {sample['occupation']}")
    return sample

if __name__ == "__main__":
    get_sample()
```

### 작업 2: Preamble 생성 로직 구현

**관련 파일:**
- [`scripts/demo_gen.py`](../../../scripts/demo_gen.py)

- [ ] **단계 1: 필드 매핑**
샘플 데이터를 바탕으로 말투·정체성 문단을 만드는 함수 구현 (LLM 호출 없이도 가능; 필요 시 별도 서비스에서 생성한 텍스트만 삽입).
- [ ] **단계 2: 프롬프트 템플릿 설계**
`cultural_background`, `skills_expertise` 등을 포함하도록 템플릿 확장.

### 작업 3: nanobot 설정 파일 생성 및 저장

**관련 파일:**
- [`scripts/demo_gen.py`](../../../scripts/demo_gen.py)

- [ ] **단계 1: JSON 출력 함수 구현**
`name` 등을 파일명으로 하고, `nanobot` 호환 구조로 JSON 저장.
- [ ] **단계 2: 스킬 자동 매핑 로직 추가**
`skills_list`에 특정 키워드가 있으면 설정 JSON에서 `web`이나 `exec` 도구를 켜는 필드 반영.

### 작업 4: 통합 테스트 및 시연

- [ ] **단계 1: 인격체 설정 생성 실행**
실행: `python scripts/demo_gen.py` (또는 확장된 진입점)
- [ ] **단계 2: 생성된 인격체로 nanobot 실행**
실행: `nanobot agent -c configs/<생성된이름>.json -m "자기소개 부탁드려요."`
- [ ] **단계 3: 결과 검증**
데이터셋의 정보와 AI의 페르소나가 일치하는지 확인.
