# -*- encoding: utf-8 -*-
# ----------------------------------------------------------------------------
# Enriching
# Based on the game show project by Vladimir Khil aka Ur-Quan
# Copyright © 2020 Sergey Chernov aka Gamer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------------

import codecs
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from random import randint
from random import choice
from random import randrange
from threading import Timer
from enum import Enum
buzzer = []
player = [] #поле для ввода имён игроков
start_names = [] #переменные с именами игроков
player_term = [None, None]
active = 0
players = [] # record'ы игроков
Klausimai = []
varianty = []
knopki = []
eax = []
golosov = []
skem_knopka = []
rr_button = []
danger = []
bong_buttons = []
kto_nazhal = None
root = tk.Tk()
var_ready = []
root.geometry("900x900")
termotvet = tkinter.StringVar()
stagegong = None
q_number = 0 #0
happy_variant  = None
otv = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
money = [3000, 9000, 15000, 30000, 90000, 150000, 300000, 900000, 1500000, 3000000]
termmoney = [4000, 16000, 80000, 400000]
zaideju_vardai = []
zaideju_pinigai = []
maximal = []
parodytas_klausimas = tk.Label(root, justify = tkinter.CENTER, bg="#cfcfcf", wraplength = 380)
#vote = []
index_term = None
bong_stopped = None
class term(Enum):
    default = 0
    random_pick = 1
    ready = 2
    pressed = 3
    after = 4

class bongstage(Enum):
    before = 0
    inprogress = 1
    stopped = 2
    finish = 3
    after = 4

class priem(Enum):
    do = 0
    otveti = 1
    vse = 2

TermQ = []
_3579 = term.default
_otveti = priem.do

qterm = codecs.open ('qbaset.txt', 'r', "utf_8_sig")  # stage+1
for line in qterm:
    xi = {}
    HUH = line.rstrip("\n")
    xi["Q"] = HUH
    xi["A"] = list(map(str, qterm.readline().split()))
    test = []
    TermQ.append(xi)
qterm.close()


def udacha(iok):
    global rr_button
    if (iok in danger):
        tkinter.messagebox.showinfo("Вам не повезло", aux_list[loser]["name"]+' покидает игру')
        log.write(aux_list[loser]["name"]+' покидает игру с выигрышем '+str(aux_list[loser]['sgor']+aux_list[loser]['nesgor'])+'\n')
        aux_list.pop(loser)
    else:
        tkinter.messagebox.showinfo("Вам повезло!", aux_list[loser]["name"]+' остаётся в игре')
        log.write(aux_list[loser]["name"] + ' остаётся в игре' + '\n')
    rr_button = []
    roulette.grab_release()
    roulette.withdraw()
    show(q_number)


