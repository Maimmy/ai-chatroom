# たまちゃんの "こころの相談ノート" チャット風アプリ（LINE風デザイン改良）

import streamlit as st
from openai import OpenAI
import base64
import random
from datetime import datetime, timedelta

# 🔐 パスワード認証
PASSWORD = "happy!"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    pw = st.text_input("🔐 合言葉を入力してください", type="password")
    if pw == PASSWORD:
        st.session_state.authenticated = True
    else:
        st.stop()

# OpenAI APIキーとプロンプトをSecretsから取得
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
system_prompt = st.secrets["SYSTEM_PROMPT"]

# ランダムな初回メッセージ候補
greeting_options = [
    "ねえ、今日はどんなことがあった？なんでも話して大丈夫だよ",
    "よかったら、いまの気持ち、ここに置いていってもいいよ",
    "うんうん、まずは深吸吼して…どこから話してみようか？",
    "なんだかモヤモヤする？そのまんまでも大丈夫だよ",
    "言葉にならなくてもいいよ。浮かんだこと、ここに書いてみて"
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
なんでも置いてって<br>～こころの休憩所～<br>ゆるっと、話そ？
</div>
""", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
答えづらいな…って思ったときは、<strong>「選択肢ほしい」</strong>って言ってみてね。ヒントをだします！
""", unsafe_allow_html=True)

# LINE風スタイルCSS（吹き出し＋背景・三角削除・アイコン調整＋フッター非表示）
st.markdown("""
    <style>
        html, body, [data-testid="stApp"] {
            background-color: #93aad4 !important;
        }
        .main .block-container {
            background-color: #93aad4 !important;
        }
        header, [data-testid="stStatusWidget"], [data-testid="stToolbar"], .viewerBadge_container__1QSob, .stDeployButton, .stActionButton, .stFloatingButton, footer, #MainMenu {
            display: none !important;
            visibility: hidden;
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
            white-space: pre-wrap;
            word-wrap: break-word;
            font-size: 14px;
        }
        .bubble-right {
            position: relative;
            background: #93de83;
            color: #000;
            padding: 10px 15px;
            border-radius: 15px;
            margin: 5px 0;
            max-width: 90%;
            text-align: left;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-size: 14px;
        }
    </style>
""", unsafe_allow_html=True)

# 吹き出し描画（テキスト）
def render_bubble(message, sender="user"):
    if sender == "assistant":
        st.markdown(f"""
        <div style="display:flex; justify-content:flex-start; align-items:flex-start; margin-bottom:4px">
            <div style="margin-top: 4px; margin-right:8px;">
                <img src="https://raw.githubusercontent.com/Maimmy/ai-chatroom/f086cb7861fd372832d99c02c4d4ad2bcde6ea39/20250519coach.png" width="32" style="min-width:32px; height:auto;" />
            </div>
            <div>
                <div class="bubble-left">{message}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif sender == "user":
        st.markdown(f"""
        <div style="display:flex; justify-content:flex-end; align-items:flex-end; margin-bottom:4px">
            <div>
                <div class="bubble-right">{message}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# チャット履歴の表示（systemメッセージは除外）
for msg in st.session_state.messages:
    if msg["role"] == "user":
        render_bubble(msg["content"], sender="user")
    elif msg["role"] == "assistant":
        render_bubble(msg["content"], sender="assistant")

# 入力段
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
            reply = "あいちゃん、いまちょっと混み合ってるみたい🚦 もう一度時間をおいて話しかけてみてね。"
        render_bubble(reply, sender="assistant")
        st.session_state.messages.append({"role": "assistant", "content": reply})
