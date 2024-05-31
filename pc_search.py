from tkinter import *
from tkinter import ttk
import pandas as pd
import numpy as np
import folium
from folium.plugins import MiniMap
import requests

class GUI:
    def __init__(self):
        self.window = Tk()
        self.window.title("Termproject")
        self.window.geometry("1280x720")

        self.frame2 = Frame(self.window)
        self.frame2.pack(anchor=W, padx=10, pady=10)

        self.search_geo = Entry(self.frame2, width=30)  # 지역 검색창 entry
        self.search_geo.grid(row=0, column=0, padx=5, pady=5)

        self.geo_button = Button(self.frame2, text="검색", command=self.search_pc_room)  # 지역 검색 버튼
        self.geo_button.grid(row=0, column=1, padx=5, pady=5)

        self.pc_info = Listbox(self.frame2, width=60, height=35)  # pc방 정보를 보여주는 listbox
        self.pc_info.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

        # 임시 리스트 항목 추가


        self.favorite_button = Button(self.frame2, text="즐겨찾기", command=self.add_to_favorites)  # 즐겨찾기 버튼
        self.favorite_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        self.mapc = Canvas(self.frame2, width=1020, height=570, bg="black")
        self.mapc.grid(row=1, column=2, columnspan=2, padx=5)

        self.window.mainloop()

    def search_pc_room(self):
        url = "https://dapi.kakao.com/v2/local/search/keyword.json"
        map_headers = {"Authorization": "KakaoAK 846ccd607715f559334168534f07d9ef"}
        region = self.search_geo.get() + " pc방"
        params = {"query": region}
        response = requests.get(url, params=params, headers=map_headers)

        if response.status_code == 200:
            data = response.json()
            self.pc_info.delete(0, END)  # 기존 목록 삭제
            for place in data['documents']:
                name = place['place_name']
                self.pc_info.insert(END, name)  # 이름을 리스트 박스에 추가
        else:
            print("검색에 실패했습니다.")
    def add_to_favorites(self):
        selected_index = self.pc_info.curselection()
        if selected_index:
            selected_item = self.pc_info.get(selected_index)
            print(f"{selected_item}를 즐겨찾기를 완료했습니다.")
        else:
            print("선택된 항목이 없습니다.")

if __name__ == "__main__":
    w = GUI()