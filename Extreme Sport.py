#!/usr/bin/env python
print("Starting TIME-ers")
print("Loading...")

import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
from ioUtils import *
import random
import time
import PySimpleGUI as sg

import datetime
year = datetime.date.today().year


full = {}


url = "https://en.wikipedia.org/wiki/Detailed_logarithmic_timeline"

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')

tables = soup.find_all('table')

rows = str(tables).split("<tr>")

for row in rows:
    #print(row)

    hasPeriod = True
    
    try:
        interval, period, event = row.split("<td>")
    except:
        try:
            interval,event = row.split("<td>")
            hasPeriod = False
        except:
            continue


    interval = removeMarkup(interval, "<", ">")
    interval = removeMarkup(interval, "(", ")")

    interval = interval.replace("years", "y")
    interval = interval.replace("exaannus", "Ea")
    interval = interval.replace("zettaannus", "Za")

    interval = interval.replace("Ya", "e24")
    interval = interval.replace("Za", "e21")
    interval = interval.replace("Ea", "e18")
    interval = interval.replace("Pa", "e15")
    interval = interval.replace("Ta", "e12")
    interval = interval.replace("Ga", "e9")
    interval = interval.replace("Ma", "e6")
    interval = interval.replace("ka", "e3")
    interval = interval.replace("y", "")
    interval = interval.replace(" ", "")

    interval = interval.strip("\n")

    #if "." in interval:
    #    interval = str(int(interval))

    if not hasPeriod:
        interval = "F" + interval

    #print(interval)

    if hasPeriod:

        period = removeMarkup(period, "<", ">")
        period = removeMarkup(period, "(", ")")

        if "–" in period:
            period = period = period.split("–")[-1]

        if "ca." in period:
            period = period.split("ca.")[-1]
            period = period.strip()
            if "CE" not in period:
                period = period + " AD"

        period = period.strip()

    else:
        period = "False"

    if not len(period):
        period = "False"

    event = removeMarkup(event, "<", ">")
    event = event.strip("\n")

    events = []

    for i in range(0, len(event.split("\n"))):
        if len(str(event.split("\n")[i])) < 4:
            continue
        events.append(removeMarkup(event.split("\n")[i], "[", "]"))
    
    if len(events) and len(interval):
        
        full[interval] = [period, events]


bg = "#440088"
fg = "lightblue"
window = None

def loadMain():
    global window

    try:
        window.close()
    except:
        pass
    
    layout = [[sg.Column([[sg.Text('Enter Timer Duration (mins):', background_color=bg, text_color=fg, font=("Helevicta", 18))],
                         [sg.Input(k="-INPUT-", background_color="#330055", text_color=fg, size=(10, None), font=("Helevicta", 18),
                                   pad=((3, 3), (13, 20)))],
                         [sg.Button("Exit", button_color=(fg, "#330055"), key="-EXIT-", font=("Helevicta", 14), size=(8, None)),
                          sg.Button("Done", button_color=(fg, "#330055"), key="-DONE-", font=("Helevicta", 14), size=(8, None),
                                    bind_return_key=True)]],
                         element_justification="centre", background_color=bg)]]

    window = sg.Window('TIME-ers.', layout,
                       finalize=True,
                       margins=(25, 25),
                       background_color=bg,
                       grab_anywhere=False)

    window.refresh()

loadMain()

far = False

def getEntry(date):
    global far, window

    target = ""
    future = False

    if date > 0 and date <= 10:
        future = True
        data = ["False", ["The present day.", "Today.", "Tomorrow.", "Yesterday",
                          "Everything that is going to happen next week.", "All of last week."]]
    else:
        for timePeriod in full.keys():
            if "F" in timePeriod:   
                future = True
                timePeriod = timePeriod[1:]
                lower, upper = timePeriod.split("–")
                lower = eval(lower.replace("e", "*10**"))
                upper = eval(upper.replace("e", "*10**"))
                print(date, lower, upper)
                if date > int(lower) and date <= int(upper):                
                    target = timePeriod
                    break
            else:
                lower, upper = timePeriod.split("–")
                lower = eval(lower.replace("e", "*10**"))
                upper = eval(upper.replace("e", "*10**"))
                if date > int(lower)*-1 and date <= int(upper)*-1:                
                    target = timePeriod
                    break
        else:
            far = True

        if not far:
            if future:
                data = full["F"+str(target)]
            else:
                data = full[str(target)]
        else:
            data = ["False", ["The universe ends.", "All is lost", "There is nothing left.", "We are out of time."]]

    if len(data) == 2:
        period, events = data

    chosen = ""

    n = 1

    numEvents = random.randint(1, 2)

    if len(events) == 1:
        event = events[0] + "."
        if ". " in event:
            event = random.choice(event.split(". ")) + "."
        chosen = event

    else:

        targ = numEvents
        if numEvents > len(events):
            targ = len(events)
        
        while n <= targ:

            event = random.choice(events)

            if ". " in event:
                event = random.choice(event.split(". ")) + "."

            if str(event).lower().replace(".", "") not in str(chosen).lower().replace(".", ""):
                if n == 1:
                    chosen += event.replace(".", "").strip() + "."
                elif n == targ:
                    chosen += ". " + event.replace(".", "").strip() + "."
                else:
                    chosen += ". " + event.replace(".", "").strip() + "."
                n += 1

    chosen = chosen[0].upper() + chosen[1:]
    chosen = chosen.replace("..", ".")
    #print("Chosen: ", chosen)

    return chosen, period
    

