from tkinter import *
from tkinter import ttk
from reaData import Data

class Child(Data):
    
    '''Класс отвечает за окно выбора рассчетной длины волны'''

    def __init__(self, master):
        super().__init__()

        self.children = Toplevel(master)
        self.style = ttk.Style(self.children)
        self.style.configure("TButton", padding=1, relief="flat", 
            background="#ccc", font='arial 8')
        self.style.configure("TCombobox", relief="flat", 
            background="white", font='arial 8')
        self.style.configure("TLabel", foreground="black", font='arial 8')
        self.children.title('λ, Å')
        self.children.geometry('170x120+600+600')
        self.children.resizable(False, False)
        self.labelwave = ttk.Label(self.children, text = "Длина волны")
        self.combwave = ttk.Combobox(self.children)
        self.combwave.config(values= self.lenght, width = 8)
        self.buttonwave = ttk.Button(self.children, text = "Закрыть", 
            width = 10, command = self.cliced_button1)
        self.buttonwave1 = ttk.Button(self.children, text = "Выбрать", 
            width = 8, command = self.cliced_button2)
        self.wavelength = float()

        self.labelwave.place(x = 15, y = 10)
        self.combwave.place(x = 15, y = 30)
        self.buttonwave.place(x = 50, y = 85)
        self.buttonwave1.place(x = 100, y = 29)

    def cliced_button1(self):
        #закрываем окно
        self.children.destroy()

    def cliced_button2(self):
        #поиск и отображение длины волны в датафрейме
        self.wordwave = self.combwave.get()
        self.wavelength = float(self.datawave.loc[self.wordwave])
        text = "Длина волны {:.4f} Å".format(self.wavelength)
        self.labelwave = Label(self.children, text = text)
        self.labelwave.place(x= 20, y = 57)