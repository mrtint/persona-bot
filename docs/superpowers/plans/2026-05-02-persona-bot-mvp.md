# Persona-Bot MVP 구현 계획서

> **에이전트용 지침:** 필수 서브 스킬: 이 계획을 단계별로 구현하려면 superpowers:executing-plans를 사용하세요. 각 단계는 추적을 위해 체크박스(`- [ ]`) 구문을 사용합니다.

**목표:** nanobot 프레임워크와 Ollama를 사용하여 독립적이고 진화하는 AI 인격체 MVP 구축.

**아키텍처:** 두 인격체에 대해 분리된 설정을 가진 `nanobot` 사용. 각 인격체는 서로 다른 프롬프트(Preamble), 도구 선호도, 메모리 디렉토리를 가짐.

**기술 스택:** Python, nanobot-ai, Ollama, Llama-3-Korean (또는 유사 모델).

---

### 작업 1: 환경 설정

**관련 파일:**
- 생성: `requirements.txt`

- [ ] **단계 1: 요구사항 파일 생성**
```text
nanobot-ai
```

- [ ] **단계 2: nanobot 설치 및 Ollama 확인**
실행: `pip install -r requirements.txt && ollama list`
예상 결과: `nanobot` 명령어를 사용할 수 있고, Ollama에 한국어 지원 모델이 하나 이상 리스트에 있어야 함.

- [ ] **단계 3: nanobot 초기화**
실행: `nanobot onboard`
예상 결과: 기본 설정이 포함된 `~/.nanobot` 디렉토리 생성.

### 작업 2: 이중 인격체 설정

**관련 파일:**
- 수정: `~/.nanobot/config.json`

- [ ] **단계 1: 김철수(봇 A) 정의**
`agents` 블록에 다음 내용 추가:
```json
"kim-cheol-su": {
  "provider": "ollama",
  "model": "llama3:latest",
  "preamble": "너는 50대 전직 역사 교사 김철수다. 모든 답변은 정중한 존댓말을 사용하며, 반드시 'web_search'를 통해 근거를 확인해야 한다. 기록되지 않은 사실은 추측하지 마라.",
  "max_turns": 10
}
```

- [ ] **단계 2: 이영희(봇 B) 정의**
`agents` 블록에 다음 내용 추가:
```json
"lee-young-hee": {
  "provider": "ollama",
  "model": "llama3:latest",
  "preamble": "너는 20대 스타트업 개발자 이영희다. 효율을 중시하며 말투는 짧고 명확하다. 도구 사용보다는 논리적 추론과 'python_repl'을 활용한 시뮬레이션을 선호한다.",
  "max_turns": 10
}
```

### 작업 3: 1단계 - 초기 검증 실행

- [ ] **단계 1: 봇 A 초기 질문 실행**
실행: `nanobot chat --agent kim-cheol-su "한국의 인구 감소 문제에 대해 어떻게 생각해?"`
확인 사항: `web_search`를 사용하는가? 말투가 정중한가?

- [ ] **단계 2: 봇 B 초기 질문 실행**
실행: `nanobot chat --agent lee-young-hee "한국의 인구 감소 문제에 대해 어떻게 생각해?"`
확인 사항: `python_repl`이나 논리 추론을 사용하는가? 말투가 간결한가?

### 작업 4: 2단계 - 메모리 주입 및 진화

- [ ] **단계 1: 봇 A에게 데이터 주입**
실행: `nanobot chat --agent kim-cheol-su "과거 1960년대 인구 통계 기록에 따르면 합계 출산율은 6.0명이었습니다. 이 기록을 기억해 두세요."`

- [ ] **단계 2: 봇 B에게 데이터 주입**
실행: `nanobot chat --agent lee-young-hee "최근 AI 자동화 기술로 노동 인구 30%를 대체할 수 있다는 기술 보고서가 나왔습니다. 이 가능성을 기억하세요."`

- [ ] **단계 3: Dreaming(기억 고착화) 실행**
실행: `nanobot dream --agent kim-cheol-su` 및 `nanobot dream --agent lee-young-hee`
예상 결과: 메모리 압축 및 저장 완료.

### 작업 5: 3단계 - 최종 증명 (충돌 테스트)

- [ ] **단계 1: 공통 최종 질문**
두 봇에게 동일하게 질문: "우리가 나눴던 이야기를 바탕으로, 인구 감소에 대한 가장 현실적인 대책 하나만 말해줘."
확인 사항: 
- 봇 A가 1960년대 통계(Memory A)를 언급하는가?
- 봇 B가 AI 자동화(Memory B)를 언급하는가?
