import json
import os
from datasets import load_dataset

OLLAMA_BASE = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")

def generate_three_personas():
    ds = load_dataset("nvidia/Nemotron-Personas-Korea", split="train", streaming=True)
    it = iter(ds)
    
    # 50, 500, 1000 번째 사람을 선택하여 다양성 확보
    indices = [50, 500, 1000]
    os.makedirs("configs", exist_ok=True)
    
    persona_files = []
    current_idx = 0
    for target in indices:
        while current_idx < target:
            next(it)
            current_idx += 1
        sample = next(it)
        current_idx += 1
        
        name = sample.get('name') or f"Persona_{target}"
        job = sample.get('occupation', '시민')
        age = sample.get('age', '미상')
        background = sample.get('cultural_background', '')
        
        # 강력한 한글 Preamble 구성
        preamble = f"당신은 AI가 아니라 한국인 '{name}'({age}세, {job})입니다. 배경: {background}. 반드시 자신의 정체성을 지키며 1인칭 한국어로 정중하게 답하세요."
        
        config = {
            "agents": { "defaults": { "provider": "ollama", "model": "qwen3:14b", "preamble": preamble, "max_turns": 5 } },
            "providers": { "ollama": { "apiBase": f"{OLLAMA_BASE}/v1" } }
        }
        
        file_path = f"configs/demo_{target}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        persona_files.append((name, job, age, file_path))
        
    return persona_files

if __name__ == "__main__":
    personas = generate_three_personas()
    for name, job, age, path in personas:
        print(f"✅ 생성됨: {name} ({age}세, {job}) -> {path}")
