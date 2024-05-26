from tkinter import *
from url_to_tkPhotoImage import url2PhotoImage
from getAPIs import *


class MainGUI:
    def __init__(self):
        window = Tk()
        window.title('여기에 제목 입력')
        window.geometry('1280x720')

        frame0 = Frame(window, width=400, height=40, bg='gray')
        frame0.place(x=10, y=10)

        # 캐릭터의 이름을 입력할 Entry와 이름을 저장하고 있을 Variable
        self.name_var = StringVar()
        ent = Entry(frame0, width=44, textvariable=self.name_var, relief='solid', borderwidth=10)
        ent.place(x=0, y=0)

        self.name = ''
        # 캐릭터의 이름을 받아올 버튼
        button = Button(frame0, text='검색', bg='white', foreground='black', width=9, height=2, command=self.get_name)
        button.place(x=330)

        self.frame1 = Frame(window, width=400, height=650, bg='black')
        self.frame1.place(x=10, y=60)

        # img1 = PhotoImage(file='gn_f_item_182.png')

        lab1 = Label(self.frame1, width=64, height=64, bg='black')
        lab1.place(x=10, y=30)
        lab2 = Label(self.frame1, width=64, height=64, bg='black')
        lab2.place(x=10, y=130)
        lab3 = Label(self.frame1, width=64, height=64, bg='black')
        lab3.place(x=10, y=230)
        lab4 = Label(self.frame1, width=64, height=64, bg='black')
        lab4.place(x=10, y=330)
        lab5 = Label(self.frame1, width=64, height=64, bg='black')
        lab5.place(x=10, y=430)
        lab6 = Label(self.frame1, width=64, height=64, bg='black')
        lab6.place(x=10, y=530)

        self.frame2 = Frame(window, width=350, height=700, bg='black')
        self.frame2.place(x=420, y=10)

        self.status = {'crt': 0, 'spc': 0, 'swf': 0, 'dom': 0, 'end': 0, 'exp': 0, 'hp': 0, 'atk': 0}
        self.tendency = {'kind': 0, 'cour': 0, 'charm': 0, 'intel': 0}

        self.bg_labels = dict()
        self.bg_labels['atk'] = Label(self.frame2, text='공격력', font=('Arial', 16, 'bold'), fg='light gray', bg='black')
        self.bg_labels['atk'].place(x=40, y=40)
        self.bg_labels['hp'] = Label(self.frame2, text='최대 생명력', font=('Arial', 16, 'bold'), fg='light gray', bg='black')
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

        self.frame3 = Frame(window, width=490, height=700)
        self.frame3.place(x=780, y=10)

        self.char_image_canvas = Canvas(self.frame3, width=490, height=700, bg='black')
        self.char_image_canvas.pack()

        window.mainloop()

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
        self.char_image_canvas.create_image(245, 350, image=img, tags='img')

        self.status = profile['status']
        self.tendency = profile['tendency']

        for k, v in self.status.items():
            self.vars[k].set(v)
        for k, v in self.tendency.items():
            self.vars[k].set(v)


MainGUI()
