"""로컬 Ollama와 연결되는 간단한 CLI 챗봇."""

import json
import sys

import requests

sys.stdout.reconfigure(encoding="utf-8")
sys.stdin.reconfigure(encoding="utf-8")

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "gemma4:e2b"


def main():
    print(f"Ollama 챗봇 ({MODEL}) - 종료하려면 'exit' 또는 'quit' 입력\n")

    messages = []

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("종료합니다.")
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        try:
            response = requests.post(
                OLLAMA_URL,
                json={"model": MODEL, "messages": messages, "stream": True},
                stream=True,
                timeout=120,
            )
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            print("\n[오류] Ollama 서버에 연결할 수 없습니다. 'ollama serve'가 실행 중인지 확인하세요.\n")
            messages.pop()
            continue

        print("Bot: ", end="", flush=True)
        full_reply = ""
        for line in response.iter_lines():
            if not line:
                continue
            chunk = json.loads(line)
            content = chunk.get("message", {}).get("content", "")
            print(content, end="", flush=True)
            full_reply += content
            if chunk.get("done"):
                break
        print("\n")

        messages.append({"role": "assistant", "content": full_reply})


if __name__ == "__main__":
    main()
