#!/usr/bin/python
# coding=utf-8

import sys
import requests
import json
import telepot
import traceback
from datetime import datetime
from lostark_api_token import Token


MAX_MSG_LENGTH = 300
headers = {
    'accept': 'application/json',
    'authorization': "bearer " + Token
}
TOKEN = '7136216320:AAGACewrMFFDf3_XtqylY4zCAWOI24xV9oY'
bot = telepot.Bot(TOKEN)

ITEM_CODES = {
    "경명돌": "66110223",
    "위명돌": "66110222",
    "찬명돌": "66110224",
    "정파강": "66102005",
    "파강": "66102004",
    "정수강": "66102105",
    "수강": "66102104",
    "명파(대)": "66130133",
    "명파(중)": "66130132",
    "명파(소)": "66130131",
    "상레하": "6861009",
    "최상레하": "6861011"
}

def get_market_data(item_code):
    url = "https://developer-lostark.game.onstove.com/markets/items/" + item_code
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def format_market_data(data):
    if data:
        formatted_data = ""
        for item in data[0]['Stats']:
            date = item.get('Date')
            price = item.get('AvgPrice')
            formatted_data += f"{date} - {price}\n"
        return formatted_data
    else:
        return "데이터를 불러오지 못했습니다."

def send_message(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)