def russian_roulette(y):
    global roulette, rr_button, danger
    roulette = tk.Toplevel(root)
    rr_button = []
    danger = []
    roulette.protocol('WM_DELETE_WINDOW', noway)
    for tf in range((q_number-1)//2):
        while True:
            ou = randint(0, 4)
            if (ou not in danger):
                danger.append(ou)
                break
    #print(danger) #для отладки
    for a in range(5):
        smd = tk.Button(roulette, text = "Испытайте удачу", command = lambda rsrs = a: udacha(rsrs))
        rr_button.append(smd)
        rr_button[a].pack(side=tk.LEFT)
    roulette.grab_set()



def accepted_in_terminator(*args):
    global _3579
    global kto_nazhal, loser
    otvet = str(termotvet.get())
    log.write ("Игрок даёт ответ "+otvet+'\n')
    no_spaces = otvet.replace(" ", "")
    no_sp_lower = no_spaces.lower()
    if (no_sp_lower == TermQ[index_term]["A"][0]):
        tkinter.messagebox.showinfo("Верно!", "Поздравляю, ответ правильный!")
        log.write("Это верный ответ" + '\n')
    elif (no_sp_lower in TermQ[index_term]["A"]):
        tkinter.messagebox.showinfo("Верно!", "Правильный ответ - " + TermQ[index_term]["A"][0])
        log.write("Это верный ответ (" + TermQ[index_term]["A"][0] + ')' + '\n')
    else:
        tkinter.messagebox.showinfo("Неверно!", "Ошибка! Правильный ответ - " + TermQ[index_term]["A"][0])
        log.write("Это неверный ответ. Правильный ответ - " + TermQ[index_term]["A"][0] + '\n')
    if ((kto_nazhal == 0) and (no_sp_lower in TermQ[index_term]["A"])) or (
            (kto_nazhal == 1) and not (no_sp_lower in TermQ[index_term]["A"])):
        winner = player_term[0]
        loser = player_term[1]
    elif ((kto_nazhal == 1) and (no_sp_lower in TermQ[index_term]["A"])) or (
            (kto_nazhal == 0) and not (no_sp_lower in TermQ[index_term]["A"])):
        winner = player_term[1]
        loser = player_term[0]
    aux_list[winner]["sgor"], aux_list[loser]["sgor"] = (aux_list[winner]["sgor"] + aux_list[loser][
        "sgor"]), 0
    #zomg teh hindu code
    for s in range(len(aux_list)):
        zaideju_pinigai[s]['text'] = str(aux_list[s]['sgor']) + ' + ' + str(aux_list[s]['nesgor']) + ' = ' + str(
            aux_list[s]['sgor'] + aux_list[s]['nesgor']) + '\n'
    # for z in range(len(IgrokiDummy)):
    #     print(str(IgrokiDummy[z]["Name"]) + ': ' + str(IgrokiDummy[z]["Sgor"] + IgrokiDummy[z]["Nesgor"]) + '(' + str(
    #         IgrokiDummy[z]["Share"]) + ')')
    Terminator_Question.place_forget()
    buzzer[0]["bg"] = "#cccccc"
    buzzer[1]["bg"] = "#cccccc"
    buzzer[0].place_forget()
    buzzer[1].place_forget()
    TermQ.pop(index_term)
    termotvet.set = ''
    vvod.place_forget()
    _3579 = term.default
    kto_nazhal = None
    russian_roulette(loser)
    # stage+=1
    pass #дописать


def answer(l):
    golosov[l]+=((aux_list[active-1]['sgor'])+(aux_list[active-1]['nesgor']))
    eax[l]["text"] = str(int(eax[l]["text"])+(aux_list[active-1]['sgor'])+(aux_list[active-1]['nesgor']))
    aux_list[active-1]['vote'] = l+1
    log.write (aux_list[active-1]['name']+' - '+Klausimai[r]['A'][l]+ '\n')
    for a in range(otv[q_number - 1]):
        knopki[a]["state"] = "disabled"
    root.lop = root.after(1000, ko)

def doSomething():
    if tk.messagebox.askyesno("Exit", "Do you want to quit the application?"):
        log.close()
        root.destroy()

def noway():
    tkinter.messagebox.showinfo("Окно закрыть пока нельзя")

def next():
    global active, stagegong, bong_summa_index, bong_stopped, bong_summa, happy_variant
    #active+=1
    stagegong = bongstage.before
    happy_variant = randint(0, 2)
    #print(happy_variant+1)
    bong_stopped = False
    bong_summa_index = -1
    while True:
        active+=1
        if (active>=len(aux_list)):
            tkinter.messagebox.showinfo("Всё", "Игра окончена!")
            log.write("Игра окончена")
            break
        elif (aux_list[active]["sgor"]>0):
            break
    if (active < len(aux_list)):
        tkinter.messagebox.showinfo(aux_list[active]["name"], "Играйте в гонг-игру!")
        bong_summa["text"] = "0"
        bong_stop["text"] = "Стоп"
        for a in range(len(bong_buttons)):
            bong_buttons[a]["state"] = "normal"
    else:
        tkinter.messagebox.showinfo("Конец", "Игра окончена")
        for a in range(len(bong_buttons)):
            bong_buttons[a].place_forget()
        bong_stop.place_forget()
        bong_summa.place_forget()

    #dopisat



def auxiliary_function():
    global active
    active+=1
    reshenie(active)

def goon(w):
    nuspresti.grab_release()
    nuspresti.withdraw()
    auxiliary_function()

def cash(w):
    global who_walks_away
    nuspresti.grab_release()
    nuspresti.withdraw()
    log.write(aux_list[w]['name']+' забирает '+str(aux_list[w]['sgor'] + aux_list[w]['nesgor']) + '\n')
    who_walks_away.append(w)
    zaideju_pinigai[w]['text'] = ' '
    zaideju_vardai[w]['text'] = ' '
    auxiliary_function()


def chair(w):
    nuspresti.grab_release()
    nuspresti.withdraw()
    log.write(aux_list[w]['name'] + ' стабилизирует выигрыш' + '\n')
    aux_list[w]['sgor'], aux_list[w]['nesgor'] = aux_list[w]['sgor']//2, aux_list[w]['nesgor']+(aux_list[w]['sgor']//2)
    aux_list[w]['stab_can'] = False
    zaideju_pinigai[w]['text'] = str(aux_list[w]['sgor']) + ' + ' + str(aux_list[w]['nesgor']) + ' = ' + str(
        aux_list[w]['sgor'] + aux_list[w]['nesgor']) + '\n'
    auxiliary_function()


def onKeyPress(event):
    global kto_nazhal, _3579
    if not (_3579 == term.ready):
        pass
    elif not (event.char in set ('AaLlфФдД')):
        pass
    else:
        if (event.char in set('AaфФ')):
            buzzer[0]["bg"]="#ff0000"
            kto_nazhal = 0
        elif (event.char in set('LlдД')):
            buzzer[1]["bg"]="#ff0000"
            kto_nazhal = 1
        log.write('Кнопку нажимает '+aux_list[player_term[kto_nazhal]]["name"]+'\n')
        _3579 = term.pressed
        vvod.place(relx=0.5, rely = 0.5)
        vvod.focus_set()
        #print('Got key press: ', event.char)


def terminator(samsung):
    global index_term, _3579
    player_term[1]=samsung
    log.write(' и выбирает в соперники '+aux_list[player_term[1]]["name"]+'\n')
    index_term = randint(0, len(TermQ) - 1)
    for ij in range(len(skem_knopka)):
        skem_knopka[ij].pack_forget()
    for a in range(2):
        b = tk.Label(text=aux_list[player_term[a]]["name"])
        buzzer.append(b)
    for a in range(2):
        buzzer[a].place (relx = 0.4+0.3*a, rely = 0.3)
        buzzer[a]["bg"] = "#cccccc"
        buzzer[a]["text"] = aux_list[player_term[a]]["name"]
    global Terminator_Question
    Terminator_Question = tk.Label(text=TermQ[index_term]["Q"])
    Terminator_Question.place(relx=0.1, rely=0.85)
    skem.grab_release()
    skem.withdraw()
    log.write("Вопрос терминатора: " + TermQ[index_term]["Q"] + '\n')
    _3579 = term.ready


def term_choose():
    root.after_cancel(term_choose)
    global schetchik
    schetchik -=1
    global active_term
    active_term = randrange(len(aux_list))
    root.title(aux_list[active_term]["name"])
    if (schetchik ==0 ):
        root.title('tk')
        skem_knopka = []
        log.write('Терминатор выбрал '+aux_list[active_term]["name"]+'\n')
        if tkinter.messagebox.askyesno(aux_list[active_term]["name"], 'будете ли вы играть в терминатор?'):
            player_term[0] = active_term
            aux_list[active_term]['nesgor'] += termmoney[(q_number-3)//2]
            zaideju_pinigai[active_term]['text'] = str(aux_list[active_term]['sgor']) + ' + ' + str(aux_list[active_term]['nesgor']) + ' = ' + str(
                aux_list[active_term]['sgor'] + aux_list[active_term]['nesgor']) + '\n'
            log.write(aux_list[active_term]["name"]+' берёт '+str(termmoney[(q_number-3)//2]))
            global skem
            skem = tk.Toplevel(root)
            skem.protocol('WM_DELETE_WINDOW', noway)
            skem.title(aux_list[active_term]["name"]+ ', с кем будете играть?')
            for a in range(len(aux_list)):
                if (a!=player_term[0]):
                    bar = tk.Button (skem, text = aux_list[a]["name"], command = lambda koi = a: terminator(koi))
                    skem_knopka.append(bar)
            for a in range(len(skem_knopka)):
                skem_knopka[a].pack(side=tk.LEFT)
            skem.grab_set()
        else:
            log.write('Игрок отказывается играть в терминатор' + '\n')
            show(q_number)
    else:
        root.termtimer = root.after(400, term_choose)


def blah():
    global variant_bg, happy_variant, stagegong, active, bong_stopped, all_m
    stagegong = bongstage.finish
    if variant_bg == happy_variant:
        bong_summa["text"] = str(all_m)
        bong_stop["state"] = "disabled"
        if (bong_stopped)==False:
            aux_list[active]["sgor"] = all_m
            log.write(aux_list[active]["name"]+' отыгрывает все '+str(aux_list[active]["sgor"])+'\n')
    else:
        bong_summa["text"] = "ГОНГ"
        bong_stop["state"] = "disabled"
        if (bong_stopped)==False:
            aux_list[active]["sgor"] = 0
            log.write(aux_list[active]["name"] + ' ничего не отыгрывает'+'\n')
    zaideju_pinigai[active]['text'] = str(aux_list[active]['sgor']) + ' + ' + str(
        aux_list[active]['nesgor']) + ' = ' + str(aux_list[active]['sgor'] + aux_list[active]['nesgor']) + '\n'
    log.write('Итого ' + aux_list[active]["name"] + ' выигрывает ' + str(
        aux_list[active]['sgor'] + aux_list[active]['nesgor']) + '\n')
    bong_stop["text"] = "Следующий игрок"
    bong_stop["state"] = "normal"

def increase():
    global stagegong, bong_summa_index, bong_buttons, bong_summa, bong_stop
    stagegong = bongstage.inprogress
    root.after_cancel(root.bongtimer)
    bong_summa_index += 1
    if (bong_summa_index == 0):
        bong_stop["state"] = "active"
        bong_summa["text"] = str(var_ready[bong_summa_index])
        stagegong = bongstage.inprogress
        root.bongtimer = root.after(randint(1600, 3200), increase)
    elif bong_summa_index <= len(var_ready)-1:
        bong_summa["text"] = str(var_ready[bong_summa_index])
        root.bongtimer = root.after(randint(1600, 3200), increase)
        # if (bong_summa_index < len(x2)-1):
        #     root.timer = root.after(randint(800, 1900), increase)
    elif (bong_summa_index >= len(var_ready)):
        blah()




def setgong(variant_, aim):
    global var_ready, variant_bg, happy_variant, all_m
    b = randint (5, 15)
    cpp = []
    for d in range(b):
        while True:
            e = randint(1, aim - 1)
            if not (e in cpp):
                break
        cpp.append(e)
    #c.append (aim)
    cpp.sort()
    #c.pop(0)
    if (variant_!=happy_variant):
        var = cpp[:randint(3, b-2)]
    else:
        var = cpp.copy()
    var_ready = var.copy()
    #print(var_ready)
    variant_bg = variant_
    all_m = aim

def reshenie(lm):
    global nuspresti, yes, no, stab, active, q_number
    if (active<len(aux_list)):
        nuspresti = tk.Toplevel(root)
        nuspresti.protocol('WM_DELETE_WINDOW', noway)
        nuspresti.title(aux_list[lm]['name'] + ', ваше решение')
        yes = tk.Button(nuspresti, text="Продолжить игру", command=lambda t=lm: goon(t))
        yes.pack(side=tk.LEFT)
        no = tk.Button(nuspresti, text="Забрать деньги", command=lambda t=lm: cash(t))
        no.pack(side=tk.LEFT)
        if (aux_list[lm]['stab_can']):
            stab = tk.Button(nuspresti, text="Стабилизировать", command=lambda t=lm: chair(t))
            stab.pack(side=tk.LEFT)
        nuspresti.grab_set()
    else:
        if (len(aux_list)==len(who_walks_away)):
            tkinter.messagebox.showinfo("Игра окончена", "Все игроки забрали деньги")
            log.write("Игра окончена"+'\n')
        else:
            for s in range(len(aux_list)):
                zaideju_vardai[s].place_forget()
                zaideju_pinigai[s].place_forget()
            aux_list[:] = [x for i, x in enumerate(aux_list) if i not in who_walks_away]
            # for a in range (len(aux_list)):
            #     zaideju_vardai[a].place(x=8, y=8 + 55 * a)
            #     zaideju_pinigai[a].place(x=108, y=8 + 55 * a)
            q_number+=1
            if (len(aux_list)>1) and(q_number in [3, 5, 7, 9]): #терминатор
                global schetchik
                schetchik = randint(10, 20)
                tkinter.messagebox.showinfo('Терминатор', 'Играем в терминатор!')
                root.termtimer = root.after(400, term_choose)
            else:
                show(q_number)


def stopgame():
    global stagegong, bong_summa_index, timer, variant, bong_stopped
    if stagegong == bongstage.inprogress:
        root.after_cancel(root.bongtimer)
        stagegong = bongstage.stopped
        bong_stopped = True
        log.write(aux_list[active]["name"]+' отыгрывает '+str(var_ready[bong_summa_index])+'\n')
        aux_list[active]['sgor'] = var_ready[bong_summa_index]
        zaideju_pinigai[active]['text'] = str(aux_list[active]['sgor']) + ' + ' + str(aux_list[active]['nesgor']) + ' = ' + str(aux_list[active]['sgor'] + aux_list[active]['nesgor']) + '\n'
        #print(str(var_ready[bong_summa_index]))
        bong_stop["text"] = "Смотреть дальше"
    elif stagegong == bongstage.stopped:
        bong_summa_index += 1
        if (bong_summa_index < len(var_ready)):
            bong_summa["text"] = str(var_ready[bong_summa_index])
        elif (bong_summa_index == len(var_ready)):
            blah()
            zaideju_pinigai[active]['text'] = str(aux_list[active]['sgor']) + ' + ' + str(
                aux_list[active]['nesgor']) + ' = ' + str(aux_list[active]['sgor'] + aux_list[active]['nesgor']) + '\n'
            #log.write('Итого ' + aux_list[active]["name"] + ' выигрывает ' + str(aux_list[active]['sgor'] + aux_list[active]['nesgor']) + '\n')
            #aux_list[active]["sgor"] = all_m
    elif (stagegong ==bongstage.finish):
        next()


def start(uyt):
    for a in range(len(bong_buttons)):
        bong_buttons[a]["state"] = "disabled"
    root.bongtimer = root.after(randint(1600, 3200), increase)
    setgong(uyt, aux_list[active]['sgor'])
    #print(uyt, aux_list[active]['sgor'])


def bong_game():
    global stagegong, bong_summa_index, active, bong_buttons, bong_summa, bong_stop, bong_stopped
    bong_stopped = False
    stagegong = bongstage.before
    bong_summa_index = -1
    for a in range(3):
        l = tk.Button(text=str(a + 1), width=5, height=1, command=lambda rtt=a: start(rtt))
        bong_buttons.append(l)
        bong_buttons[a].place(relx=.30 + .25 * a, rely=0.08)
    bong_summa = tk.Label(root, width=14, height=1, text="0")
    bong_summa.place(relx=0.3, rely=0.18)
    bong_stop = tk.Button(text="Стоп", width=9, height=1, command=stopgame, state="disabled")
    bong_stop.place(relx=0.31, rely=0.24)



def whattodo(j):
    global nuspresti, yes, no, stab, active
    if (j<10):
        global who_walks_away
        who_walks_away = []
        active = 0
        reshenie(active)

            # nuspresti = tk.Toplevel(root)
            # nuspresti.protocol('WM_DELETE_WINDOW', noway)
            # nuspresti.title (aux_list[u]['name']+', ваше решение')
            # yes = tk.Button(nuspresti, text="Продолжить игру", command = lambda t=u: goon(t))
            # yes.pack(side=tk.LEFT)
            # no = tk.Button(nuspresti, text="Забрать деньги", command =lambda t=u: cash(t))
            # no.pack(side=tk.LEFT)
            # if (aux_list[u]['stab_can']):
            #     stab = tk.Button(nuspresti, text="Стабилизировать", command =lambda t=u: chair(t))
            #     stab.pack(side=tk.LEFT)
            # nuspresti.grab_set()
        #q_number+=1
        #show(q_number)
    else:
        tkinter.messagebox.showinfo("Поздравляем", "Вы успешно прошли игру!")





def ch_corr_ontimer(i):
    global active, bong_buttons, happy_variant, variant_bg
    if(Klausimai[r]["C"][0]-1 == accepted):
        varianty[i]["bg"] = "#7fff7f"
        log.write("Это правильный ответ"+'\n')
        for u in range(len(aux_list)):
            aux_list[u]['sgor'] += money[q_number-1] // len(aux_list)
            zaideju_pinigai[u]['text'] = str(aux_list[u]['sgor']) + ' + ' + str(aux_list[u]['nesgor']) + ' = ' + str(
                aux_list[u]['sgor'] + aux_list[u]['nesgor']) + '\n'
            #imie_dummy = tk.Label(text=aux_list[u]["name"])
            #pieniadze_dummy = tk.Label(text=str(aux_list[u]['sgor']) + ' + ' + str(aux_list[u]['nesgor']) + ' = ' + str(
                #aux_list[u]['sgor'] + aux_list[u]['nesgor']) + '\n')
            #zaideju_vardai.append(imie_dummy)
            #zaideju_pinigai.append(pieniadze_dummy)
            #zaideju_vardai[u].place(x=8, y=8 + 55 * u)
            #zaideju_pinigai[u].place(x=108, y=8 + 55 * u)
        tkinter.messagebox.showinfo("Верно!", "Вы дали правильный ответ!")
        for a in range(otv[q_number - 1]):
            varianty[a].place_forget()
            eax[a].place_forget()
        parodytas_klausimas.place_forget()
        for u in range(len(aux_list)):
            log.write(
                aux_list[u]['name'] + ': ' + str(aux_list[u]['sgor']) + ' + ' + str(
                    aux_list[u]['nesgor']) + ' = ' + str(
                    aux_list[u]['sgor'] + aux_list[u]['nesgor']) + '\n')
        whattodo(q_number)
    else:
        varianty[i]["bg"] = "#ff7f7f"
        log.write("Это неправильный ответ" + '\n')
        varianty[Klausimai[r]["C"][0]-1]["bg"] = "#7fff7f"
        log.write("Правильный ответ - "+Klausimai[r]["A"][Klausimai[r]["C"][0]-1]+ '\n')
        tkinter.messagebox.showinfo("Вы ошиблись!", "Правильный ответ - "+Klausimai[r]["A"][Klausimai[r]["C"][0]-1])
        for a in range(otv[q_number - 1]):
            varianty[a].place_forget()
            eax[a].place_forget()
        parodytas_klausimas.place_forget()
        active = -1
        bong_buttons = []
        happy_variant = randint(0, 2)
        #print(happy_variant+1)
        variant_bg = None
        while True:
            active+=1
            if (aux_list[active]['sgor']>0):
                break
        tkinter.messagebox.showinfo(aux_list[active]["name"], "Играйте в гонг-игру!")
        bong_game()
        pass #дописать




def ko():
    root.after_cancel(root.lop)
    global active, _otveti, aux_list, ui, accepted, Points, Ochki, _sort, maximal, otvet, pristine
    if (_otveti != priem.vse):
        active +=1
        _otveti = priem.otveti
        if (active > len(aux_list)):
            _otveti = priem.vse
            maximal = []
            for a in range(otv[q_number - 1]):
                knopki[a].place_forget()
            Points = []
            for a in range (otv[q_number - 1]):
                Ochki = dict(Index=(a+1), Sum=golosov[a])
                Points.append(Ochki)
            _sort = sorted(Points, key=lambda s: s['Sum'], reverse = True)
            for o in range((len(_sort) - 1), 0, -1):
                if (_sort[o]["Sum"] == _sort[0]["Sum"]):
                    for l in range(o, -1, -1):
                        maximal.append(_sort[l]["Index"])
                        break
            maximal.append(_sort[0]["Index"])
            if (len(maximal) > 1):
                of_rich = 0
                mostmoney = 0
                for a in range(len(aux_list)):
                    if (aux_list[a]['vote'] in maximal) and ((aux_list[a]['sgor'])+(aux_list[a]['nesgor']) > mostmoney):
                        of_rich = a
                        mostmoney = (aux_list[a]['sgor'])+(aux_list[a]['nesgor'])
                count = 0
                otvet = []
                for a in range(len(aux_list)):
                    if (aux_list[a]['sgor'])+(aux_list[a]['nesgor'] == mostmoney) and (aux_list[a]['vote'] in maximal):
                        count += 1
                        otvet.append(aux_list[a]['vote'])
                #print("Самых богатых игроков: ", count)
                #print(otvet, 'Rich vars')
                pristine =  None
                if (count > 1):
                    pristine = choice(otvet)-1
                    #print(pristine)
                    #print(("Самых богатых игроков: "+str(p)))
                    tkinter.messagebox.showinfo("Случайный выбор", "Случайно выбран ответ "+Klausimai[r]["A"][pristine])
                else:
                    pristine = otvet[0]-1
                    tkinter.messagebox.showinfo("Из ответов, собравших максимум голосов, ", "Самый богатый игрок выбрал ответ "+Klausimai[r]["A"][pristine])
            else:
                pristine = maximal[0]-1
                tkinter.messagebox.showinfo("Ответ принят", Klausimai[r]["A"][pristine])
            log.write("Команда выбрала ответ "+Klausimai[r]["A"][pristine]+ '\n')
            varianty[pristine]["bg"]="#ffff7f"
            accepted = pristine
            root.check_correct = root.after(2500, lambda h = pristine: ch_corr_ontimer(h))
            #for a in range(len(aux_list)):
                #Points[aux_list[a]['vote']] += ((aux_list[a]['sgor'])+(aux_list[a]['nesgor']))


            #допишу потом
            #ui = max(golosov)
            #tkinter.messagebox.showinfo("OK", "Выбран ответ "+Klausimai[r]["A"][ui])#отладка

        else:
            tkinter.messagebox.showinfo(aux_list[active-1]["name"], 'Дайте свой ответ')
            for a in range(otv[q_number-1]):
                knopki[a]["state"]="normal"





def show(test):
    global imie_dummy, pieniadze_dummy, parodytas_klausimas, active, accepted, _otveti
    root.after_cancel(root.qu_sh)
    if (test==1):
        tk.messagebox.showinfo("Готово", "Мы начинаем игру")
    else:
        tk.messagebox.showinfo("Внимание", "Следующий вопрос")
    accepted = None
    v = codecs.open('baza' + str(test) + '.txt', 'r', "utf_8_sig")
    global count
    global Klausimai
    global zaideju_vardai
    global zaideju_pinigai
    global golosov, varianty, dum_var, buttonz, knopki, eax, jik
    golosov = []
    eax = []
    count = 0
    Klausimai = []
    buttonz = []
    jik = None
    dum_var = None
    varianty = []
    knopki = []
    for line in v:
        vopr = {}
        HUHA = line.rstrip("\n")
        vopr["Q"] = HUHA
        vopr["A"] = []
        vopr["C"] = []
        for a in range(otv[test-1]):
            foo = v.readline()
            foo = foo.rstrip('\n')
            vopr["A"].append(foo)
        foo = v.readline()
        vopr["C"].append(int(foo))
        Klausimai.append(vopr)
        count+=1
    v.close()
    imie_dummy = []
    pieniadze_dummy = []
    zaideju_vardai = []
    zaideju_pinigai = []
    for u in range (len(aux_list)):
        imie_dummy = tk.Label(text = aux_list[u]["name"])
        pieniadze_dummy = tk.Label(text = str(aux_list[u]['sgor']) + ' + ' + str(aux_list[u]['nesgor']) + ' = ' + str(aux_list[u]['sgor'] + aux_list[u]['nesgor'])+'\n')
        zaideju_vardai.append(imie_dummy)
        zaideju_pinigai.append(pieniadze_dummy)
        zaideju_vardai[u].place(x=8, y = 8 + 55*u)
        zaideju_pinigai[u].place(x = 108, y=8+55*u)
        aux_list[u]["vote"] = None
        log.write(
            aux_list[u]['name'] + ': ' + str(aux_list[u]['sgor']) + ' + ' + str(
                aux_list[u]['nesgor']) + ' = ' + str(
                aux_list[u]['sgor'] + aux_list[u]['nesgor']) + '\n')
    global r
    r = randint(0, len(Klausimai)-1)
    log.write(Klausimai[r]["Q"]+'\n')
    for a in range(otv[q_number-1]):
        log.write(str(a+1)+'. '+Klausimai[r]["A"][a] + '\n')
        dum_var = tk.Label(text = Klausimai[r]["A"][a], bg="#7fffff")
        varianty.append(dum_var)
        varianty[a].place(relx=0.4, rely = 0.14+0.07*a, width=280, height=40)
        buttonz = tk.Button(root, text = "Выбор", width=14, height=1, command = lambda a1 = a: answer(a1))
        knopki.append(buttonz)
        knopki[a].place(relx=0.72, rely=0.14+0.07*a)
        knopki[a]["state"] = "disabled"
        golosov.append(0)
        jik = tk.Label(text=str(golosov[a]))
        eax.append(jik)
        eax[a].place(relx=0.29, rely=0.14+0.07*a, width=100, height=40)
    #log.write(str(Klausimai[r]["C"][0]) + '\n')
    parodytas_klausimas.place(relx=0.4, rely=0.02, width = 410, height = 70)
    parodytas_klausimas["text"] = Klausimai[r]["Q"]
    parodytas_klausimas["justify"] = tkinter.CENTER
    parodytas_klausimas["bg"] = "#cfcfcf"
    parodytas_klausimas["wraplength"] = 380
    active = 0
    # for al in range(len(aux_list)):
    #     aux_list[al]["vote"] = None
    #     log.write(
    #         aux_list[al]['name'] + ': ' + str(aux_list[al]['sgor']) + ' + ' + str(aux_list[al]['nesgor']) + ' = ' + str(
    #             aux_list[al]['sgor'] + aux_list[al]['nesgor']) + '\n')
    #vote=[]
    _otveti = priem.do
    log.write("Ответы игроков: "+'\n')
    root.lop = root.after(1000, ko)
    # /* отладочная инфа
    #root.lop = root.after(100, ko)
    # log.write(Klausimai[len(Klausimai)-1]["Q"]+'\n')
    # for a in range(otv[q_number-1]):
    #     log.write(Klausimai[len(Klausimai)-1]["A"][a])
    # log.write(str(Klausimai[len(Klausimai)-1]["C"][0]) + '\n')
    #*/



def kwalif():
    global aux_list
    for a in range(len(start_names)):
        if start_names[a].get()=="":
            tk.messagebox.showwarning("Имена", "По меньшей мере у одного из игроков пустое имя. Исправьте")
            break
    else:
        rich.place_forget()
        log.write('Игроки: '+'\n')
        aux_list = []
        for b in range (5):
            aux_dict = {}
            aux_dict['name'] = start_names[b].get()
            aux_dict['sgor'] = 600
            aux_dict['nesgor'] = 0
            aux_dict['stab_can'] = True
            aux_dict['vote'] = None
            D = aux_dict.copy()
            aux_list.append(aux_dict)
        for b in range(5):
            pass
            #log.write(aux_list[b]['name'] + ': ' + str(aux_list[b]['sgor']) + ' + ' + str(aux_list[b]['nesgor']) + ' = ' + str(aux_list[b]['sgor'] + aux_list[b]['nesgor'])+'\n')
        for b in range(5):
            player[b].place_forget()
        #tk.messagebox.showinfo("Готово", "Мы начинаем игру")
        global q_number
        q_number+=1
        root.qu_sh = root.after(1000, lambda b=q_number: show(b))








for x in range(5):
    dummy = tk.StringVar()
    dummy.set("Игрок "+str(x+1))
    start_names.append(dummy)

for pl_field in range (5):
    nombre = ttk.Entry(root, textvariable = start_names[pl_field])
    player.append(nombre)
    player[pl_field].place(width=140, relx = 0.03, rely=0.05+pl_field*(0.18))

rich = tk.Button(root, text="Начать игру", command=kwalif, width = 14, height = 30)
rich.place(relx = 0.5, rely=0.05)

log = open ('log.txt', 'a')
log.write('\n')
root.protocol('WM_DELETE_WINDOW', doSomething)
root.bind('<KeyPress>', onKeyPress)
vvod = tk.Entry(textvariable = termotvet)
vvod.bind("<Return>", accepted_in_terminator)

root.mainloop()
