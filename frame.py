from tkinter import *
from tkinter import ttk, messagebox as mb, filedialog as fd
import tkinter.scrolledtext as tkst
from child import Child
from reaData import Data
from pandas import read_table
from subprocess import Popen


class FrameGrand(Data):
    #Шаблон закладок в notebook

    def __init__(self, frame, name, font = 'arial 8', *args):
        super().__init__()
        self.frame = frame
        self.style = ttk.Style(self.frame)
        self.style.configure("TButton", padding=2, relief="flat", 
            background="#ccc", font = font)
        self.style.configure("TCombobox", relief="flat", 
            background="white", font = font)
        self.style.configure("TLabel", foreground="black", font = 'arial 9')
        
        self.click = 1 # проверка нажатий, для каждой вкладки свой
        self.first_oxide = str()
        self.second_oxide = str()
        self.only_oxide = str()
        self.name = name
        self.result = float()


        #Область выбора вещества
        self.label1 = ttk.Label(self.frame, text="Название вещества")        
        self.comb1 = ttk.Combobox(self.frame)
        self.comb1.config(font=font, width = 19)    
        self.button1 = ttk.Button(self.frame, width = 10)

        #Очистка полученной системы, выбранных оксидов/оксида
        self.label2 = ttk.Label(self.frame)       
        self.text2 = Text(self.frame, width=22, height=1, 
            bg="white", fg='black', font=font)      
        self.button2 = ttk.Button(self.frame, text = 'Очистить', 
            width = 10, command = self.delete)  

        #Выбор cистемы исчесления
        self.label3 = ttk.Label(self.frame, text='Система рассчёта')
        self.comb3 = ttk.Combobox(self.frame)
        self.comb3.config(font=font, width=19)     
        self.button3 = ttk.Button(self.frame, text = 'λ, Å', 
            width = 10, command = self.childWind)

        #Выбор соостава при рассчете положения пиков
        self.label4 = ttk.Label(self.frame, text='Значение состава')        
        self.message_entry4 = ttk.Entry(self.frame, width=22, font=font)     
        self.button4 = ttk.Button(self.frame, text = 'Рассчитать', 
            width = 10) 

        #Выбор угла/d и нумерация пика при расчете состава
        self.label5 = ttk.Label(self.frame, text='Пик')
        self.comb5 = ttk.Combobox(self.frame)
        self.comb5.config(font=font, values= self.peak_list, 
            width = 7)
        self.label15 = ttk.Label(self.frame, text='Значение')
        self.message_entry5 = ttk.Entry(self.frame, font=font, width = 10)     
        self.button5 = ttk.Button(self.frame, width = 10)

        #Отображение результата и действия над ним (сохранение/удаление
        self.label6 = ttk.Label(self.frame, text='Результат')       
        self.text6 = Text(self.frame, width=36, font=font, 
            bg="white", fg='gray')         
        self.button6 = ttk.Button(self.frame, width = 10)
        self.button7 = ttk.Button(self.frame, text = "Очистить",    
            width = 10)
        
        # Scale Фрейм "Справка"
        self.buttonIcon = Button(self.frame, highlightcolor = 'white', 
            bd = 0, relief="flat")
        self.labelInfo = ttk.Label(self.frame) 
        self.infoPeakButton = Button(self.frame, text = "2θ", 
            width = 7, height = 3, bd = 1, highlightcolor = 'black')
        self.infoSolutButton = Button(self.frame, text = "X", 
            width = 7, height = 3, bd = 1, highlightcolor = 'black')
        self.infoSaveButton = Button(self.frame, 
            width = 81, height = 80, bd = 1, highlightcolor = 'black')
        self.infoDeleteButton = Button(self.frame,
            width = 81, height = 80, bd = 1, highlightcolor = 'black')
    
    def help(self, imag1, imag2, imag3, relief="flat", bag="#ccc", fg = "black", 
        font = 'arial 14', ydelt = 150, xdelt = 4, activebackground = "gray"):
        
        #кнопки в справке каждой вкладке соответствует своя

        intro = open('help/intro.txt', 'r', encoding='utf-8')
        word = intro.read()

        self.labelInfo.config(text = word, justify = CENTER, font = 'arial 8')
        self.buttonIcon.config(image = imag3, justify = CENTER, 
            command = self.info, background= bag, relief = relief)
        self.infoPeakButton.config(command = self.infoPeak, 
            background= bag, relief = relief, fg = fg, font = font)
        self.infoSolutButton.config(command = self.infoSolut, 
            background= bag, relief = relief, fg = fg, font = font)
        self.infoSaveButton.config(command = self.infoSave, image = imag1, 
            background= bag, relief = relief)
        self.infoDeleteButton.config(command = self.infoDelete, image = imag2, 
            background= bag, relief = relief)

        self.buttonIcon.place(x= 38, y = 25)
        self.labelInfo.place(x= 58, y = 230)
        self.infoPeakButton.place(x= 51+xdelt, y = 152+ydelt)
        self.infoSolutButton.place(x= 138+xdelt, y = 152+ydelt)
        self.infoSaveButton.place(x= 51+xdelt, y = 235+ydelt)
        self.infoDeleteButton.place(x= 138+xdelt, y = 235+ydelt)       

    # блок открытия сторонних документов с пояснениями
    def info(self):
        Popen(['start', 'help/info.pdf'], shell=True)

    def infoPeak(self):
        Popen(['start', 'help/infoPeak.pdf'], shell=True)

    def infoSolut(self):
        Popen(['start', 'help/infoSolut.pdf'], shell=True)

    def infoSave(self):
        Popen(['start', 'help/infoSave.pdf'], shell=True)

    def infoDelete(self):
        Popen(['start', 'help/infoDelete.pdf'], shell=True)

    #позиционирование всех введенных ранее блоков
    def choisubst(self, textbutt, nclick = 2, state = "normal"):
        """Область выбора вещества"""
        self.click_butt = nclick                 #задает колличество нажатий
        self.button1.config(text = textbutt, command = self.day)
        self.comb1.config(values= self.name_oxides, state = state)

        self.label1.place(x=30, y=25)            #надпись "Навание вещества"
        self.comb1.place(x=30, y=51)             #Выбор вещества
        self.button1.place(x=180,y=50)           #кнопка добавления вещества

    def selectsys(self, text='Полученная смесь'):
        """Очистка полученной системы, выбранных оксидов/оксида"""
        self.label2.config(text = text)

        self.label2.place(x=30, y=80)            #надпись 'Полученная система'
        self.text2.place(x=30, y=103)            #вывод веществ
        self.button2.place(x=180,y=100)          #кнопка удаления полученной 
                                                 #  системы/оксида
    def colculsys(self, deltay = 0):
        """Выбор cистемы исчесления"""
        self.comb3.config(values=self.values_list)
        self.comb3.bind("<<ComboboxSelected>>", self.wave)  

        self.label3.place(x=30, y=130-deltay)    #Надпись "Величина"
        self.comb3.place(x=30,y=153-deltay)      #выбор системы рассчета
        self.button3.place(x=180,y=153-deltay)   #кнопка изменения длины   
                                                 #    волны 

    def selectcompos(self):
        """Выбор состава при рассчете положения пиков"""
        self.button4.config(command = self.rechtPeak)

        self.label4.place(x=30, y=180)            #надпись 'Значение состава'
        self.message_entry4.place(x=30, y= 203)   #ввод состава
        self.button4.place(x=180, y=203)          #кнопка рассчета

    def selectpeak(self, text="Рассчитать"):
        """Ввод угла/d и нумерация пика при расчете состава"""
   
        self.button5.config(text = text)
        if text == "Рассчитать":
            self.button5.config(command = self.rechtSol)
        else:
            self.button5.config(command = self.added)

        self.label5.place(x=30, y=180)             #надпись 'Пик'
        self.comb5.place(x=30, y= 203)             #выбор пика
        self.label15.place(x=100, y=180)           #Надпись "Величина"
        self.message_entry5.place(x=100, y =204)   #поле ввода Значения
        self.button5.place(x=180, y=203)           #кнопка сохранения/удаления

        
    def resultsave(self, text, deltay = 0, heidelt= 0):
        """Отображение результата и действия над ним (сохранение/удаление"""

        self.text6.config(height=13+heidelt)         
        self.button6.config(text = text, command= self.action)
        self.button7.config(command= self.clean)
  
        self.label6.place(x=30, y=233-deltay)  #надпись 'Результат'
        self.text6.place(x= 30, y=255-deltay)  #полученый результат
        self.button6.place(x=180,y=450)        #кнопка сохранения/удаления
                                               #    полученного результата
        self.button7.place(x=30,y=450)         #очистка поля "Результат"

