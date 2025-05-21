# たまちゃんの "こころの相談ノート" チャット風アプリ（LINE風デザイン改良）

import streamlit as st
from openai import OpenAI
import base64
import random
from datetime import datetime

# 🔐 パスワード認証
PASSWORD = "happy!"
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

# ランダムな初回メッセージ候補
greeting_options = [
    "ねえ、今日はどんなことがあった？なんでも話して大丈夫だよ🍀",
    "よかったら、いまの気持ち、ここに置いていってもいいよ🌿",
    "うんうん、まずは深呼吸して…どこから話してみようか？",
    "なんだかモヤモヤする？そのまんまでも大丈夫だよ。",
    "言葉にならなくてもいいよ。浮かんだこと、ここに書いてみて🕊️"
]
initial_greeting = random.choice(greeting_options)

# セッション初期化
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": initial_greeting}
    ]

# タイトルとヒント表示
st.markdown("""
<div style="text-align: center; line-height: 1.8; font-size: 22px; font-weight: bold;">
なんでも置いてって～こころの休憩所～<br>ゆるっと、話そ？
</div>
""", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
<small>📝 答えづらいな…って思ったときは、<strong>「選択肢ほしい」</strong>って言ってみてね。あいちゃんが、ヒントをくれるよ🌱</small>
""", unsafe_allow_html=True)

# LINE風スタイルCSS（吹き出し＋しっぽ＋背景）
st.markdown("""
    <style>
        html, body, [data-testid="stApp"] {
            background-color: #93aad4 !important;
        }
        .main .block-container {
            background-color: #93aad4 !important;
        }
        .bubble-left {
            position: relative;
            background: #ffffff;
            color: #000;
            padding: 10px 15px;
            border-radius: 15px;
            margin: 5px 0;
            max-width: 70%;
            text-align: left;
        }
        .bubble-left::after {
            content: "";
            position: absolute;
            left: -10px;
            top: 10px;
            width: 0;
            height: 0;
            border: 10px solid transparent;
            border-right-color: #ffffff;
            border-left: 0;
            margin-top: -10px;
        }
        .bubble-right {
            position: relative;
            background: #93de83;
            color: #000;
            padding: 10px 15px;
            border-radius: 15px;
            margin: 5px 0;
            max-width: 70%;
            text-align: left;
        }
        .bubble-right::after {
            content: "";
            position: absolute;
            right: -10px;
            top: 10px;
            width: 0;
            height: 0;
            border: 10px solid transparent;
            border-left-color: #93de83;
            border-right: 0;
            margin-top: -10px;
        }
        .meta {
            font-size: 10px;
            color: #444;
            text-align: right;
            margin-top: 4px;
        }
    </style>
""", unsafe_allow_html=True)

# 吹き出し描画（テキスト＋時間＋既読）
def render_bubble(message, sender="user"):
    timestamp = datetime.now().strftime("%p %I:%M").replace("AM", "午前").replace("PM", "午後")
    if sender == "assistant":
        st.markdown(f"""
        <div style="display:flex; justify-content:flex-start; align-items:flex-start; margin-bottom:10px">
            <div class="bubble-left">
                {message}<br>
                <div class="meta">{timestamp}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif sender == "user":
        st.markdown(f"""
        <div style="display:flex; justify-content:flex-end; align-items:flex-start; margin-bottom:10px">
            <div class="bubble-right">
                {message}<br>
                <div class="meta">既読　{timestamp}</div>
            </div>
        </div>
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

    with st.spinner("あいちゃんが考え中…"):
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
