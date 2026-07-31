import streamlit as st
import ollama

# 사용할 모델명 설정
MODEL_NAME = "gpt-oss:20b-cloud"

st.set_page_config(page_title="내 전용 Ollama 챗봇", page_icon="💬")
st.title("💬 Local Ollama Chatbot")
st.caption(f"Model: {MODEL_NAME}")

# 대화 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 내용 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자 메시지 저장 및 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 어시스턴트 답변 응답 처리 (스트리밍)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            # Ollama API 호출 (실시간 스트리밍 답변)
            response = ollama.chat(
                model=MODEL_NAME,
                messages=st.session_state.messages,
                stream=True,
            )

            for chunk in response:
                content = chunk.get("message", {}).get("content", "")
                full_response += content
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Ollama 연동 중 오류 발생: {e}")
            full_response = "오류가 발생했습니다. Ollama 서비스가 실행 중인지 확인해 주세요."

    # 챗봇 답변 저장
    st.session_state.messages.append({"role": "assistant", "content": full_response})