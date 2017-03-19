#!/usr/bin/env python3
from tkinter import *
import json

def load(path):
    with open(path, 'r') as f:
        return json.loads(f.read())

TUNINGS =  load('tunings.json')
SCALES  =  load('scales.json')
NOTES = ['E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb']
COLORS = { 'Root':'Red', 'Scale':'Yellow', 'Default':'White' }

class Chart(object):
    def __init__(self):
        self.window = Tk()
        self.window.geometry("625x250+200+200")
        self.window.title('Scale Chart for Guitar')
        self.tuning = StringVar(self.window)
        self.tuning.set('Standard')
        self.tonic  = StringVar(self.window)
        self.tonic.set('E')
        self.scale  = StringVar(self.window)
        self.scale.set('Major')
        
        for i in range(0, 25):
            self.make_label(i, '', 0, i + 1, 0, 10)
            self.make_label(i, '', 9, i + 1, 0, 10)

        OptionMenu(self.window, self.tuning, *TUNINGS.keys(), command=self.invalidate).place(x=155, y=210)
        OptionMenu(self.window, self.tonic, *NOTES, command=self.invalidate).place(x=275, y=210)
        OptionMenu(self.window, self.scale, *SCALES.keys(), command=self.invalidate).place(x=350, y=210)

    def invalidate(self, val):
        tuning = TUNINGS[str(self.tuning.get())]
        for i in range(0, 6):
            self.make_label(tuning[i], '', i + 2, 0, 10)

        tonic = str(self.tonic.get())
        offset = self.get_offset()
        ournotes = self.make_scale()
        for f in range(0, 25):
            for s in range(0, 6):
                start = offset[s]
                bg = ''
                
                if tonic == self.get_tonic(f + start % 12):
                    bg = 'Root'
                elif self.get_tonic(f + start) in ournotes:
                    bg = 'Scale'

                self.make_label(self.get_tonic(f + start), bg, s + 2, f + 1)
    
    def get_offset(self):
        offsets = []
        tuning = TUNINGS[self.tuning.get()]
        for s in range(0, 6):
            offsets.append(NOTES.index(tuning[s]))
        return offsets

    def get_tonic(self, index):
        return NOTES[index % len(NOTES)]

    def make_label(self, text, bg, row, col, x=0, y=0):
        bg = COLORS.get(bg) if bg != '' else COLORS.get('Default')
        text = str(text) + ' ' if len(str(text)) == 1 else text
        Label(self.window, text=text, bg=bg).grid(row=row, column=col, padx=x, pady=y)

    def make_scale(self):
        filler = 0
        key = SCALES.get(self.scale.get())
        size = len(key)

        notes = []
        for i in range(size):
            filler += key[i % size]
            notes.append(int(filler + NOTES.index(self.tonic.get())))
    
        scale = []
        for notes in notes:
            scale.append(self.get_tonic(notes))

        return scale

    def show(self):
        self.invalidate(0)
        self.window.mainloop()
    
if __name__ == '__main__':
    Chart().show()