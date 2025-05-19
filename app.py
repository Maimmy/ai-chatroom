# たまちゃんの "こころの相談ノート" チャット風アプリ（アイコン固定＋吹き出し整形）

import streamlit as st
from openai import OpenAI
import base64

# 🔐 パスワード認証
PASSWORD = "secret123"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    pw = st.text_input("🔐 合言葉を入力してください", type="password")
    if pw == PASSWORD:
        st.session_state.authenticated = True
        st.success("ようこそ🌷")
    else:
        st.stop()

# OpenAI APIキーとプロンプトをSecretsから取得
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
system_prompt = st.secrets["SYSTEM_PROMPT"]

# セッション初期化
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": "ねえ、今日はどんなことがあった？なんでも話して大丈夫だよ🍀"}
    ]

# タイトル
st.title("こころの相談ノート")
st.markdown("---")

# 💬 LINE風の吹き出し表示関数（アイコン固定＋カラーカスタム）
def get_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

coach_icon = get_image_base64("20250519coach.png")
client_icon = get_image_base64("20250519client.png")

def render_bubble(message, sender="user"):
    if sender == "assistant":
        st.markdown(f"""
        <div style="display:flex; justify-content:flex-start; align-items:flex-start; margin-bottom:10px">
            <img src="data:image/png;base64,{coach_icon}" width="40" height="40"
                 style="margin-right:10px; border-radius:50%; object-fit:cover; align-self:flex-start;">
            <div style="background-color:#ffffff; padding:10px 15px; border-radius:15px; max-width:70%; text-align:left; border:1px solid #ddd">
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif sender == "user":
        st.markdown(f"""
        <div style="display:flex; justify-content:flex-end; align-items:flex-start; margin-bottom:10px">
            <div style="background-color:#93de83; padding:10px 15px; border-radius:15px; max-width:70%; text-align:left">
                {message}
            </div>
            <img src="data:image/png;base64,{client_icon}" width="40" height="40"
                 style="margin-left:10px; border-radius:50%; object-fit:cover; align-self:flex-start;">
        </div>
        """, unsafe_allow_html=True)

# 背景カラー変更
st.markdown("""
    <style>
        body {
            background-color: #93aad4;
        }
    </style>
    """, unsafe_allow_html=True)

# チャット履歴の表示（systemメッセージは除外）
for msg in st.session_state.messages:
    if msg["role"] == "user":
        render_bubble(msg["content"], sender="user")
    elif msg["role"] == "assistant":
        render_bubble(msg["content"], sender="assistant")

# 入力欄
user_input = st.chat_input("あなたの気持ち、ここに書いてね…")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    render_bubble(user_input, sender="user")

    with st.spinner("ちょっと待ってね…"):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = "あいちゃん、いまちょっと混み合ってるみたい💦 もう一度時間をおいて話しかけてみてね。"
        render_bubble(reply, sender="assistant")
        st.session_state.messages.append({"role": "assistant", "content": reply})
