# 인격체 생성기 (Persona Generator) 구현 계획서

> **에이전트용 지침:** 필수 서브 스킬: 이 계획을 단계별로 구현하려면 superpowers:executing-plans를 사용하세요. 각 단계는 추적을 위해 체크박스(`- [ ]`) 구문을 사용합니다.

**목표:** NVIDIA 한국인 페르소나 데이터셋을 `nanobot` 설정 파일로 자동 변환하는 Python 도구 구축.

**아키텍처:**
1. `datasets` 라이브러리를 사용해 데이터셋 로드.
2. `ollama` API를 사용하여 정밀 Preamble 생성.
3. 결과물을 JSON 파일로 출력.

**기술 스택:** Python, datasets, ollama-python, nanobot.

---

### 작업 1: 라이브러리 설치 및 기초 코드 작성

**관련 파일:**
- 생성: `scripts/persona_gen.py`
- 수정: `requirements.txt`

- [ ] **단계 1: 추가 패키지 설치**
```text
datasets
ollama
```
실행: `pip install datasets ollama`

- [ ] **단계 2: 기초 데이터 로드 코드 작성**
`scripts/persona_gen.py`에 데이터셋을 불러와 샘플 하나를 출력하는 코드 작성.
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
- 수정: `scripts/persona_gen.py`

- [ ] **단계 1: Ollama 연동 코드 추가**
샘플 데이터를 바탕으로 봇의 성격과 지침을 생성하는 함수 구현.
- [ ] **단계 2: 프롬프트 템플릿 설계**
`cultural_background`, `skills_expertise` 등을 포함하여 "행동 양식"을 추출하도록 프롬프트 구성.

### 작업 3: nanobot 설정 파일 생성 및 저장

**관련 파일:**
- 수정: `scripts/persona_gen.py`

- [ ] **단계 1: JSON 출력 함수 구현**
`name`을 파일명으로 하고, `nanobot` 호환 구조로 JSON 저장.
- [ ] **단계 2: 스킬 자동 매핑 로직 추가**
`skills_list`에 특정 키워드가 있으면 `web`이나 `exec` 도구를 활성화하는 코드 작성.

### 작업 4: 통합 테스트 및 시연

- [ ] **단계 1: 무작위 인격체 생성 실행**
실행: `python scripts/persona_gen.py`
- [ ] **단계 2: 생성된 인격체로 nanobot 실행**
실행: `nanobot agent -c configs/<생성된이름>.json -m "자기소개 부탁드려요."`
- [ ] **단계 3: 결과 검증**
데이터셋의 정보와 AI의 페르소나가 일치하는지 확인.
