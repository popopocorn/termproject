from tkinter import *
from tkinter import font
from winsound import *
import random
import deck_check
from Card import *


class MainGUI:
    def __init__(self):
        self.window = Tk()
        self.window.title('도리짓고땡')
        self.window.geometry('800x600')
        self.window.configure(bg='green')
        self.font = font.Font(self.window, size=20, weight='bold', family='Consolas')
        self.font2 = font.Font(self.window, size=14, weight='bold', family='Consolas')
        self.p1 = dict()
        self.p2 = dict()
        self.p3 = dict()
        self.d = dict()
        self.sys = dict()
        self.turn = 0

        self.deck = []
        for i in range(1, 10 + 1):
            for j in range(1, 4 + 1):
                self.deck.append(Card(i, PhotoImage(file='GodoriCards/{0}.{1}.gif'.format(i, j))))
        for i in range(0, 8, 28):
            self.deck[i].light = True

        random.shuffle(self.deck)
        self.curr = 0
        self.flipped_img = PhotoImage(file='GodoriCards/cardback.gif')

        self.setupButton()
        self.setupLabel()
        self.Init()

        self.window.mainloop()

    def setupButton(self):
        self.p1['b'] = list()
        self.p1['b'].append(Button(self.window, text='5만', width=4, height=1, font=self.font2,
                                   command=lambda: self.betPressed(1, 5)))
        self.p1['b'].append(Button(self.window, text='1만', width=4, height=1, font=self.font2,
                                   command=lambda: self.betPressed(1, 1)))
        self.p1['b'][0].place(x=30, y=550)
        self.p1['b'][1].place(x=100, y=550)

        self.p2['b'] = list()
        self.p2['b'].append(Button(self.window, text='5만', width=4, height=1, font=self.font2,
                                   command=lambda: self.betPressed(2, 5)))
        self.p2['b'].append(Button(self.window, text='1만', width=4, height=1, font=self.font2,
                                   command=lambda: self.betPressed(2, 1)))
        self.p2['b'][0].place(x=230, y=550)
        self.p2['b'][1].place(x=300, y=550)

        self.p3['b'] = list()
        self.p3['b'].append(Button(self.window, text='5만', width=4, height=1, font=self.font2,
                                   command=lambda: self.betPressed(3, 5)))
        self.p3['b'].append(Button(self.window, text='1만', width=4, height=1, font=self.font2,
                                   command=lambda: self.betPressed(3, 1)))
        self.p3['b'][0].place(x=430, y=550)
        self.p3['b'][1].place(x=500, y=550)

        self.sys['deal'] = Button(self.window, text='Deal', width=6, height=1, font=self.font2,
                                  command=self.dealPressed)
        self.sys['deal'].place(x=600, y=550)
        self.sys['again'] = Button(self.window, text='Again', width=6, height=1, font=self.font2,
                                   command=self.againPressed)
        self.sys['again'].place(x=700, y=550)

    def setupLabel(self):
        temp = PhotoImage()
        bg = 'lime'
        fg = 'white'
        self.p1['lc'] = list()
        self.p2['lc'] = list()
        self.p3['lc'] = list()
        self.d['lc'] = list()
        self.p1['ls'] = list()
        self.p2['ls'] = list()
        self.p3['ls'] = list()
        self.d['ls'] = list()
        self.p1['vs'] = list()
        self.p2['vs'] = list()
        self.p3['vs'] = list()
        self.d['vs'] = list()
        for n in range(5):
            for p in [self.p1, self.p2, self.p3, self.d]:
                p['lc'].append(Label(self.window, width=64, height=100, bg=bg, image=temp))
                p['lc'][-1].lower()
                p['vs'].append(StringVar())
                p['ls'].append(Label(self.window, width=2, bg=bg, font=self.font2, fg=fg, textvariable=p['vs'][n]))

            self.p1['lc'][n].place(x=20 + n*20, y=400)
            self.p2['lc'][n].place(x=220 + n*20, y=400)
            self.p3['lc'][n].place(x=420 + n*20, y=400)
            self.d['lc'][n].place(x=220 + n*20, y=150)

            self.p1['ls'][n].place(x=10 + n*35, y=370)
            self.p2['ls'][n].place(x=210 + n * 35, y=370)
            self.p3['ls'][n].place(x=410 + n * 35, y=370)
            self.d['ls'][n].place(x=210 + n * 35, y=120)

        for p in [self.p1, self.p2, self.p3]:
            p['vb'] = StringVar()
            p['lb'] = Label(self.window, width=6, height=1, font=self.font, fg='gold', textvariable=p['vb'], bg=bg)
            p['vr'] = StringVar()
            p['lr'] = Label(self.window, width=18, font=self.font2, fg='cyan', textvariable=p['vr'], bg=bg, anchor='w')
            p['vw'] = StringVar()
            p['lw'] = Label(self.window, width=3, font=self.font, fg='red', textvariable=p['vw'], bg=bg, anchor='w')

        self.sys['moneyVar'] = StringVar()
        self.sys['moneyLabel'] = Label(self.window, width=8, height=1, font=self.font, fg='gold',
                                       textvariable=self.sys['moneyVar'], bg=bg, anchor='e')
        self.p1['lb'].place(x=50, y=505)
        self.p2['lb'].place(x=250, y=505)
        self.p3['lb'].place(x=450, y=505)

        self.d['vr'] = StringVar()
        self.d['lr'] = Label(self.window, width=18, font=self.font2, fg='cyan',
                             textvariable=self.d['vr'], bg=bg, anchor='w')
        self.p1['lr'].place(x=10, y=340)
        self.p2['lr'].place(x=210, y=340)
        self.p3['lr'].place(x=410, y=340)
        self.d['lr'].place(x=210, y=90)

        self.p1['lw'].place(x=10, y=300)
        self.p2['lw'].place(x=210, y=300)
        self.p3['lw'].place(x=410, y=300)

        self.sys['moneyLabel'].place(x=650, y=505)

    def labelRefresh(self):
        self.p1['vb'].set(str(self.p1['bet'])+'만')
        self.p2['vb'].set(str(self.p2['bet'])+'만')
        self.p3['vb'].set(str(self.p3['bet'])+'만')
        self.sys['moneyVar'].set(str(self.sys['money'])+'만')
        pass

    def Init(self):
        self.p1['bet'] = 0
        self.p2['bet'] = 0
        self.p3['bet'] = 0
        self.sys['money'] = 1000
        self.p1['hand'] = list()
        self.p2['hand'] = list()
        self.p3['hand'] = list()
        self.d['hand'] = list()
        self.buttonControl(0, 0)
        self.buttonControl(1, 1)
        self.buttonControl(2, 0)
        self.labelRefresh()

    def betPressed(self, p, n):
        PlaySound('sounds/chip.wav', SND_FILENAME | SND_ASYNC)
        self.buttonControl(1, 1)
        if p == 1:
            print(f'p1 {n}만 pressed. ')
        elif p == 2:
            print(f'p2 {n}만 pressed. ')
        else:
            print(f'p3 {n}만 pressed. ')

    def dealPressed(self):
        print('Deal pressed. ')
        if self.turn == 0:
            self.buttonControl(0, 1)
            self.buttonControl(1, 0)
            PlaySound('sounds/cardFlip1.wav', SND_FILENAME | SND_ASYNC)
            for obj in (self.p1, self.p2, self.p3):
                obj['hand'].append(self.deck[self.curr])
                self.curr += 1
                obj['lc'][0].configure(image=obj['hand'][0].img)
                obj['vs'][0].set(str(obj['hand'][0].score))

            self.d['hand'].append(self.deck[self.curr])
            self.curr += 1
            self.d['lc'][0].configure(image=self.flipped_img)

            self.turn += 1
        elif self.turn == 1:
            self.buttonControl(1, 0)
            for i in range(1, 4):
                PlaySound('sounds/cardFlip1.wav', SND_FILENAME | SND_ASYNC)
                for obj in (self.p1, self.p2, self.p3):
                    obj['hand'].append(self.deck[self.curr])
                    self.curr += 1
                    obj['lc'][i].configure(image=obj['hand'][i].img)
                    obj['lc'][i].image = obj['hand'][i].img
                    obj['vs'][i].set(str(obj['hand'][i].score))
                self.d['hand'].append(self.deck[self.curr])
                self.curr += 1
                self.d['lc'][i].configure(image=self.flipped_img)
            self.turn += 1
        elif self.turn == 2:
            PlaySound('sounds/cardFlip1.wav', SND_FILENAME | SND_ASYNC)
            self.buttonControl(0, 0)
            self.buttonControl(1, 0)
            self.buttonControl(2, 1)
            for obj in (self.p1, self.p2, self.p3):
                obj['hand'].append(self.deck[self.curr])
                self.curr += 1
                obj['lc'][4].configure(image=obj['hand'][4].img)
                obj['vs'][4].set(str(obj['hand'][4].score))

            self.d['hand'].append(self.deck[self.curr])
            self.curr += 1
            for lc, h, vs in zip(self.d['lc'], self.d['hand'], self.d['vs']):
                lc.configure(image=h.img)
                vs.set(h.score)

            # 승패 판정
            for p in [self.p1, self.p2, self.p3, self.d]:
                score = deck_check.check_point(p['hand'])
                # if score is not None:
                #     p['vr'].set(score[1])
                # else:
                #     p['vr'].set('노메이드')

            PlaySound('sounds/win.wav', SND_FILENAME | SND_ASYNC)
            self.turn += 1
        else:
            print('ERROR: turn 이 0, 1, 2가 아닌데 dealPressed() 호출됨')

    def againPressed(self):
        print('Again pressed')
        if self.turn == 3:
            PlaySound('sounds/ding.wav', SND_FILENAME | SND_ASYNC)
            self.buttonControl(0, 0)
            self.buttonControl(1, 1)
            self.buttonControl(2, 0)
            temp = PhotoImage()
            for i in range(5):
                self.p1['lc'][i].configure(image=temp)
                self.p2['lc'][i].configure(image=temp)
                self.p3['lc'][i].configure(image=temp)
                self.d['lc'][i].configure(image=temp)
                self.p1['vs'][i].set('')
                self.p2['vs'][i].set('')
                self.p3['vs'][i].set('')
                self.d['vs'][i].set('')

            self.labelRefresh()
            # 초기화
            random.shuffle(self.deck)
            self.curr = 0
            self.p1['hand'].clear()
            self.p2['hand'].clear()
            self.p3['hand'].clear()
            self.labelRefresh()
            self.turn = 0
        else:
            print('ERROR: turn 이 3이 아닌데 againPressed() 호출됨')

    def buttonControl(self, index, state):
        if state == 0:
            state = 'disable'
        else:
            state = 'active'

        if index == 0:
            for n in range(2):
                self.p1['b'][n]['state'] = state
                self.p2['b'][n]['state'] = state
                self.p3['b'][n]['state'] = state
        elif index == 1:
            self.sys['deal']['state'] = state
        elif index == 2:
            self.sys['again']['state'] = state


MainGUI()
