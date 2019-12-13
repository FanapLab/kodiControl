from kodipydent import Kodi 
from time import sleep
import requests

class Control():
    def __init__(self):
        self.host = '10.21.26.152'
        self.username = 'kodi'
        self.password = None
        self.kodi = self.initiator()
        self.playSpeed = None

        self.dispatch = {
            "play":self.play,
            "stop":self.pause,
            "and":self.stop,
            "bank":self.ShowStock,
        }
    
    def initiator(self):
        return Kodi(self.host, username= self.username, password=self.password)

    def dispatcher(self,func):
        print("Im dispatcher to %s"%(func))
        self.dispatch[func]()
    
    def play(self):
        if self.kodi.Player.GetActivePlayers()["result"]:
            if self.playSpeed == 0:
                playerid = self.kodi.Player.GetActivePlayers()["result"][0]["playerid"]
                self.kodi.Player.PlayPause(playerid)
                self.playSpeed = 1
        else:
            self.kodi.Player.Open(item={"playlistid":1})
            self.playSpeed = 1

        print("play")
    
    def pause(self):
        if self.kodi.Player.GetActivePlayers()["result"]:
            if self.playSpeed == 1:
                playerid = self.kodi.Player.GetActivePlayers()["result"][0]["playerid"]
                self.kodi.Player.PlayPause(playerid)
                self.playSpeed = 0

        print("pause")

    def stop(self):
        if self.kodi.Player.GetActivePlayers()["result"]:
            playerid = self.kodi.Player.GetActivePlayers()["result"][0]["playerid"]
            self.kodi.Player.Stop(playerid)
        print("stop")
    
    def ShowStock(self):
        url= "http://www.tsetmc.com/tsev2/data/instinfodata.aspx?i=9536587154100457&c=57+"
        page = requests.get(url)
        stock = page.text.split(",")[2]
        self.kodi.GUI.ShowNotification(title="بانک پاسارگاد",message="قیمت آخرین معامله:%s"%(stock))
        print("stocks")
