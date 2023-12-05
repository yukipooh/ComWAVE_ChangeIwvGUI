from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import StateEnum
import tkinter as tk
import numpy as np
import os

class MyApp(tk.Frame):
    #コンストラクタ
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.InitParameters()
        self.InitWedgets()
        
    #パラメータを初期化
    def InitParameters(self):
        self.selected_file_path = ""
        self.valueList = []

    #ウィジェットを生成、初期化
    def InitWedgets(self):
        self.canvas = tk.Canvas(self.master)
        self.frame = tk.Frame(self.canvas)

        # Canvasを親とした縦方向のScrollbar
        self.scrollbarY = tk.Scrollbar(self.canvas, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbarX = tk.Scrollbar(self.canvas, orient=tk.HORIZONTAL, command=self.canvas.xview)
        # スクロールの設定
        self.canvas.configure(scrollregion=(0, 0, 1920, 6000))
        self.canvas.configure(yscrollcommand=self.scrollbarX.set)
        self.canvas.configure(yscrollcommand=self.scrollbarY.set)

        #配置
        # self.scrollbarX.pack(side=tk.BOTTOM, fill=tk.X)
        self.scrollbarY.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # Canvas上の座標(0, 0)に対してFrameの左上（nw=north-west）をあてがうように、Frameを埋め込む
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw", width=1920, height=6000)

        #cotファイル選択ボタン
        self.SelectCot = tk.Button(self.frame,bg='#000000',fg='#ffffff',width=12,height=3)
        self.SelectCot["text"] = "SELECT COT FILE" #ボタンのテキスト
        self.SelectCot["command"] = self.LoadCotFile
        self.SelectCot.grid(row=0,column=0)

        #iwvファイル選択ボタン
        self.AddIwv = tk.Button(self.frame,bg='#000000',fg='#ffffff',width=12,height=3)
        self.AddIwv["text"] = "ADD IWV FILE" #ボタンのテキスト
        self.AddIwv["command"] = self.LoadIWVFile
        self.AddIwv.grid(row=0,column=1)

        #波形ファイル一括変更用の波形選択用リストボックス
        self.comboBox = ttk.Combobox(self.frame, width=15, height=5, values=["test1","test2"])
        self.comboBox.grid(row=0, column=2)
        newList = ["a","b","c"]
        self.comboBox["values"] = newList

        #iwvファイル一括変更ボタン
        self.ChangeAllIwvButton = tk.Button(self.frame,bg='#ff4500',fg='#ffffff',width=12,height=3)
        self.ChangeAllIwvButton["text"] = "CHANGE ALL" #ボタンのテキスト
        self.ChangeAllIwvButton["command"] = self.OnClickChangeAllIwvButton
        self.ChangeAllIwvButton.grid(row=0,column=3,padx=10)

        #selectAllボタン
        self.SelectAllButton = tk.Button(self.frame,bg='#000000',fg='#ffffff',width=12,height=3)
        self.SelectAllButton["text"] = "SELECT ALL" #ボタンのテキスト
        self.SelectAllButton["command"] = self.SelectAll
        self.SelectAllButton.grid(row=0,column=4)

        #DeselectAllボタン
        self.DeselectAllButton = tk.Button(self.frame,bg='#000000',fg='#ffffff',width=12,height=3)
        self.DeselectAllButton["text"] = "DESELECT ALL" #ボタンのテキスト
        self.DeselectAllButton["command"] = self.DeselectAll
        self.DeselectAllButton.grid(row=0,column=5)

        #Delayのラベル
        self.DelayLabel = tk.Label(self.frame,text="追加する遅延時間",width=12,height=3)
        self.DelayLabel.grid(row=0,column=6,padx=10)

        #Delay入力テキストボックス
        self.DelayEntry = tk.Entry(self.frame,width=15)
        self.DelayEntry.grid(row=0,column=7)

        #AddDelayAll
        self.AddDelayAllButton = tk.Button(self.frame,bg='#ff4500',fg='#ffffff',width=12,height=3)
        self.AddDelayAllButton["text"] = "ADD DELAY ALL" #ボタンのテキスト
        self.AddDelayAllButton["command"] = self.OnClickAddDelayAllButton
        self.AddDelayAllButton.grid(row=0,column=8,padx=15)


    #一括変更用のコンボボックスの選択肢を更新する
    def UpdateComboBoxValues(self):
        self.comboBox["values"] = self.valueList
        self.comboBox.current(0)

    #選択状態のエレメントの波形ファイルを変更する
    def OnClickChangeAllIwvButton(self):
        changeList = []
        for i in range(self.elementNum):
            if self.elementButtonClicked[i] == True:
                changeList.append(i + 1)
                self.elementComboBoxes[i].set(self.comboBox.get())
        self.ChangeElementIWV(changeList, self.comboBox.get())

    #指定された探触子の波形ファイルを指定されたものに変更する。elementIndexesには変更したい探触子番号が入ったリストを渡す。
    def ChangeElementIWV(self, elementIndexes, iwvName):
        # print(iwvName)
        # print(elementIndexes)
        writeLines = []
        # with open(self.selectedCotFilePath, encoding="utf-8") as loadedFile, open(self.selectedCotFilePath, "w") as writer:
        with open(self.selectedCotFilePath, encoding="utf-8") as loadedFile:
            for i in range(self.elementStartColumn - 1):
                #element部分の行になるまで読み込む
                line = loadedFile.readline()
                writeLines.append(line)
                # writer.write(line)
            #素子分ループ回して該当の素子の波形ファイルを変える
            for i in range(self.elementNum):
                line = loadedFile.readline()
                if ((i + 1) in elementIndexes) == True:
                    parameters = line[:-1].split(",")
                    # print(line)
                    # print(parameters[5])
                    line = line.replace(parameters[5], iwvName)
                    # print(line)
                # writer.write(line)
                writeLines.append(line)
            while line:
                line = loadedFile.readline()
                writeLines.append(line)
        with open(self.selectedCotFilePath, "w") as writer:
            for line in writeLines:
                print(line)
                writer.write(line)

    #波形ファイルを読み込みそのファイル名をコンボボックスに追加する。
    def LoadIWVFile(self):
        fTyp = [("iwvファイル", "*.iwv")]
        if self.selected_file_path == "":
            iDir = os.path.abspath(os.path.dirname(__file__))
        else:
            iDir = os.path.abspath(os.path.dirname(self.selected_file_path))
        self.selected_file_path = filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
        if self.selected_file_path == "":
            print("unselected")
            return
        iwvName = os.path.basename(self.selected_file_path)
        if (iwvName in self.valueList) == False:
            self.valueList.append(iwvName)
            self.UpdateComboBoxValues()
            self.UpdateIWVBoxValues()
        else:
            print("既に存在しています")

    #Cotファイルを読み込みそのデータからエレメントのボタンやiwv選択用コンボボックスを表示する
    def LoadCotFile(self):
        fTyp = [("cotファイル","*.cot")]
        if self.selected_file_path == "":
            iDir = os.path.abspath(os.path.dirname(__file__))
        else:
            iDir = os.path.abspath(os.path.dirname(self.selected_file_path))
        self.selected_file_path = filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
        self.selectedCotFilePath = self.selected_file_path
        loadedFile = open(self.selected_file_path, encoding="utf-8")
        line = loadedFile.readline()
        currentRow = 1
        self.elementParamList = []
        parameters = []
        state = StateEnum.State.BeforeELD
        while line:
            #[:-1]で改行コードだけ取り除ける
            parameters = line[:-1].split(",")
            if parameters[0] == "ELD":
                if state == StateEnum.State.BeforeELD:
                    self.elementStartColumn = currentRow
                    state = StateEnum.State.InELD
                self.elementParamList.append(parameters)
                #リスト内に同じiwvファイルが存在しなかったら
                if (parameters[5] in self.valueList) == False:
                    self.valueList.append(parameters[5])
            else:
                if state == StateEnum.State.InELD:
                    state = StateEnum.State.AfterELD
                    self.elementEndColumn = currentRow - 1
                    break
            line = loadedFile.readline()
            currentRow += 1

        self.elementNum = self.elementEndColumn - self.elementStartColumn + 1

        # print(self.elementStartColumn)
        # print(self.elementEndColumn)
        # print(self.elementParamList)
        self.ShowElementUI()
        self.ShowIWVBox()
        self.UpdateComboBoxValues()
        loadedFile.close()
        
    #エレメントごとのボタンを表示する
    def ShowElementUI(self):
        counter = 1
        self.elementButton = []
        self.elementButtonClicked = []
        for params in self.elementParamList:
            #Elementボタン
            self.elementButton.append(tk.Button(self.frame,bg='#696969',fg='#ffffff',width=12,height=2)) 
            self.elementButtonClicked.append(False)
            self.elementButton[counter - 1]["text"] = "Element " + str(counter) #ボタンのテキスト
            self.elementButton[counter - 1]["command"] = lambda c=counter: self.OnClickElementButton(c)
            self.elementButton[counter - 1].grid(column=0, row=counter, padx=1, pady=1)
            counter += 1

    #エレメントのボタンを押された時の処理、選択状態/非選択状態を切り替える。
    def OnClickElementButton(self, elementIndex):
        self.elementButtonClicked[elementIndex - 1] = not self.elementButtonClicked[elementIndex - 1] #bool反転
        # print(self.elementButtonClicked[elementIndex - 1])
        if self.elementButtonClicked[elementIndex - 1] == True:
            self.elementButton[elementIndex - 1]["bg"] = "#008080"
        else:
            self.elementButton[elementIndex - 1]["bg"] = "#696969"

    #すべてのエレメントを選択状態に
    def SelectAll(self):
        for i in range(self.elementNum):
            self.elementButtonClicked[i] = True
            self.elementButton[i]["bg"] = "#008080"

    #すべてのエレメントを非選択状態に
    def DeselectAll(self):
        for i in range(self.elementNum):
            self.elementButtonClicked[i] = False
            self.elementButton[i]["bg"] = "#696969"

    #AddDelayAllButtonが押されたときのオンクリック処理、　現在選択されている素子のリストを渡して遅延時間を指定秒数足し合わせる。
    def OnClickAddDelayAllButton(self):
        changeList = []
        for i in range(self.elementNum):
            if self.elementButtonClicked[i] == True:
                changeList.append(i + 1)
        self.AddDelayAll(changeList)

    #指定された全ての素子の遅延時間を指定秒数足し合わせる。elementIndexesには変更したい素子番号が入ったリストを渡す。
    def AddDelayAll(self, elementIndexes):
        writeLines = []
        #入力された文字がFloatに変換可能でない場合は処理を行わない
        if self.isFloat(self.DelayEntry.get()) == False:
            return
        additiveDelay = float(self.DelayEntry.get())
        with open(self.selectedCotFilePath, encoding="utf-8") as loadedFile:
            for i in range(self.elementStartColumn - 1):
                #element部分の行になるまで読み込む
                line = loadedFile.readline()
                writeLines.append(line)
            #素子分ループ回して該当の素子の遅延時間を変える
            for i in range(self.elementNum):
                line = loadedFile.readline()
                if ((i + 1) in elementIndexes) == True:
                    parameters = line[:-1].split(",")
                    # line = line.replace(parameters[6], '{:E}'.format(float(parameters[6]) + additiveDelay))
                    line = line.replace(parameters[6], np.format_float_scientific(float(parameters[6]) + additiveDelay, precision=7,exp_digits=3, min_digits=6))
                writeLines.append(line)
            while line:
                line = loadedFile.readline()
                writeLines.append(line)
        with open(self.selectedCotFilePath, "w") as writer:
            for line in writeLines:
                print(line)
                writer.write(line)

    #Elementごとの波形ファイル設定用コンボボックスを表示
    def ShowIWVBox(self):
        self.elementComboBoxes = []
        self.elementVariables = []
        counter = 0
        for item in self.elementParamList:
            #波形ファイル一括変更用の波形選択用リストボックス
            iwvName = item[5]
            self.elementVariables.append(tk.StringVar())
            self.elementComboBoxes.append(ttk.Combobox(self.frame, textvariable=self.elementVariables[counter], width=15, height=5, values=self.valueList))
            self.elementComboBoxes[counter].set(iwvName)
            self.elementComboBoxes[counter].grid(row=counter + 1, column=1)
            #Comboboxの値が選択されたときの処理を設定
            self.elementComboBoxes[counter].bind('<<ComboboxSelected>>', lambda e, c=counter: self.ChangeElementIWV([c + 1], self.elementComboBoxes[c].get()))
            # self.elementComboBoxes[counter].bind('<<ComboboxSelected>>', lambda e, c=counter: print(self.elementComboBoxes[c].get()))
            counter += 1

    def UpdateIWVBoxValues(self):
        for i in range(self.elementNum):
            self.elementComboBoxes[i]["values"] = self.valueList

    #アプリ終了
    def QuitApp(self):
        # print("quit this App")
        self.master.destroy()

    #テキストがFloatに変換可能かどうか判定する
    def isFloat(self, text):
        try:
            float(text)
        except ValueError:
            return False
        else:
            return True

    