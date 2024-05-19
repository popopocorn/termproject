from tkinter import *
import requests
import json
from lostark_api_token import Token

headers = {
    "accept": "application/json",
    "authorization": Token
}

class GUI:
    def __init__(self):
        self.window = Tk()
        self.window.title("Termproject")
        self.window.geometry("1280x720")

        self.frame3 = Frame(self.window)
        self.frame3.pack(anchor=W, padx=10, pady=10)

        self.item_info_listbox = Listbox(self.frame3, width=30, height=35)
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

        self.mapc = Canvas(self.frame3, width=1020, height=570, bg="white")
        self.mapc.grid(row=1, column=2, columnspan=2, padx=5)

        self.window.mainloop()

    def draw_info(self, item_id):
        url = "https://developer-lostark.game.onstove.com/markets/items/" + item_id
        response = requests.get(url, headers=headers)
        data = response.json()
        price_by_day = data[0]["Stats"]
        price={}
        self.mapc.delete("all")
        for day in range(7):
            price[price_by_day[day]["Date"]] = price_by_day[day]["AvgPrice"]

        x = 50
        y = 50
        for date, avg_price in price.items():
            text = f"{date}: {avg_price}"  # 표시할 텍스트 내용
            self.mapc.create_text(x, y, text=text, anchor=W)  # 텍스트를 캔버스에 그림
            y += 20
    def show_selected_item(self, event):
        selected_index = self.item_info_listbox.curselection()
        if selected_index:
            selected_item = self.item_info_listbox.get(selected_index)
            item_id = self.items[selected_item]
            print(f"선택된 항목: {selected_item}")
            self.draw_info(item_id)

w = GUI()
