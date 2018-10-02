# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import os
import sys
from argparse import ArgumentParser
import requests
import json
import csv
import random

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

#スクレイピングでお店のデータをcsvデータで取得する。
def line_get_data(place):
    f = open('area_s', 'r')
    area_s = json.load(f)
    for x in area_s:
        if place in x['garea_small']['areaname_s']:
            areacode_s = x['garea_small']['areacode_s']
    data={'京都市':3404,'四条':3414,'河原町':3402}
    apikey='0600c456734c0f1315878fc5aeb29fa2&'
    place=data[place]
    url='http://api.gnavi.co.jp/RestSearchAPI/20150630/?keyid={key}&format=json&category_s=RSFST09004&areacode_s=AREAS{place}'.format(key=apikey,place=place)

    html=requests.get(url)

    data=json.loads(html.text)

    with open('a.csv','w',newline='',encoding='utf-8') as w:
        writer=csv.writer(w)
        for k in data['rest']:
            writer.writerow([k['name'],k['url']])

#CSVデータを読み込む。もし、次と呼ばれたりしたら、イテレーターを用いて、
#next(リスト型データ)としたほうがいい。

def line_answer():
    data=[]
    csvfile = 'a.csv'
    f = open(csvfile, "r",encoding="utf-8")
    reader = csv.reader(f)
    for x in reader:
        data.append(x)
    f.close()
    return data

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    if not 'へ飲みに行くぞ' in event.message.text:
        return None
    # この辺に地名をAPIに投げるコードを記述
    # 得られた店名とURLを nomiya_info に格納
    text_split = event.message.text.split("へ")
    place = text_split[0]
    line_get_data(place)
    nomiyas = line_answer()
    if nomiyas = 
    nomiya = random.choice(nomiyas)
    TEXT="{}へ飲みに行くぞ！ {}{}".format(nomiya[0], nomiya[1], areacode_s)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=TEXT) #event.message.text がメッセージの本文
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
