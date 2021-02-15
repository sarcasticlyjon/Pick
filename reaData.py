from pandas import read_csv, read_table, DataFrame as dt, Series as se
from math import asin, degrees, sin, radians
from tkinter import messagebox as mb

class Data():

    '''Класс отвечает за все манипуляции с данными'''

    def __init__(self):
        self.data = read_table("Data/root/data2.csv", index_col='(hkl)', 
            sep = "\t")
        self.datawave= read_csv("Data/root/wavelength.csv", index_col='line')
        self.lenght = list(self.datawave.index)
        self.name_oxides = list(self.data.columns[0:])
        self.peak_list = list(self.data.index)
        self.values_list = ('d, Å', 'deg(2θ)')
        self.peak_data = {}
        self.wavelength = float()

    def NaN(self, data):
        #Убираем в датафрейме пустые строки
        return data[data.notnull()]

    def colculation(self, name1, name2, selectcompos, colctype, wave, 
        composition=None, peak=None, value=None):
        # colctype = номер рассчета
        # selectcompos = выбор системы измерения ("deg"/"d")
        # composition = состав (проверка значения должна быть) в виде 0.2
        # peak = пик
        # value = положение пика в выбранной системе отсчета
        # name = имена оксидов

        # 1) рассчет положения пиков исходя из состава     
        if colctype == 1:
            oxid_first = name1
            oxid_second = name2
            solution = float(composition)

            #получаем имя рассчитываемого твердого раствора
            name = (oxid_second + "({:.2f})".format(1-solution) + "--" + 
                oxid_first + "({:.2f})\n".format(solution))
            self.data[name] = None

            #сам рассчет по Вейгарду
            self.data[name] = (solution * self.data[oxid_first] + 
                (1-solution) * self.data[oxid_second])

            #реакция на выбор системы рассчета 
            if selectcompos == "deg(2θ)":
                self.data[name] = self.conversion(name, wave)

            result = self.NaN(self.data[name])
            
            return result.round(4), name

        # 2) рассчет состава исходя из положения пиков
        elif colctype == 2:
            oxid_first = name1
            oxid_second = name2
            name = oxid_second + "(1-x)" + oxid_first + "(x)"

            #пересчет deg в d, все данные в d, все считается в d, потом конверт.
            if selectcompos == "deg(2θ)":
                deg = radians(value)
                d = 2*sin(deg/2)
                light = float(wave)
                d = light / d
            else:
                d = value

            self.data[name] = None 
            #если пик был выставлен, то расчет линеен:
            if peak: 
                result1 = (
                (d-(self.data[oxid_second].loc[peak]))
                /((self.data[oxid_first].loc[peak]) -
                 (self.data[oxid_second].loc[peak]))
                )
            #если пик не известен, то рассчет ведется по всем столбцам:
            else: 
                new_data = self.data[oxid_first] - self.data[oxid_second]
                new_data = self.NaN(new_data)
                new_index = list(new_data.index) #нужен список пиков, 
                                                 #которые не дадут при 
                                                 #операции с ними None
                
                self.data[name]= (
                    (d-self.data[oxid_second])/
                    (self.data[oxid_first] - self.data[oxid_second])
                    )
                data2 = self.NaN(self.data[name])

                #мы знаем, что состав от 0 до 1, ищем его в данных
                result1 = data2[(data2 >=0) & (data2 <= 1)]
                
            return result1, name


    def adData(self, oxide, peak, value, ddeg, wave):
        # Добавление/Изменение данных
        if oxide in list(self.data.columns[0:]):
            if ddeg == 'deg(2θ)':
                deg = radians(value)
                d = 2*sin(deg/2)
                light = float(wave)
                d = light / d
                self.data[oxide].loc[peak] = d
                data = self.conversion(oxide, wave)
            else:
                self.data[oxide].loc[peak] = value
        
        else:
            self.data[oxide] = None
            self.peak_data[peak] = value
            series_peak_data = se(self.peak_data)
            self.data[oxide] = series_peak_data
        
        data = self.data[oxide]

        return data.round(4)     

    def save(self):
        #Сохранение данных, при добавлении
        self.data.to_csv("Data/root/data2.csv", index_label='(hkl)', sep= '\t')

    def conversion(self, name, wave):
        #Перевод deg в d и обратно
        self.wavelength = wave
        data = self.data[name].copy()
        data = data**(-1)
        for i in data.index:
            data.loc[i] = 2* degrees(asin(self.wavelength * 
                0.5 * data.loc[i]))
        return data.round(4)

    def csvSave(self, name, data):
        #Сохранение данных, при рассчете положения пиков тв.р-ов и состава.
        mb.askquestion("Сохранение" , "Сохранить полученные данные?")
        data.to_csv(f"Data/{name}.csv",  index_label='(hkl)', sep="\t")
        mb.showinfo('Информация', "Сохранение произведено в папку Data")

    def delet(self, name): 
        #удаление данных
        del self.data[name]
        self.data.to_csv("Data/root/data2.csv", index_label='(hkl)', sep = "\t")
        self.name_oxides = list(self.data.columns[0:])