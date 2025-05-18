# たまちゃんの "こころの相談ノート" チャット風アプリ（Secrets対応＋system非表示）
# 使用技術：Streamlit + OpenAI API（新バージョン）

import streamlit as st
from openai import OpenAI

# OpenAI APIキーとプロンプトをSecretsから取得
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
system_prompt = st.secrets["SYSTEM_PROMPT"]

# 初期化：セッション状態で会話履歴を保持
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": "ねえ、今日はどんなことがあった？なんでも話して大丈夫だよ🍀"}
    ]

# タイトル表示
st.title("こころの相談ノート by あいちゃん")
st.markdown("---")

# チャット履歴の表示（systemメッセージは除外）
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 入力欄
user_input = st.chat_input("あなたの気持ち、ここに書いてね…")

if user_input:
    # ユーザーの入力を追加
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # AIの返答を取得
    with st.chat_message("assistant"):
        with st.spinner("あいちゃんが考え中…"):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.messages
                )
                reply = response.choices[0].message.content
            except Exception as e:
                reply = "あいちゃん、いまちょっと混み合ってるみたい💦 もう一度時間をおいて話しかけてみてね。"
            st.markdown(reply)

    # 返答を会話履歴に追加
    st.session_state.messages.append({"role": "assistant", "content": reply})
