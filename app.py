import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv

load_dotenv() #.envファイルから環境変数を読み込む

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ["ACCESS_TOKEN"]) # LINE Messaging APIのアクセストークン設定 インスタンス化
handler = WebhookHandler(os.environ["CHANNEL_SECRET"]) # APIのチャネルシークレット設定　ウェブフックから来た情報と照合するためのインスタンス化


@app.route("/")
def index():
    return "you call index()"


@app.route("/push_sample")
def push_sample():
    """プッシュメッセージを送る"""
    user_id = os.environ["USER_ID"]
    line_bot_api.push_message(
        user_id, TextSendMessage(text="Hello World!")
    )
    return "OK"


@app.route("/callback", methods=["POST"])
def callback():
    """Messaging APIからの呼び出し関数"""
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=event.message.text)
    )
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)