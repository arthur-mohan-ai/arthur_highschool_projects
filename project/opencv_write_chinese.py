# pip install pillow

import cv2
from PIL import Image,ImageDraw,ImageFont
import numpy as np

def cv2AddChineseText(img,text,position,textColor=(0,255,0),textSize=30):
    if isinstance(img,np.ndarray):#判断是否openCV图片类型
        img = Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype("simsun.ttc",textSize,encoding="utf-8")
    # 绘制文本
    draw.text(position,text,textColor,font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)

def zh_ch(string):
    return string.encode("gbk").decode(errors="ignore")
    
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while True:
        ret,frame = cap.read()
        # 展示图片
        # cv2.putText(frame,"创新工作坊",(123,123),font,2,(0,255,0),3)
        frame = cv2AddChineseText(frame,"创新工作坊",(123,123),(0,255,0),30)
        
        cv2.imshow("capture",frame)
        if cv2.waitKey(1) & 0xFF==ord("q"):
            break
        
    # 释放对象，销毁窗口
    cap.release()
    cv2.destroyAllWindows()


