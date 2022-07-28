import requests
from bs4 import BeautifulSoup
import sys

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



