from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
import xml.dom.minidom
import get_all_train
app = Flask(__name__)

path = r'config.xml'
element = xml.dom.minidom.parse(path)

root = element.documentElement
channel_secret =  root.getElementsByTagName('channel_secret')[0].firstChild.data
channel_access_token =  root.getElementsByTagName('channel_access_token')[0].firstChild.data



line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    input_text = event.message.text
    if '?' in input_text:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='請輸入 起點,終點,時間 (使用,分開)站名可使用代號或部分中文站名表示\ne.g.\n\nA8,高鐵,!1400\n表示A8長庚醫院站到A18桃園高鐵站且"出發時間"為14點整\n\n北車,長庚,@1400\n表示A1台北車站到A8長庚醫院站且"抵達時間"為14點整\n\n北車,二航廈\n表示A1台北車站到A13機場第二航廈站且"出發時間"為現在\n\n\n現在有支援直達車查詢囉!可以試試看\n\n#1,8,@1400\n\n表示A1台北車站到A8長庚醫院站且"抵達時間"為14點整的直達車！'))
    elif "？" in input_text:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='請輸入 起點,終點,時間 (使用,分開)站名可使用代號或部分中文站名表示\ne.g.\n\nA8,高鐵,!1400\n表示A8長庚醫院站到A18桃園高鐵站且"出發時間"為14點整\n\n北車,長庚,@1400\n表示A1台北車站到A8長庚醫院站且"抵達時間"為14點整\n\n北車,二航廈\n表示A1台北車站到A13機場第二航廈站且"出發時間"為現在\n\n\n現在有支援直達車查詢囉!可以試試看\n\n#1,8,@1400\n\n表示A1台北車站到A8長庚醫院站且"抵達時間"為14點整的直達車！'))
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=get_all_train.main(input_text)+'\n\n\n可以輸入?看看有沒有新功能喔！'))
        




if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)