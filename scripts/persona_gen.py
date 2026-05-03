import requests
import json
from datasets import load_dataset
import os

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")

def final_attempt():
    ds = load_dataset("nvidia/Nemotron-Personas-Korea", split="train", streaming=True)
    sample = next(iter(ds))
    name = sample.get('name') or "김영수"
    
    # 가장 단순한 시스템 프롬프트
    system_prompt = f"당신은 {name}입니다. AI가 아닙니다. 1인칭으로만 말하세요."
    
    url = f"{OLLAMA_HOST}/api/create"
    # Modelfile 내용을 한 줄의 문자열로 처리
    modelfile_content = f"FROM qwen3:14b\nSYSTEM {system_prompt}"
    
    payload = {
        "name": "persona_final",
        "modelfile": modelfile_content
    }
    
    print(f"Ollama API 호출 중... (이름: {name})")
    response = requests.post(url, json=payload)
    print(f"응답 상태: {response.status_code}")
    print(f"응답 내용: {response.text}")

if __name__ == "__main__":
    final_attempt()
