# 인격체 생성기 (Persona Generator) 디자인 스펙

## 개요
`nvidia/Nemotron-Personas-Korea` 데이터셋을 활용하여 `nanobot` 에이전트의 인격 설정을 자동으로 생성하는 도구입니다. 데이터 기반의 입체적인 인격체 생성을 목표로 합니다.

## 핵심 기능
1. **페르소나 추출:** 키워드 필터링을 통한 NVIDIA 데이터셋 샘플링.
2. **Preamble 합성:** Ollama를 활용하여 원천 데이터를 구체적인 행동 프로토콜로 변환.
3. **자동 스킬 할당:** 페르소나의 전문 분야에 맞춰 `nanobot` 도구(web, exec 등) 활성화.
4. **설정 자동화:** `nanobot` 호환 JSON 설정 파일 생성 및 저장.

## 데이터 매핑 전략
- `identity`: name, gender, age, occupation
- `worldview`: cultural_background, career_goals_ambitions
- `expertise`: skills_list, major_field
- `style`: narrative lenses (professional, concise, arts 등)

## 검증 방법
생성된 설정 파일을 사용하여 `nanobot`을 즉시 실행하고, 설정된 페르소나의 정체성과 전문성이 답변에 반영되는지 확인.