def timeMapper(duration):

    startTime = time.time()

    lastRefresh = 0

    global window, bg, fg, far

    window.close()

    layout = [[sg.Column([[sg.Text(' '*50, background_color="#330055", text_color=fg, font=("Helevicta", 12), k="-S-"),
                           sg.VerticalSeparator(k="-VR1-"),
                           sg.Text('0.000%', background_color="#330055", text_color=fg, font=("Helevicta", 12), k="-%-"),
                           sg.VerticalSeparator(k="-VR2-"),
                           sg.Text(' '*50, background_color="#330055", text_color=fg, font=("Helevicta", 12), k="-TIME-")],
                          [sg.HorizontalSeparator(k="-HR1-")],
                          [sg.ProgressBar(100, "h", (50, 7), bar_color=("purple", "black"), k="-BAR-")],
                          [sg.Text('Around this time:', background_color=bg, text_color=fg, font=("Helevicta", 12), k="-ATT-")],
                          [sg.Multiline(k="-OUTPUT-", size=(45, 6), background_color="#330055", text_color=fg, font=("Helevicta", 14))],
                          [sg.Button("Exit", button_color=("red", "#330055"), mouseover_colors=("#330055", "red"), key="-EXIT-", font=("Helevicta", 14), size=(8, None)),
                           sg.Button("Pause", button_color=("orange", "#330055"), mouseover_colors=("#330055", "orange"), key="-DONE-", font=("Helevicta", 14), size=(8, None))]],
                          element_justification="centre", background_color=bg, k="-COL-")]]

    window = sg.Window('TIME-ers.', layout,
                       finalize=True,
                       margins=(10, 10),
                       background_color="#330055")

    window.refresh()

    paused = False
    pauseTime = 0
    pauseStart = 0

    while 1:

        event, values = window.read(timeout=1)

        if event == "-DONE-":
            if paused:
                paused = False
                window.TKroot.configure(background="#330055")
                window["-DONE-"].update("Pause")
                pauseTime = time.time() - pauseStart
                startTime += pauseTime
                print("pAUSED ", pauseTime)
            else:
                paused = True
                pauseStart = time.time()
                window["-DONE-"].update("Resume")
                window.TKroot.configure(background="orange")
                

            window.refresh()

        elif event == "-EXIT-" or event == sg.WIN_CLOSED:
            loadMain()
            main()

        if paused:
            continue

        completion = 1 - ((time.time() - startTime) / duration)

        rem = (startTime + duration) - time.time()

        if rem > 120:
            rem = str(rem / 60).split(".")[0] + " mins."
        else:
            rem = str(rem).split(".")[0] + " secs."

        window["-S-"].update(rem)

        window["-%-"].update(str((1-completion)*100)[:5].strip(".") + "%")

        window["-BAR-"].update((1-completion)*100)

        if (startTime + duration) - time.time() > 0:
            yearsAgo = (2.71828**(20.3405*(completion**3)+3) - 2.71828**3)*-1
        else:
            try:
                yearsAgo = (2.71828**(20.3405*(((completion)*-1)**3)+3) - 2.71828**3)
            except OverflowError:
                far = True
            if not far:
                window.TKroot.configure(background="maroon")

        yA = yearsAgo

        #print(yA)

        event, period, = getEntry(yA)

        if not far:
            yearsAgo = str(yearsAgo).split(".")[0]

            ago = False
            if "-" in str(yearsAgo):
                ago = True
                yearsAgo = str(yearsAgo).strip("-")

            if len(str(yearsAgo)) > 9:
                T = yearsAgo[:-9] + " billion"
            elif len(str(yearsAgo)) > 6:
                T = yearsAgo[:-6] + " million"
            elif len(str(yearsAgo)) > 4:
                T = yearsAgo[:-3] + " thousand"
            else:
                T = yearsAgo
                if int(T) < 6000 and ago:
                    T = int(T)*-1
                    if T < int(year)*-1:
                        T = str((int(year)*-1 - int(T))) + " BC."
                    else:
                        T = str((int(year)) + int(T)) + " AD."

            if not contains(T, ["BC", "AD"]):
                if ago:
                    T += " years ago."
                else:
                    T += " years time."
                
        else:
            T = "The distant future."
            window.TKroot.configure(background="red")

            
        window["-TIME-"].update(T)

        delay = random.randint(4, max(5, int(duration/60)))

        if time.time() - lastRefresh > delay:

            lastRefresh = time.time()

            window["-OUTPUT-"].update("")
            window["-OUTPUT-"].print(event)

        window.refresh()


def main():
    while 1:
        event, values = window.read()

        if event == "-EXIT-":
            quit()
        elif event == "-DONE-":
            duration = float(values["-INPUT-"]) * 60

            timeMapper(duration)


if __name__ == "__main__":
    main()
