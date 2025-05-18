# たまちゃんの "こころの相談ノート" チャット風アプリ設計
# 使用技術：Streamlit + OpenAI API（ChatGPT）
# 公開：スマホ対応、URLでアクセス可能

import streamlit as st
from openai import OpenAI
import os

# OpenAI APIキー（後で.envやsecretsに設定）
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 初期化：セッション状態で会話履歴を保持
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "あなたは、やさしく寄り添い、感情に共感しながら問いかけをしてくれるAIです。相手の心に寄り添い、否定せず、あたたかい返答をしてください。"},
        {"role": "assistant", "content": "ねえ、今日はどんなことがあった？なんでも話して大丈夫だよ🍀"}
    ]

# タイトル
st.title("こころの相談ノート by あいちゃん")
st.markdown("---")

# チャット表示
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 入力受付
user_input = st.chat_input("あなたの気持ち、ここに書いてね…")

if user_input:
    # ユーザーの入力を保存
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # ChatGPTからの返答を取得
    with st.chat_message("assistant"):
        with st.spinner("あいちゃんが考え中…"):
            from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ChatGPTからの返答を取得（修正後）
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=st.session_state.messages
)

reply = response.choices[0].message.content
            st.markdown(reply)
    
    # 返答を履歴に追加
    st.session_state.messages.append({"role": "assistant", "content": reply})
