# -------------------------------------------------------
# Assignment 1
# Written by Michel Rahme 40038465
# For COMP 472 Section IX – Summer 2020
# --------------------------------------------------------

from tkinter import *
from crime_plot import *


class MyApp:
    entry = None

    def __init__(self):
        # set tkinter window 
        self.root = Tk()
        self.root.title("Montreal Crime Tracker")
        self.root.minsize(500, 250)
        Label(self.root, text="Please set Threshold then select Grid Size to generate Figure", font=(None, 18)).grid(
            row=0, padx=(10, 10), pady=(20, 0), columnspan=2)
        Label(self.root, text="Only values between 0 to 100 will be accepted", font=(None, 15)).grid(
            row=1, padx=(10, 0), pady=(10, 0), columnspan=2)
        Label(self.root, text="Threshold: ").grid(row=2, pady=(20, 0))
        self.entry = Entry(self.root)
        self.entry.insert(END, '50')
        self.entry.grid(row=2, column=1, pady=(20, 0), sticky=W)
        Label(self.root, text="Grid Size: ").grid(row=3)
        Button(self.root, text="0.001", command=self.on_clicked_1).grid(row=3, column=1, sticky=W)
        Button(self.root, text="0.002", command=self.on_clicked_2).grid(row=3, column=1, padx=(0, 30))

    # Button 1 function
    def on_clicked_1(self):
        if not self.entry.get().isalpha():
            if 0 <= float(self.entry.get()) <= 100:
                CrimePlot(threshold=float(self.entry.get()), grid_size=0.001)

    # Button 2 function
    def on_clicked_2(self):
        if not self.entry.get().isalpha():
            if 0 <= float(self.entry.get()) <= 100:
                CrimePlot(threshold=float(self.entry.get()), grid_size=0.002)


if __name__ == '__main__':
    app = MyApp()
    app.root.mainloop()
