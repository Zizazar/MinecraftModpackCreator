import requests
from bs4 import BeautifulSoup
import sys
import tkinter as tk
from tkinter import ttk
import os

window = tk.Tk()

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        mainFrame = tk.Frame(master=window)
        mainFrame.pack(side=tk.TOP)
        labelFrame = tk.Label(master=mainFrame)
        labelFrame.pack()
        DownloadLabel = tk.Label(master=labelFrame, text="Репозиторий модов", width=32)
        DownloadLabel.pack(side=tk.LEFT)
        DownloadedLabel = tk.Label(master=labelFrame, text="Скаченые моды", width=32)
        DownloadedLabel.pack(side=tk.LEFT)
        DownloadList = tk.Listbox(master=mainFrame, width=32, height=16)
        DownloadList.pack(side=tk.LEFT)
        DownloadedList = tk.Listbox(master=mainFrame, width=33, height=16)
        DownloadedList.pack(side=tk.LEFT)


        buttomFrame = tk.Frame(master=window)
        buttomFrame.pack(side=tk.LEFT)
        buttom2Frame = tk.Frame(master=window)
        buttom2Frame.pack(side=tk.LEFT)
        butDownload = tk.Button(master=buttomFrame, text="Скачать", width=32)
        butDownload.pack()
        Version = ttk.Combobox(master=buttomFrame, width=12, values=["1.19", "1.12.2"])
        Version.pack(side=tk.LEFT)
        def updateList():
            DownloadList.delete(0,tk.END)
            for i in range(len(ParseMods(Version.get())[0])):
                DownloadList.insert(0, ParseMods(Version.get())[0][i])

        butUpdate = tk.Button(master=buttomFrame, text="Обновить список", width=15, command= updateList)
        butUpdate.pack(side=tk.LEFT)
        butDelete = tk.Button(master=buttom2Frame, text="Удалить", width=32)
        butDelete.pack()
        butActivated = tk.Button(master=buttom2Frame, text="Выключить мод", width=32)
        butActivated.pack()



def ParseMods(mc_version):
    url = 'https://github.com/Zizazar/MinecraftModpackCreator/releases/tag/' + mc_version
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    modsRaw = soup.find_all('span', class_= "px-1 text-bold")
    outUrl = []
    mods = []
    for i in range(len(modsRaw) - 2):
        print(modsRaw[i].text)
        mods.append(modsRaw[i].text)
        outUrl.append('https://github.com/Zizazar/MinecraftModpackCreator/releases/download/{0}/{1}'.format(mc_version, mods[i]))
    return mods,outUrl



if __name__ == "__main__":
    application = App()
    application.mainloop()