#*******************************************************************************

    def day(self):
        #Ограничение нажатий на кнопку - выбор макс количество оксидов
        if self.click <= self.click_butt:
            if self.click == 1:
                if self.click_butt == 1:
                    self.onlyox()
                else:
                    self.firox()
                self.click += 1
            elif self.click == 2:
                self.secox()
                self.click += 1
        elif self.click_butt == 0:
            self.onlyox()
        elif self.click > self.click_butt:
            mb.showerror("Ошибка", 
                f"Можно выбрать только {self.click_butt} вещество(-а)")

    def firox(self):
        #вставка первого оксида в окно отображения
        self.first_oxide = self.comb1.get()
        text = self.first_oxide+"(x)"
        self.text2.insert(1.0, text)
    
    def secox(self):
        #вставка второго оксида в окно отображения
        self.second_oxide = self.comb1.get()
        text = self.second_oxide+"(1-x) -- "
        self.text2.insert(1.0, text)

    def onlyox(self):
        #вставка единственного оксида в окно отображения
        self.only_oxide = self.comb1.get()

        if self.name == "Запись":
            self.text2.insert(1.0, self.only_oxide)
        else:
            try:
                self.text6.delete(1.0, END)
                if self.comb3.get() == 'd, Å':
                    d = self.data[self.only_oxide].copy()
                elif self.comb3.get() == 'deg(2θ)':
                    self.wavelength = getattr(Wave, "wavelength")
                    d = self.conversion(self.only_oxide, self.wavelength)
                d = self.NaN(d)
                text = self.text(self.only_oxide, d)
                self.text6.insert(1.0, text)
            except:
                mb.showerror("Ошибка", "Ошибка ввода, проверьте поля ввода!")

    def text(self, name, data, sys='d, Å'):
        #чистка лишней информации перед отображением
        if len(data) != 0:
            tx_data = str(data)
            index_1 = tx_data.find('Name')
            index_2 = tx_data.find('(hkl)')+5
            tx_data = (name +"\n" + tx_data[:index_2] + "\t{}\n".format(sys) + 
                tx_data[index_2+1:index_1])
            tx_data += '\n___________________________\n'
        else:
            tx_data = ('При заданных параметрах данные\n'+
            f'о твердом растворе \n{name}'+
            '\nне найдены\n___________________________\n')

        return tx_data

    def wave(self, eventObject):
        #действие comboboxa при выборе система исчестления
        if eventObject.widget.get() == 'deg(2θ)':
            self.childWind()
            
    def childWind(self):
        #отображение окна выбора длины волны
        global Wave 
        Wave = Child(self.frame)

    def rechtPeak(self):
        # Рассчёт положения пиков при известном составе
        try:
            composition = self.message_entry4.get()
            composition = self.chekget(composition)
            O1 = self.first_oxide
            O2 = self.second_oxide
            ddeg = self.comb3.get()
            if ddeg == 'deg(2θ)':
                self.wavelength = getattr(Wave, "wavelength")
            self.result = self.colculation(colctype = 1, name1 = O1, 
                name2= O2, selectcompos = ddeg, composition = composition, 
                wave = self.wavelength)
            text = self.text(self.result[1], self.result[0], ddeg)
            self.text6.insert(1.0, text)
            self.click = 1
        except:
            mb.showerror("Ошибка", "Ошибка ввода, проверьте поля ввода!")

    def rechtSol(self):
        # Рассчёт состава по положению пика
        try:
            value = self.message_entry5.get()
            value = self.chekget(value, typecolc = "sol")
            O1 = self.first_oxide
            O2 = self.second_oxide
            ddeg = self.comb3.get()
            if ddeg == 'deg(2θ)':
                self.wavelength = getattr(Wave, "wavelength")
            peak = self.comb5.get()
            self.result = self.colculation(colctype = 2, name1 = O1, 
                name2= O2, selectcompos = ddeg, peak = peak, value = value,
                wave = self.wavelength)
            text = self.text(self.result[1], self.result[0], "x")
            self.text6.insert(1.0, text)
            self.click = 1
        except:
            mb.showerror("Ошибка", "Ошибка ввода, проверьте поля ввода!")

    def added(self):

        # Действие кнопки "Добавить" при записи новых веществ
        try:
            self.text6.delete(1.0, END)
            value = self.message_entry5.get()
            value = self.chekget(value, typecolc = "sol")
            oxide = self.only_oxide
            peak = self.comb5.get()
            ddeg = self.comb3.get()
            if ddeg == 'deg(2θ)':
                self.wavelength = getattr(Wave, "wavelength")

            self.result = self.adData(oxide, peak, value, ddeg, self.wavelength)

            self.result = self.NaN(self.result)
            text = self.text(oxide, self.result, ddeg)
            self.text6.insert(1.0, text)
        except:
            mb.showerror("Ошибка", "Ошибка ввода, проверьте поля ввода!")
 
    def chekget(self, value, typecolc = "peak"):
        # проверка введенных данных, должно быть без(,)
        value = value.strip()
        if value.find(',') != -1:
            mb.showerror("Ошибка", "Введите десятичное число через точку")
        elif (float(value) < 0 or float(value) > 1) and typecolc == "peak":
            mb.showerror("Ошибка", "Введите десятичное число от 0 до 1")
        elif value[:2] == '00':
            mb.showerror("Ошибка", "Ошибка ввода")
        else:           
            return float(value)

    def action(self):
        # Действие кнопки "Сохранить/Удалить"
        if self.name == "Запись":
            mb.askquestion ( "Сохранение" , "Сохранить полученные данные?")
            self.save()
            self.newlist()
        elif self.name == "Удаление":
            mb.showwarning ( "Удаление" , 
                f"Уверены что хотите удалить информацию о {self.only_oxide}?")
            self.delet(self.only_oxide)
            self.newlist()
            self.clean()
        elif self.name == "Положение":
            solution = float(self.message_entry4.get())
            name = (self.second_oxide + str(solution) + 
                self.first_oxide + str(1-solution) )
            self.csvSave(name, self.result[0])
        elif self.name == "Состав":
            name = (self.message_entry5.get() + "--" + self.second_oxide + "--" +
                self.first_oxide)
            self.csvSave(name, self.result[0])

    def clean(self):
        # Очистка поля результата
        self.text6.delete(1.0, END)
        self.click = 1

    def delete(self):
        #действие кнопки "очистить" при добавлении оксидов
        self.text2.delete(1.0, END)
        self.click = 1

    def newlist(self):
        # Изменение списка оксидов
        self.data = read_table("Data/root/data2.csv", index_col='(hkl)', sep = "\t")
        self.name_oxides = list(self.data.columns[0:])
        self.comb1.config(values= self.name_oxides)