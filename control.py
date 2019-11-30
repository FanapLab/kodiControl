from kodipydent import Kodi 
from time import sleep
import requests

class Control():
    def __init__(self):
        self.host = '127.0.0.1'
        self.username = 'kodi'
        self.password = None
        self.kodi = self.initiator()
        self.playSpeed = None
    
    def initiator(self):
        return Kodi(self.host, username= self.username, password=self.password)
    
    def play(self):
        if self.kodi.Player.GetActivePlayers()["result"]:
            if self.playSpeed == 0:
                playerid = self.kodi.Player.GetActivePlayers()["result"][0]["playerid"]
                self.kodi.Player.PlayPause(playerid)
                self.playSpeed = 1
        else:
            self.kodi.Player.Open(item={"playlistid":1})
            self.playSpeed = 1
    
    def pause(self):
        if self.kodi.Player.GetActivePlayers()["result"]:
            if self.playSpeed == 1:
                playerid = self.kodi.Player.GetActivePlayers()["result"][0]["playerid"]
                self.kodi.Player.PlayPause(playerid)
                self.playSpeed = 0
    def stop(self):
        if self.kodi.Player.GetActivePlayers()["result"]:
            playerid = self.kodi.Player.GetActivePlayers()["result"][0]["playerid"]
            self.kodi.Player.Stop(playerid)
    
    def ShowStock(self):
        url= "http://www.tsetmc.com/tsev2/data/instinfodata.aspx?i=9536587154100457&c=57+"
        page = requests.get(url)
        stock = page.text.split(",")[2]
        self.kodi.GUI.ShowNotification(title="بانک پاسارگاد",message="قیمت آخرین معامله:%s"%(stock))
        



if __name__ == "__main__":    
    control = Control()
    control.play()
    sleep(5)
    control.play()
    sleep(5)
    control.play()
    control.pause()
    sleep(5)
    control.play()
    sleep(5)
    control.stop()
    sleep(5)

