#!/usr/bin/python
# coding=utf-8

import sys
import time
import telepot
from pprint import pprint
from datetime import date
import traceback
import noti
class TelegramBot:
    def handle(msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type != 'text':
            noti.send_message(chat_id, '잘못된 입력입니다.')
            return

        text = msg['text']
        args = text.split(' ')

        if text.startswith('시세') and len(args) > 1:
            item_name = args[1]
            if item_name in noti.ITEM_CODES:
                item_code = noti.ITEM_CODES[item_name]
                print(f'아이템 시세 조회: {item_name} ({item_code})')
                market_data = noti.get_market_data(item_code)
                formatted_data = noti.format_market_data(market_data)
                noti.send_message(chat_id, formatted_data)
            else:
                noti.send_message(chat_id, '알 수 없는 아이템 이름입니다.')
        else:
            noti.send_message(chat_id, '모르는 명령어입니다.\n시세 [아이템 이름] 명령을 사용하세요.')


    today = date.today()
    print(f'[{today}] received token: {noti.TOKEN}')

    bot = telepot.Bot(noti.TOKEN)
    pprint(bot.getMe())

    bot.message_loop(handle)

    print('Listening...')

    while 1:
        time.sleep(10)
