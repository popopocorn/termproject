import threading
from tkinter import *
from tkinter import ttk
from url_to_tkPhotoImage import url2PhotoImage
from getAPIs import *
import requests
import json
from lostark_api_token import Token
from tkintermapview import TkinterMapView
import telepot
import time
import traceback
import noti
import sys
from pprint import pprint
from datetime import date
from PIL import ImageGrab
from send_email import *


class TelegramBot:
    def __init__(self):
        self.bot = telepot.Bot(noti.TOKEN)
        self.bot.message_loop(self.handle)

    def handle(self, msg):
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


class mainGUI():
    def __init__(self):
        self.window = Tk()
        self.window.title("Termproject")
        self.window.geometry("1280x720")

        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(expand=True, fill="both")

        # ---------------------------------------------------------------------------------------
        # 캐릭터 검색 notebook 시작
        # ---------------------------------------------------------------------------------------
        frame0 = Frame(self.notebook, width=400, height=40, bg='gray')
        frame0.place(x=10, y=10)
        self.notebook.add(frame0, text="검색")
        # 캐릭터의 이름을 입력할 Entry와 이름을 저장하고 있을 Variable
        self.name_var = StringVar()
        ent = Entry(frame0, width=44, textvariable=self.name_var, relief='solid', borderwidth=10)
        ent.place(x=9, y=0)

        self.name = ''
        # 캐릭터의 이름을 받아올 버튼
        button = Button(frame0, text='검색', bg='white', foreground='black', width=9, height=2, command=self.get_name)
        button.place(x=340)

        self.frame1 = Frame(self.notebook, width=550, height=650, bg='black')
        self.frame1.place(x=10, y=60)

        self.equipment_img_labels = []
        self.equipment_name_labels = []
        self.equipment_name_text_variables = []
        self.equipment_quality_labels = []
        self.equipment_quality_variables = []
        for i in range(6):
            self.equipment_img_labels.append(Label(self.frame1, width=64, height=64, bg='black'))
            self.equipment_img_labels[-1].place(x=10, y=30+100*i)

            self.equipment_name_text_variables.append(StringVar())
            self.equipment_name_text_variables[i].set('')
            self.equipment_name_labels.append(Label(self.frame1, width=15, height=1, bg='black', fg='white',
                                                    font=('Arial', 12, 'bold'), anchor='w',
                                                    textvariable=self.equipment_name_text_variables[i]))
            self.equipment_name_labels[i].place(x=100, y=30+100*i)

            self.equipment_quality_variables.append(IntVar())
            self.equipment_quality_variables[i].set(0)
            self.equipment_quality_labels.append(Label(self.frame1, width=10, bg='black', fg='black',
                                                       font=('Arial', 10, 'bold'),
                                                       textvariable=self.equipment_quality_variables[i]))
            self.equipment_quality_labels[i].place(x=100, y=60 + 100 * i)

        self.accessory_img_labels = []
        self.accessory_name_labels = []
        self.accessory_name_variables = []
        self.accessory_quality_labels = []
        self.accessory_quality_variables = []

        for i in range(5):
            self.accessory_img_labels.append(Label(self.frame1, width=64, height=64, bg='black'))
            self.accessory_img_labels[i].place(x=430, y=30+100*i)
            self.accessory_name_variables.append(StringVar())
            self.accessory_name_variables[i].set('')
            self.accessory_name_labels.append(Label(self.frame1, width=15, height=1, bg='black', fg='white',
                                                    font=('Arial', 12, 'bold'),
                                                    textvariable=self.accessory_name_variables[i], anchor='e'))
            self.accessory_name_labels[i].place(x=420, y=30+100*i, anchor='e')
            self.accessory_quality_variables.append(IntVar())
            self.accessory_quality_variables[i].set(0)
            self.accessory_quality_labels.append(Label(self.frame1, width=10, bg='black', fg='black',
                                                       font=('Arial', 10, 'bold'),
                                                       textvariable=self.accessory_quality_variables[i]))
            self.accessory_quality_labels[i].place(x=420, y=60+100*i, anchor='e')

        self.frame2 = Frame(self.notebook, width=350, height=685, bg='black')
        self.frame2.place(x=570, y=25)

        self.status = {'crt': 0, 'spc': 0, 'swf': 0, 'dom': 0, 'end': 0, 'exp': 0, 'hp': 0, 'atk': 0}
        self.tendency = {'kind': 0, 'cour': 0, 'charm': 0, 'intel': 0}

        self.bg_labels = dict()
        self.bg_labels['atk'] = Label(self.frame2, text='공격력', font=('Arial', 16, 'bold'), fg='light gray', bg='black')
        self.bg_labels['atk'].place(x=40, y=40)
        self.bg_labels['hp'] = Label(self.frame2, text='최대 생명력', font=('Arial', 16, 'bold'), fg='light gray',
                                     bg='black')
        self.bg_labels['hp'].place(x=200, y=40)
        self.bg_labels['crt'] = Label(self.frame2, text='치명', font=('Arial', 16, 'bold'), fg='light gray', bg='black')
        self.bg_labels['crt'].place(x=60, y=180)
        self.bg_labels['spc'] = Label(self.frame2, text='특화', font=('Arial', 16, 'bold'), fg='light gray', bg='black')
        self.bg_labels['spc'].place(x=60, y=230)
        self.bg_labels['swf'] = Label(self.frame2, text='신속', font=('Arial', 16, 'bold'), fg='light gray', bg='black')
        self.bg_labels['swf'].place(x=60, y=280)
        self.bg_labels['dom'] = Label(self.frame2, text='제압', font=('Arial', 16, 'bold'), fg='light gray', bg='black')
        self.bg_labels['dom'].place(x=60, y=330)
        self.bg_labels['end'] = Label(self.frame2, text='인내', font=('Arial', 16, 'bold'), fg='light gray', bg='black')
        self.bg_labels['end'].place(x=60, y=380)
        self.bg_labels['exp'] = Label(self.frame2, text='숙련', font=('Arial', 16, 'bold'), fg='light gray', bg='black')
        self.bg_labels['exp'].place(x=60, y=430)
        self.bg_labels['intel'] = Label(self.frame2, text='지성', font=('Arial', 16, 'bold'), fg='light gray', bg='black')
        self.bg_labels['intel'].place(x=50, y=560)
        self.bg_labels['cour'] = Label(self.frame2, text='담력', font=('Arial', 16, 'bold'), fg='light gray', bg='black')
        self.bg_labels['cour'].place(x=200, y=560)
        self.bg_labels['charm'] = Label(self.frame2, text='매력', font=('Arial', 16, 'bold'), fg='light gray', bg='black')
        self.bg_labels['charm'].place(x=50, y=640)
        self.bg_labels['kind'] = Label(self.frame2, text='친절', font=('Arial', 16, 'bold'), fg='light gray', bg='black')
        self.bg_labels['kind'].place(x=200, y=640)

        self.vars = dict()
        for k, v in self.status.items():
            self.vars[k] = IntVar()
            self.vars[k].set(v)
        for k, v in self.tendency.items():
            self.vars[k] = IntVar()
            self.vars[k].set(v)

        self.labels = dict()
        self.labels['atk'] = Label(self.frame2, textvariable=self.vars['atk'], font=('Arial', 16, 'bold'),
                                   fg='light gray', bg='black')
        self.labels['atk'].place(x=40, y=80)
        self.labels['atk'] = Label(self.frame2, textvariable=self.vars['hp'], font=('Arial', 16, 'bold'),
                                   fg='light gray', bg='black')
        self.labels['atk'].place(x=200, y=80)
        self.labels['crt'] = Label(self.frame2, textvariable=self.vars['crt'], font=('Arial', 16, 'bold'),
                                   fg='light gray', bg='black')
        self.labels['crt'].place(x=160, y=180)
        self.labels['spc'] = Label(self.frame2, textvariable=self.vars['spc'], font=('Arial', 16, 'bold'),
                                   fg='light gray', bg='black')
        self.labels['spc'].place(x=160, y=230)
        self.labels['swf'] = Label(self.frame2, textvariable=self.vars['swf'], font=('Arial', 16, 'bold'),
                                   fg='light gray', bg='black')
        self.labels['swf'].place(x=160, y=280)
        self.labels['dom'] = Label(self.frame2, textvariable=self.vars['dom'], font=('Arial', 16, 'bold'),
                                   fg='light gray', bg='black')
        self.labels['dom'].place(x=160, y=330)
        self.labels['end'] = Label(self.frame2, textvariable=self.vars['end'], font=('Arial', 16, 'bold'),
                                   fg='light gray', bg='black')
        self.labels['end'].place(x=160, y=380)
        self.labels['exp'] = Label(self.frame2, textvariable=self.vars['exp'], font=('Arial', 16, 'bold'),
                                   fg='light gray', bg='black')
        self.labels['exp'].place(x=160, y=430)
        self.labels['intel'] = Label(self.frame2, textvariable=self.vars['exp'], font=('Arial', 16, 'bold'),
                                     fg='light gray', bg='black')
        self.labels['intel'].place(x=120, y=560)
        self.labels['cour'] = Label(self.frame2, textvariable=self.vars['exp'], font=('Arial', 16, 'bold'),
                                    fg='light gray', bg='black')
        self.labels['cour'].place(x=270, y=560)
        self.labels['charm'] = Label(self.frame2, textvariable=self.vars['exp'], font=('Arial', 16, 'bold'),
                                     fg='light gray', bg='black')
        self.labels['charm'].place(x=120, y=640)
        self.labels['kind'] = Label(self.frame2, textvariable=self.vars['exp'], font=('Arial', 16, 'bold'),
                                    fg='light gray', bg='black')
        self.labels['kind'].place(x=270, y=640)

        self.frame3 = Frame(self.notebook, width=400, height=685)
        self.frame3.place(x=930, y=25)

        self.char_image_canvas = Canvas(self.frame3, width=340, height=685, bg='black')
        self.char_image_canvas.pack()
        # ---------------------------------------------------------------------------------------
        # 캐릭터 검색 notebook 끝
        # ---------------------------------------------------------------------------------------

        # ---------------------------------------------------------------------------------------
        # 경매장 notebook 시작
        # ---------------------------------------------------------------------------------------

        self.frame4 = Frame(self.window)
        self.frame4.pack(anchor=W, padx=10, pady=10)
        self.notebook.add(self.frame4, text="경매장")

        self.item_info_listbox = Listbox(self.frame4, width=30, height=35)
        self.item_info_listbox.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

        # 아이템과 ID 매핑
        self.items = {
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

        self.item_info = {}  # 응답 데이터를 저장할 딕셔너리

        for item in self.items.keys():
            self.item_info_listbox.insert(END, item)

        self.item_info_listbox.bind("<<ListboxSelect>>", self.show_selected_item)

        self.mapc = Canvas(self.frame4, width=1020, height=570, bg="white")
        self.mapc.grid(row=1, column=2, columnspan=2, padx=5)

        # 이메일 발송을 위한 버튼 제작 (2024.06.07)
        self.email_button = Button(self.frame4, text='이메일 전송', font=('Arial', 16, 'bold'), bg='white',
                                   command=self.email_b_pressed)
        self.email_button.grid(row=2, column=1)
        self.email_button['state'] = 'disable'

        # ---------------------------------------------------------------------------------------
        # 경매장 notebook 끝
        # ---------------------------------------------------------------------------------------
        # ---------------------------------------------------------------------------------------
        # pc방 notebook 시작
        # ---------------------------------------------------------------------------------------
        self.frame5 = Frame(self.window)
        self.frame5.pack(side=LEFT, anchor=W, padx=10, pady=10)
        self.notebook.add(self.frame5, text="pc방 검색")

        self.search_geo = Entry(self.frame5, width=30)  # 지역 검색창 entry
        self.search_geo.grid(row=0, column=0, padx=5, pady=5)

        self.geo_button = Button(self.frame5, text="검색", command=self.search_pc_room)  # 지역 검색 버튼
        self.geo_button.grid(row=0, column=1, padx=5, pady=5)

        self.pc_info = Listbox(self.frame5, width=60, height=35)  # pc방 정보를 보여주는 listbox
        self.pc_info.grid(row=1, column=0, columnspan=2, padx=5, pady=10)
        self.pc_info.bind("<<ListboxSelect>>", self.on_pc_info_select)

        self.map_widget = TkinterMapView(self.frame5, width=800, height=720, corner_radius=0)
        self.map_widget.grid(row=1, column=3, padx=10, pady=10, sticky=NSEW)

        # ---------------------------------------------------------------------------------------
        # pc방 notebook 끝
        # ---------------------------------------------------------------------------------------
        # ---------------------------------------------------------------------------------------
        # 텔레그램 봇 시작
        # ---------------------------------------------------------------------------------------
        telegram_thread = threading.Thread(target=self.start_telegram_bot())
        telegram_thread.daemon=True
        telegram_thread.start()


        self.window.mainloop()

    def start_telegram_bot(self):
        try:
            bot = TelegramBot()
        except Exception as e:
            print(f"Error in Telegram bot: {e}")
            traceback.print_exc()
    # 유저 이름 받기
    def get_name(self):
        self.name = str(self.name_var.get())
        profile = get_profiles(self.name)
        equipment = get_equipment(self.name)

        if profile is None:
            print('No User Exist')
            return

        img = url2PhotoImage(profile['image_url'])
        temp_label = Label(self.frame3, image=img)
        temp_label.image = img
        self.char_image_canvas.delete('img')
        self.char_image_canvas.create_image(185, 330, image=img, tags='img')

        self.status = profile['status']
        self.tendency = profile['tendency']

        for k, v in self.status.items():
            self.vars[k].set(v)
        for k, v in self.tendency.items():
            self.vars[k].set(v)

        if equipment is None:
            return

        color_dict = {'희귀': 'sky blue',
                      '영웅': 'violet',
                      '전설': 'gold',
                      '유물': 'OrangeRed2',
                      '고대': 'yellow',
                      '에스더': 'cyan',
                      }

        for i in range(6):
            icon_url = equipment[i]['icon']
            img = url2PhotoImage(icon_url)
            reforge = equipment[i]['reforge']
            grade = equipment[i]['grade']
            name = equipment[i]['type']
            quality = int(equipment[i]['quality'])
            temp_label = Label(self.frame1, image=img)
            temp_label.image = img

            if grade not in color_dict.keys():
                bg_color = 'black'
            else:
                bg_color = color_dict[grade]

            self.equipment_img_labels[i].configure(image=img, bg=bg_color)
            text = str(reforge)+' '+str(grade)+' '+str(name)
            self.equipment_name_text_variables[i].set(text)
            if quality <= 10:
                color = 'red'
            elif quality < 30:
                color = 'orange'
            elif quality < 70:
                color = 'green'
            elif quality < 90:
                color = 'blue'
            elif quality < 100:
                color = 'purple'
            else:
                color = 'gold'
            self.equipment_quality_variables[i].set(quality)
            self.equipment_quality_labels[i].configure(bg=color, fg='white')

        for i in range(6, 6+5):
            icon_url = equipment[i]['icon']
            img = url2PhotoImage(icon_url)
            reforge = equipment[i]['reforge']
            grade = equipment[i]['grade']
            name = equipment[i]['type']
            quality = int(equipment[i]['quality'])
            temp_label = Label(self.frame1, image=img)
            temp_label.image = img

            if grade not in color_dict.keys():
                bg_color = 'black'
            else:
                bg_color = color_dict[grade]

            j = i - 6
            self.accessory_img_labels[j].configure(image=img, bg=bg_color)
            if name[-1] == '1':
                name = name[:-1]
            text = str(reforge) + ' ' + str(grade) + ' ' + str(name)
            self.accessory_name_variables[j].set(text)
            if quality <= 10:
                color = 'red'
            elif quality < 30:
                color = 'orange'
            elif quality < 70:
                color = 'green'
            elif quality < 90:
                color = 'blue'
            elif quality < 100:
                color = 'purple'
            else:
                color = 'gold'
            self.accessory_quality_variables[j].set(quality)
            self.accessory_quality_labels[j].configure(bg=color, fg='white')

    # 아이템 정보 표시
    def draw_info(self, item_id):
        url = "https://developer-lostark.game.onstove.com/markets/items/" + item_id
        response = requests.get(url, headers=headers)
        data = response.json()
        price_by_day = data[0]["Stats"]
        price = {}
        self.mapc.delete("all")

        for day in range(7):
            price[price_by_day[day]["Date"]] = float(price_by_day[day]["AvgPrice"])

        max_price = max(price.values())
        min_price = min(price.values())
        price_range = max_price - min_price

        width = 1020
        height = 570
        x_spacing = width / 8  # 공간을 나누기 위해 8로 나눔
        y_offset = 500  # 그래프의 y 축 기준선
        i = 0

        previous_x, previous_y = None, None

        for date, avg_price in sorted(price.items()):
            x = x_spacing * (i + 1)

            normalized_price = (avg_price - min_price) / price_range if price_range != 0 else 0
            heightspot = normalized_price * height * 0.3
            y = y_offset - heightspot

            # 날짜를 캔버스 아래에 표시
            self.mapc.create_text(x, y_offset + 20, text=date, anchor=N, fill="black")  # 날짜 표시
            # 가격을 캔버스 세로로 표시
            self.mapc.create_text(x, y - 20, text=f"{avg_price:.2f}", anchor=S, fill="black")  # 가격 표시
            self.mapc.create_oval(x - 5, y - 5, x + 5, y + 5, fill="orange")  # 지름 10짜리 원

            if previous_x is not None and previous_y is not None:
                self.mapc.create_line(previous_x, previous_y, x, y, fill="orange")  # 이전 점과 현재 점을 선으로 연결

            previous_x, previous_y = x, y
            i += 1

    # 선택된 아이템 표시
    def show_selected_item(self, event):
        selected_index = self.item_info_listbox.curselection()
        if selected_index:
            selected_item = self.item_info_listbox.get(selected_index)
            item_id = self.items[selected_item]
            self.draw_info(item_id)
            # 인덱스 선택시 이메일 버튼 활성화
            self.email_button['state'] = 'active'

    def search_pc_room(self):
        map_url = "https://dapi.kakao.com/v2/local/search/keyword.json"
        map_headers = {"Authorization": "KakaoAK 846ccd607715f559334168534f07d9ef"}
        region = self.search_geo.get() + " pc방"
        params = {"query": region}
        response = requests.get(map_url, params=params, headers=map_headers)

        if response.status_code == 200:
            data = response.json()
            self.pc_info.delete(0, END)  # 기존 목록 삭제
            self.places = data['documents']
            for place in self.places:
                name = place['place_name']
                self.pc_info.insert(END, name)  # 이름을 리스트 박스에 추가
        else:
            print("검색에 실패했습니다.")

    def on_pc_info_select(self, event):
        selected_index = self.pc_info.curselection()
        if selected_index:
            selected_index = selected_index[0]
            selected_place = self.places[selected_index]
            self.display_pc_room_info(selected_place)

    def display_pc_room_info(self, place):
        x = float(place['x'])
        y = float(place['y'])
        self.map_widget.set_position(y, x)
        self.map_widget.set_zoom(15)
        self.map_widget.delete_all_marker()
        self.map_widget.set_marker(y, x, text=place['place_name'])

    # 이메일 버튼 눌림
    def email_b_pressed(self):
        selected_index = self.item_info_listbox.curselection()
        if selected_index:
            selected_item = self.item_info_listbox.get(selected_index)
            # 캔버스 -> 이미지 파일로
            x = self.window.winfo_rootx() + self.mapc.winfo_x()
            y = self.window.winfo_rooty() + self.mapc.winfo_y()
            x1 = x + self.mapc.winfo_width()
            y1 = y + self.mapc.winfo_height()
            filename = 'graph.png'
            ImageGrab.grab().crop((x, y, x1, y1)).save(filename)
            print(f'이미지 저장: \'{filename}\'')
            receiver = 'ahw8670@naver.com'
            suc = send_email(receiver, str(selected_item)+' 그래프', str(selected_item))
            if suc:
                print('이메일이 성공적으로 보내졌습니다.')
        else:
            print('에러: 선택된 아이템이 없습니다!')


if __name__ == "__main__":
    mainGUI()

