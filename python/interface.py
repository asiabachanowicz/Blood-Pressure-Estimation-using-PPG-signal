from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import pandas
import numpy
import sklearn
from keras.models import Sequential, load_model
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.preprocessing import *
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.geometry("800x800")  # You want the size of the app to be 800x800
        self.resizable(0, 0)  # Don't allow resizing in the x or y direction
        self.iconbitmap("bp-icon.ico")
        self.title("Estymacja ciśnienia krwi")

        self.labelFrame1 = ttk.LabelFrame(self, text="Wybierz sygnał")
        self.labelFrame1.place(x=100, y=50)

        self.labelFrame2 = ttk.LabelFrame(self, text="Wybierz rodzaj sieci neuronowej")
        self.labelFrame2.place(x=290, y=50)

        self.labelFrame3 = ttk.LabelFrame(self, text="Rozpocznij pomiar")
        self.labelFrame3.place(x=600, y=50)

        self.labelFrame4 = ttk.LabelFrame(self, text="Ciśnienie krwi", width=680, height=270)
        self.labelFrame4.place(x=60, y=170)

        self.labelFrame5 = ttk.LabelFrame(self, text="Błąd estymacji", width=680, height=270)
        self.labelFrame5.place(x=60, y=450)

        self.fig = plt.figure(num=None, figsize=(8, 2.8), dpi=80)
        self.fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(self.fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().place(x=80, y=195)

        self.fig = plt.figure(num=None, figsize=(8, 2.8), dpi=80)
        self.fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(self.fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().place(x=80, y=475)

        self.v = IntVar()

        self.radiobutton1 = ttk.Radiobutton(self.labelFrame2, variable=self.v, value=1, text="Ciśnienie skurczowe",
                                        command=self.splitDataSys)
        self.radiobutton1.pack()
        self.radiobutton2 = ttk.Radiobutton(self.labelFrame2, variable=self.v, value=2, text="Ciśnienie rozkurczowe",
                                        command=self.splitDataDia)
        self.radiobutton2.pack()
        self.radiobutton3 = ttk.Radiobutton(self.labelFrame2, variable=self.v, value=3,
                                        text="Ciśnienie skurczowe i rozkurczowe",
                                        command=self.splitDataSysDia)
        self.radiobutton3.pack()
        self.createMenu()
        self.button1()
        self.button2()
        self.button3()
        self.button4()
        self.button5()

        self.button2.configure(state=DISABLED)
        self.button3.configure(state=DISABLED)
        self.button4.configure(state=DISABLED)
        self.radiobutton1.configure(state=DISABLED)
        self.radiobutton2.configure(state=DISABLED)
        self.radiobutton3.configure(state=DISABLED)

    def createMenu(self):
        menuBar = Menu(self)
        self.config(menu=menuBar)

        # MENUBAR
        file_menu = Menu(menuBar, tearoff=0)

        menuBar.add_cascade(label="Plik", menu=file_menu)
        file_menu.add_command(label='Nowy', command=self.reset)
        file_menu.add_separator()
        file_menu.add_command(label="Wyjdź z programu", command=self.ExitApplication)
        help_menu = Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label='Pomoc', menu=help_menu)
        help_menu.add_command(label='Instrukcja', command=self.instruction)
        help_menu.add_command(label='O programie', command=self.aboutapp)

    def ExitApplication(self):
        MsgBox = messagebox.askquestion('Uwaga', 'Czy na pewno chcesz opuścić program?',
                                           icon='warning')
        if MsgBox == 'yes':
            root.destroy()
        else:
            messagebox.showinfo('Info', 'Powrócisz teraz do ekranu aplikacji')

    def button1(self):
        self.button1 = ttk.Button(self.labelFrame1, text="Przeglądaj pliki", command=self.fileDialog)
        self.button1.pack()

    def fileDialog(self):
        self.filename = filedialog.askopenfilename(initialdir="C:/Users/Asia/Desktop/Praca/python",
                                                   title="Select A File", filetype=(("csv files", "*.csv"),
                                                   ("all files", "*.*")))
        # import data
        self.data = pandas.read_csv(self.filename, sep=",")
        self.button1.configure(state=DISABLED)
        self.radiobutton1.configure(state=NORMAL)
        self.radiobutton2.configure(state=NORMAL)
        self.radiobutton3.configure(state=NORMAL)

    # systolic blood pressure
    def splitDataSys(self):
        self.type = 0
        self.data = self.data[["cp", "st", "dt", "sw10", "dw10", "sw10+dw10", "dw10/sw10", "sw25", "dw25",
                               "sw25+dw25", "dw25/sw25", "sw33", "dw33", "sw33+dw33", "dw33/sw33", "sw50",
                               "dw50", "sw50+dw50", "dw50/sw50", "sw66", "dw66", "sw66+dw66", "dw66/sw66",
                               "sw75", "dw75", "sw75+dw75", "dw75/sw75", "sys"]]
        # lock buttons
        self.radiobutton1.configure(state=DISABLED)
        self.radiobutton2.configure(state=DISABLED)
        self.radiobutton3.configure(state=DISABLED)
        self.button2.configure(state=NORMAL)

        # split data for test
        self.predict = "sys"
        self.X = numpy.array(self.data.drop([self.predict], 1))
        self.y = numpy.array(self.data[self.predict])
        self.X_train, self.X_test, self.y_train, self.y_test = sklearn.model_selection.train_test_split(self.X, self.y,

                                                                                                   test_size=10)
        # data normalization
        scaler = StandardScaler()
        scaler.fit(self.X)
        self.X_standardized = scaler.transform(self.X)
        self.X_test_standardized = scaler.transform(self.X_test)

        # load systolic bp model
        self.model = load_model('model_55.h5')
        self.model.load_weights('weights_55.h5')

    # diastolic blood pressure
    def splitDataDia(self):
        self.type = 1
        self.data = self.data[["cp", "st", "dt", "sw10", "dw10", "sw10+dw10", "dw10/sw10", "sw25", "dw25",
                               "sw25+dw25", "dw25/sw25", "sw33", "dw33", "sw33+dw33", "dw33/sw33", "sw50",
                               "dw50", "sw50+dw50", "dw50/sw50", "sw66", "dw66", "sw66+dw66", "dw66/sw66",
                               "sw75", "dw75", "sw75+dw75", "dw75/sw75", "dia"]]
        # lock buttons
        self.radiobutton1.configure(state=DISABLED)
        self.radiobutton2.configure(state=DISABLED)
        self.radiobutton3.configure(state=DISABLED)
        self.button2.configure(state=NORMAL)

        # split data for test
        self.predict = "dia"
        self.X = numpy.array(self.data.drop([self.predict], 1))
        self.y = numpy.array(self.data[self.predict])
        self.X_train, self.X_test, self.y_train, self.y_test = sklearn.model_selection.train_test_split(self.X, self.y,
                                                                                                        test_size=10)
        # data normalization
        scaler = StandardScaler()
        scaler.fit(self.X)
        self.X_standardized = scaler.transform(self.X)
        self.X_test_standardized = scaler.transform(self.X_test)

        # load diastolic bp model
        self.model = load_model('model_52.h5')
        self.model.load_weights('weights_52.h5')

    #     systolic and diastolic blood pressure
    def splitDataSysDia(self):
        self.type = 2
        self.data = self.data[["cp", "st", "dt", "sw10", "dw10", "sw10+dw10", "dw10/sw10", "sw25", "dw25",
                               "sw25+dw25", "dw25/sw25", "sw33", "dw33", "sw33+dw33", "dw33/sw33", "sw50",
                               "dw50", "sw50+dw50", "dw50/sw50", "sw66", "dw66", "sw66+dw66", "dw66/sw66",
                               "sw75", "dw75", "sw75+dw75", "dw75/sw75", "sys", "dia"]]
        # lock buttons
        self.radiobutton1.configure(state=DISABLED)
        self.radiobutton2.configure(state=DISABLED)
        self.radiobutton3.configure(state=DISABLED)
        self.button2.configure(state=NORMAL)
        # split data for test
        self.predict1 = "sys"
        self.predict2 = "dia"
        self.X = numpy.array(self.data.drop([self.predict1, self.predict2], 1))
        self.y = numpy.array(self.data[[self.predict1, self.predict2]])

        # Splitting the total data into subsets: 70% - training, 30% - testing
        self.X_train, self.X_test, self.y_train, self.y_test = sklearn.model_selection.train_test_split(self.X, self.y,
                                                                                                        test_size=10)
        # data normalization
        scaler = StandardScaler()
        scaler.fit(self.X)
        self.X_standardized = scaler.transform(self.X)
        self.X_test_standardized = scaler.transform(self.X_test)
        # load sys dia bp model
        self.model = load_model('model_81.h5')
        self.model.load_weights('weights_81.h5')

    def startEstimation(self):
        # lock/unlock buttons
        self.button2.configure(state=DISABLED)
        self.button3.configure(state=NORMAL)
        self.button4.configure(state=NORMAL)
        # prediction
        self.y_pred = self.model.predict(self.X_test_standardized)

        # sys & dia blood pressure
        if self.type == 2:
            self.score1 = numpy.sqrt(sklearn.metrics.mean_squared_error(self.y_pred[:, 0], self.y_test[:, 0]))
            self.score2 = numpy.sqrt(sklearn.metrics.mean_squared_error(self.y_pred[:, 1], self.y_test[:, 1]))

            # estimation plot
            self.fig1 = plt.figure(num=None, figsize=(8, 2.8), dpi=80)
            self.fig1.add_subplot(111)
            t = list(range(len(self.y_pred[:, 0])))
            plt.scatter(t, self.y_pred[:, 0], label="skurczowe oszacowane")
            plt.scatter(t, self.y_test[:, 0], label="skurczowe rzeczywiste")
            plt.scatter(t, self.y_pred[:, 1], label="rozkurczowe oszacowane")
            plt.scatter(t, self.y_test[:, 1], label="rozkurczowe rzeczywiste")
            plt.xlabel("nr próbki")
            plt.ylabel("ciśnienie krwi [mmHg]")
            plt.xticks(t)
            plt.legend(loc='upper right')
            plt.tight_layout()
            self.canvas2 = FigureCanvasTkAgg(self.fig1, master=self)
            self.canvas2.draw()
            self.canvas2.get_tk_widget().place(x=80, y=195)

            self.y_pred1 = self.y_pred[:, 0].ravel()
            self.error1 = self.y_pred1 - self.y_test[:, 0]
            self.y_pred2 = self.y_pred[:, 1].ravel()
            self.error2 = self.y_pred2 - self.y_test[:, 1]

            # error histogram
            self.fig2 = plt.figure(num=None, figsize=(8, 2.8), dpi=80)
            self.fig2.add_subplot(111)
            plt.hist(self.error1, alpha=0.5, label='ciśnienie skurczowe')
            plt.hist(self.error2, alpha=0.5, label='ciśnienie rozkurczowe')
            plt.legend(loc='upper right')
            plt.xlabel("Błąd estymacji ciśnienia krwi[mmHg]")
            plt.ylabel("Liczba próbek")
            plt.tight_layout()
            self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self)
            self.canvas2.draw()
            self.canvas2.get_tk_widget().place(x=80, y=475)

        # sys or dia blood pressure
        if (self.type == 0 or self.type == 1):
            self.score = numpy.sqrt(sklearn.metrics.mean_squared_error(self.y_pred, self.y_test))

            #estimation plot
            self.fig1 = plt.figure(num=None, figsize=(8, 2.8), dpi=80)
            self.fig1.add_subplot(111)
            t = list(range(len(self.y_pred)))
            plt.scatter(t, self.y_pred, label="ciśnienie oszacowane")
            plt.scatter(t, self.y_test, label="ciśnienie rzeczywiste")
            plt.xlabel("nr próbki")
            plt.ylabel("ciśnienie krwi [mmHg]")
            plt.xticks(t)
            plt.legend(loc='upper right')
            plt.tight_layout()
            self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self)
            self.canvas1.draw()
            self.canvas1.get_tk_widget().place(x=80, y=195)

            self.y_pred = self.y_pred.ravel()
            self.error = self.y_pred - self.y_test

            # error histogram
            self.fig2 = plt.figure(num=None, figsize=(8, 2.8), dpi=80)
            self.fig2.add_subplot(111)
            plt.hist(self.error, alpha=0.5)
            plt.xlabel("Błąd estymacji ciśnienia krwi[mmHg]")
            _ = plt.ylabel("Liczba próbek")
            plt.tight_layout()
            self.canvas1 = FigureCanvasTkAgg(self.fig2, master=self)
            self.canvas1.draw()
            self.canvas1.get_tk_widget().place(x=80, y=475)

    def button2(self):
        self.button2 = ttk.Button(self.labelFrame3, text="START", command=self.startEstimation)
        self.button2.pack()

    def button3(self):
        self.button3 = ttk.Button(self, text="Wyniki", command=self.results)
        self.button3.place(x=250, y=740)

    def button4(self):
        self.button4 = ttk.Button(self, text="Zapisz", command=self.save)
        self.button4.place(x=350, y=740)

    def button5(self):
        self.button5 = ttk.Button(self, text="Nowy", command=self.reset)
        self.button5.place(x=450, y=740)

    def instruction(self):
        novi = Toplevel()
        canvas = Canvas(novi, width=421, height=351)
        canvas.pack(expand=YES, fill=BOTH)
        gif1 = PhotoImage(file='instrukcja.gif')
        # image not visual
        canvas.create_image(10, 10, image=gif1, anchor=NW)
        # assigned the gif1 to the canvas object
        canvas.gif1 = gif1

    def aboutapp(self):
        window = Tk()
        window.title("O programie")
        window.geometry('500x200')
        window.resizable(0, 0)  # Don't allow resizing in the x or y direction
        window.iconbitmap("info-icon.ico")

        self.label = ttk.Label(window, text="Program do estymacji ciśnienia krwi z sygnału PPG"
                               "\n"
                               "\nJoanna Bachanowicz"        
                               "\nInżynieria biomedyczna"
                               "\nPolitechnika Gdańska Wydział ETI"
                               "\n"
                               "\nGdańsk, 2019")
        self.label.place(x=55, y=30)

        button1 = ttk.Button(window, text="Zamknij", command=window.destroy)
        button1.place(x=215, y=140)

    def results(self):
        window = Tk()
        window.title("Wyniki")
        window.geometry('500x500')
        window.resizable(0, 0)  # Don't allow resizing in the x or y direction
        window.iconbitmap("bp-icon.ico")

        self.labelFrame1 = ttk.LabelFrame(window, text="Rzeczywiste ciśnienie krwi:", width=160, height=250)
        self.labelFrame1.place(x=55,y=30)

        self.labelFrame2 = ttk.LabelFrame(window, text="Oszacowane ciśnienie krwi:", width=160, height=250)
        self.labelFrame2.place(x=280,y=30)

        self.labelFrame3 = ttk.LabelFrame(window, text="Podsumowanie błędu sieci:", width=385, height=110)
        self.labelFrame3.place(x=55, y=300)

        button1 = ttk.Button(window, text="Zamknij", command=window.destroy)
        button1.place(x=210, y=430)

        # round results
        if (self.type == 0 or self.type == 1):
            for i in list(range(len(self.y_pred))):
                self.y_pred[i] = int(round(self.y_pred[i]))
        if (self.type ==2):
            for i in range(len(self.y_pred)):
                for j in range(len(self.y_pred[i])):
                    self.y_pred[i][j] = int(round(self.y_pred[i][j]))

        self.wyniki = self.y_pred.tolist()

        # for i in range(len(self.wyniki)):
        for i in range(10):
            self.str1 = str(self.wyniki[i]).strip('[]')
            self.Label1 = ttk.Label(self.labelFrame2, text=self.str1)
            self.Label1.pack()

        self.real = self.y_test.tolist()
        self.str2 = str(self.real).strip('[]')

        self.real = self.y_test.tolist()

        # for i in range(len(self.real)):
        for i in range(10):
            self.str2 = str(self.real[i]).strip('[]')
            self.Label2 = ttk.Label(self.labelFrame1, text=self.str2)
            self.Label2.pack()
        if self.type == 2:
            self.Label = ttk.Label(self.labelFrame3, text="RMSE- ciśnienie skurczowe: 6.92")
            self.Label.place(x=10, y=10)
            self.Label = ttk.Label(self.labelFrame3, text="RMSE- ciśnienie rozkurczowe: 3.57")
            self.Label.place(x=10, y=30)
        if self.type == 0:
            self.Label = ttk.Label(self.labelFrame3, text="RMSE- ciśnienie skurczowe: 7.12")
            self.Label.place(x=10, y=10)
        if self.type == 1:
            self.Label = ttk.Label(self.labelFrame3, text="RMSE- ciśnienie rozkurczowe: 3.52")
            self.Label.place(x=10, y=10)
        if (self.type == 0 or self.type == 1):
            self.Label = ttk.Label(self.labelFrame3, text=f"RMSE test: {self.score}")
            self.Label.place(x=10, y=40)
        if self.type == 2:
            self.Label1 = ttk.Label(self.labelFrame3, text=f"RMSE test - ciśnienie skurczowe: {self.score1}")
            self.Label1.place(x=10, y=50)
            self.Label2 = ttk.Label(self.labelFrame3, text=f"RMSE test - ciśnienie skurczowe: {self.score2}")
            self.Label2.place(x=10, y=70)

    def save(self):
        if (self.type == 0 or self.type ==1):
            df = pandas.DataFrame({"Rzeczywiste ciśnienie krwi": self.y_test, "Oszacowane ciśnienie krwi": self.y_pred})
            df.to_csv("estimated.csv", index=False)
            messagebox.showinfo('Info', 'Zapisano wyniki')
        if self.type == 2:
            df = pandas.DataFrame({"Rzeczywiste skurczowe ciśnienie krwi": self.y_test[:,0],
                                   "Oszacowane skurczowe ciśnienie krwi": self.y_pred[:,0],
                                   "Rzeczywiste rozkurczowe ciśnienie krwi": self.y_test[:,1],
                                   "Oszacowane rozkurczowe ciśnienie krwi": self.y_pred[:,1]})
            df.to_csv("estimated1.csv", index=False)
            messagebox.showinfo('Info', 'Zapisano wyniki')
        # else:
        #     messagebox.showinfo('Info', 'Brak wyników do zapisu')

    def reset(self):
        self.fig = plt.figure(num=None, figsize=(8, 2.8), dpi=80)
        self.fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(self.fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().place(x=80, y=195)

        self.fig = plt.figure(num=None, figsize=(8, 2.8), dpi=80)
        self.fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(self.fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().place(x=80, y=475)

        self.button1.configure(state=NORMAL)
        self.button2.configure(state=DISABLED)
        self.button3.configure(state=DISABLED)
        self.button4.configure(state=DISABLED)
        self.radiobutton1.configure(state=DISABLED)
        self.radiobutton2.configure(state=DISABLED)
        self.radiobutton3.configure(state=DISABLED)
        self.y_pred = 0
        self.data = []
        self.predict = 0
        self.X = 0
        self.y = 0


root = Root()
root.mainloop()