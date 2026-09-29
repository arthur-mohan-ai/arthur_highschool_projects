import json
import time
import mcpi.block as block
from toneMC2 import tttone

class Music:
    def __init__(self,pps=60,tone="toneMC1.json",music="music.json"):
        self.MCType = tone
        if tone == "toneMC2.json" or tone == "toneMC2.py":
            self.tone = tttone
        else:
            # 音调字典
            with open(tone,"r",encoding="utf-8") as f:
                self.tone = json.load(f)
            # print(self.tone,type(self.tone))#字典

        # 简谱：音调与时间关系
        with open(music,"r",encoding="utf-8") as f:
            self.music = json.load(f)
        # print(self.music,type(self.music))#列表

        # 计算每拍多长时间，一般按照分钟60拍计算
        self.pad = 60.0/pps

    def play(self,isRaspberry=False,buzzer=None,mc=None):        
        for yf in self.music:
            print(self.tone[yf[0]])
            if isRaspberry:
                buzzer.ChangeFrequency(self.tone[yf[0]])
            else:
                if self.MCType == "toneMC1.json":
                    pos = self.tone[yf[0]].split(",")
                    mc.setBlock(int(pos[0]),int(pos[1]),int(pos[2]),76)
                elif self.MCType == "toneMC2.json":
                    pos = mc.player.getTilePos()
                    mc.setBlock(pos.x+1, pos.y, pos.z,block.GRASS.id)
                    mc.setBlockWithNBT(pos.x+1, pos.y+1, pos.z, block.NOTEBLOCK.id,0,self.tone[yf[0]])
                    mc.setBlock(pos.x+2, pos.y, pos.z,block.GRASS.id)
                    mc.setBlock(pos.x+2, pos.y+1, pos.z, 76)
            time.sleep(yf[1]*self.pad)
            if not isRaspberry:
                if self.MCType == "toneMC1.json":
                    mc.setBlock(int(pos[0]),int(pos[1]),int(pos[2]),0)
                elif self.MCType == "toneMC2.json":
                    mc.setBlock(pos.x+1, pos.y+1, pos.z, 0)
                    mc.setBlock(pos.x+1, pos.y, pos.z, 0)
                    mc.setBlock(pos.x+2, pos.y+1, pos.z, 0)
                    mc.setBlock(pos.x+2, pos.y, pos.z,0)
        if buzzer:
            buzzer.stop()

    def play1(self,mc=None,pos=None):          
        for yf in self.music:
            print(self.tone[yf[0]])
            if self.MCType == "toneMC1.json":
                pos = self.tone[yf[0]].split(",")
                mc.setBlock(int(pos[0]),int(pos[1]),int(pos[2]),76)
            elif self.MCType == "toneMC2.json":
                pos_ = mc.player.getTilePos()
                x,y,z = pos
                mc.player.setTilePos(x,y,z)
                mc.setBlock(x+1, y, z,block.GRASS.id)
                mc.setBlockWithNBT(x+1, y+1, z, block.NOTEBLOCK.id,0,self.tone[yf[0]])
                mc.setBlock(x+2, y, z,block.GRASS.id)
                mc.setBlock(x+2, y+1, z, 76)

            time.sleep(yf[1]*self.pad)
            
            if self.MCType == "toneMC1.json":
                mc.setBlock(int(pos[0]),int(pos[1]),int(pos[2]),0)
            elif self.MCType == "toneMC2.json":
                mc.setBlock(x+1, y+1, z, 0)
                mc.setBlock(x+1, y, z, 0)
                mc.setBlock(x+2, y+1, z, 0)
                mc.setBlock(x+2, y, z,0)


        mc.player.setTilePos(pos_.x,pos_.y,pos_.z)


if __name__ == "__main__":
    from mcpi.minecraft import Minecraft
    try:
        import RPi.GPIO as GPIO
    except:
        pass


    mc = Minecraft.create()
    pos = mc.player.getTilePos()
    print(pos.x,pos.y,pos.z)
    buzzer = None
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        buzzer = GPIO.PWM(12,50)
        buzzer.start(0)
    except:
        pass

    music = Music(pps=30,tone="toneMC2.json",music="music.json")
    for i in range(10):
      music.play(isRaspberry=False,buzzer=buzzer,mc=mc)