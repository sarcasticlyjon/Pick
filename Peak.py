from tkinter import *
from tkinter import ttk
from frame import FrameGrand
from PIL import ImageTk, Image


class Peak():

    def __init__(self, grand):

        self.took = grand
        self.took.title('ПИК')
        self.took.geometry('280x530+300+300')
        self.took.resizable(False, False)
        self.style = ttk.Style(self.took)
        self.style.configure("TNotebook.Tab", padding = [5, 4], 
            font ='arial 13')

        #Вставка и обработка изображений для иконок
        sizenote = (19, 19)
        sizehelp = (75, 75)
        self.saveimage = Image.open('icon/save.png') 
        self.deletimage = Image.open('icon/delete.png')
        self.save = ImageTk.PhotoImage(self.saveimage.resize(sizenote, 
            Image.ANTIALIAS))
        self.delete = ImageTk.PhotoImage(self.deletimage.resize(sizenote, 
            Image.ANTIALIAS))
        self.savehelp = ImageTk.PhotoImage(self.saveimage.resize(sizehelp, 
            Image.ANTIALIAS))
        self.deletehelp = ImageTk.PhotoImage(self.deletimage.resize(sizehelp, 
            Image.ANTIALIAS))
        self.iconimage = Image.open('icon/icon.png') 
        self.icon = ImageTk.PhotoImage(self.iconimage.resize((200, 200), 
            Image.ANTIALIAS))


        self.notebook = ttk.Notebook(self.took)
        self.frame1 = ttk.Frame(self.notebook)
        self.frame2 = ttk.Frame(self.notebook)
        self.frame3 = ttk.Frame(self.notebook)
        self.frame4 = ttk.Frame(self.notebook)
        self.helpFrame = ttk.Frame(self.notebook)
        self.notebook.add(self.frame1, text='   2θ  ')
        self.notebook.add(self.frame2, text='   X   ')
        self.notebook.add(self.frame3, image = self.save)
        self.notebook.add(self.frame4, image = self.delete)
        self.notebook.add(self.helpFrame, text = 'Справка')

        # Фрейм справки
        self.helped = FrameGrand(self.helpFrame, name = 'Справка')
        self.helped.help(self.savehelp, self.deletehelp, self.icon)
        
        '''рассчет положения пиков'''

        self.firstFrame = FrameGrand(self.frame1, name ='Положение' )
        self.firstFrame.choisubst("Добавить")
        self.firstFrame.selectsys()
        self.firstFrame.colculsys(0)
        self.firstFrame.selectcompos()
        self.firstFrame.resultsave("Сохранить")
        
        '''рассчет состава'''

        self.secondFrame = FrameGrand(self.frame2, name ='Состав')
        self.secondFrame.choisubst("Добавить")
        self.secondFrame.selectsys()
        self.secondFrame.colculsys(0)
        self.secondFrame.selectpeak()
        self.secondFrame.resultsave("Сохранить")   

        '''добавление/корректировка данных'''

        self.thirdFrame = FrameGrand(self.frame3, name = "Запись")
        self.thirdFrame.choisubst("Выбрать", 1)
        self.thirdFrame.selectsys("Выбранное вещество")
        self.thirdFrame.colculsys(0)
        self.thirdFrame.selectpeak("Добавить")
        self.thirdFrame.resultsave("Сохранить") 

        '''удаление данных'''

        self.fourthFrame = FrameGrand(self.frame4, name = "Удаление")
        self.fourthFrame.colculsys(50)
        self.fourthFrame.choisubst("Показать", 0)
        self.fourthFrame.resultsave("Удалить", 100, 5)

        self.notebook.bind("<<NotebookTabChanged>>", self.updatelist)
        self.notebook.pack(expand=1, fill='both')

        self.took.mainloop()

    def updatelist(self, event):
        #обнавление данных перечня оксидов при выборе вкладки
        index = event.widget.index('current')
        if index == 0:
            self.firstFrame.newlist()
        elif index == 1:
            self.secondFrame.newlist()
        elif index == 2:
            self.thirdFrame.newlist()
        elif index == 3:
            self.fourthFrame.newlist()
        else:
            pass

root = Tk()

Peak(root)

