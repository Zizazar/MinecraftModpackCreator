import requests
from bs4 import BeautifulSoup
import sys
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
import tkinter.filedialog as fd
import os
import configparser


outUrl = []
directory = ''
config = configparser.ConfigParser()
config.read('Config.ini')
VersionVariations = config['DEFAULT']['versions'].split(',')


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        mainFrame = tk.Frame(master=window)
        mainFrame.pack(side=tk.TOP)
        labelFrame = tk.Label(master=mainFrame)
        labelFrame.pack()
        DownloadLabel = tk.Label(master=labelFrame, text="Репозиторий модов", width=32)
        DownloadLabel.pack(side=tk.LEFT)
        DownloadedLabel = tk.Label(master=labelFrame, text="Установленые моды", width=32)
        DownloadedLabel.pack(side=tk.LEFT)
        DownloadList = tk.Listbox(master=mainFrame, width=32, height=16)
        DownloadList.pack(side=tk.LEFT)
        DownloadedList = tk.Listbox(master=mainFrame, width=33, height=16)
        DownloadedList.pack(side=tk.LEFT)
        buttomFrame = tk.Frame(master=window)
        buttomFrame.pack(side=tk.LEFT)
        buttom2Frame = tk.Frame(master=window)
        buttom2Frame.pack(side=tk.LEFT)

        def Download():
            url = 'https://github.com/Zizazar/MinecraftModpackCreator/releases/download/{0}/{1}'.format(Version.get(), DownloadList.get(DownloadList.curselection()))
            print(url)
            if url != '':
                save_from_github(url)
                updateList()
            else:
                mb.showerror("Ошибка", "Выберете какой мод скачать")
        def Delete():
            file = DownloadedList.get(DownloadedList.curselection())
            path = config['Path']['Path'] + "/"
            os.remove(path + file)
            updateList()
        butDownload = tk.Button(master=buttomFrame, text="Установить", width=32, command= Download)
        butDownload.pack()
        Version = ttk.Combobox(master=buttomFrame, width=12, values=VersionVariations)
        Version.pack(side=tk.LEFT)

        Version.current(VersionVariations.index(config['CurVersion']['curVersion']))
        def updateList():
            dir = config['Path']['Path']
            if Version.get():
                config['CurVersion'] = {'curVersion': Version.get()}
                with open('Config.ini', 'w') as configfile:
                    config.write(configfile)
            if Version.get() in VersionVariations:
                DownloadList.delete(0,tk.END)
                for i in ParseMods(Version.get()):
                    DownloadList.insert(0, i)
                if 'Path' in config:
                    DownloadedList.delete(0, tk.END)
                    for i in os.listdir(dir):
                        DownloadedList.insert(0, i)
                else:
                    mb.showerror("Ошибка", "Выберите папку загрузки")
            else:
                mb.showerror("Ошибка", "Выберите версию")

        updateList()
        butUpdate = tk.Button(master=buttomFrame, text="Обновить", width=15, command= updateList)
        butUpdate.pack(side=tk.LEFT)
        butDelete = tk.Button(master=buttom2Frame, text="Удалить", width=32, command= Delete)
        butDelete.pack()
        def ChooseFolder():
            directory = fd.askdirectory(title="Открыть папку модов", initialdir="C:/Users/Артём/Desktop/MMC-Download")
            if directory:
                config['Path'] = {'Path': directory}
                with open('Config.ini', 'w') as configfile:
                    config.write(configfile)
            else:
                mb.showerror("Ошибка", "Выберите папку")
        butChooseFolder = tk.Button(master=buttom2Frame, text="Выбрать папку", width=32, command= ChooseFolder)
        butChooseFolder.pack()

def save_from_github(link):
    filename = link.split('/')[-1]
    dir = config['Path']['Path']
    r = requests.get(link, allow_redirects=True)
    open(dir +"/"+ filename, "wb").write(r.content)

def ParseMods(mc_version):
    url = 'https://github.com/Zizazar/MinecraftModpackCreator/releases/tag/' + mc_version
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    modsRaw = soup.find_all('span', class_= "px-1 text-bold")
    mods = []
    for i in range(len(modsRaw) - 2):
        mods.append(modsRaw[i].text)
    return mods



if __name__ == "__main__":
    window = tk.Tk()
    application = App()
    application.mainloop()