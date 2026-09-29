# 自定义库: camera.py
# 作用：调用摄像头生成视频流

import cv2

class VideoCamera(object):
    def __init__(self):
        # VideoCapture可以读取从url、本地视频文件以及本地摄像头的数据
        # self.cap = cv2.VideoCapture('rtsp://admin:admin@172.21.182.12:554/cam/realmonitor?channel=1&subtype=1')
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        if not success:
            return
        else:
            # 将每一帧的数据进行编码压缩，存放在memory中
            ret,jpeg = cv2.imencode(".jpg",image)
            if not ret:
                return
            else:
                return jpeg.tobytes()

def gen_frame(camera):
    while True:
        frame = camera.get_frame()
        if frame:
            # 通过将一帧帧的图像返回，就达到了看视频的目的。
            # multipart/x-mixed-replace是单次的http请求-响应模式，
            # 如果网络中断，会导致视频流异常终止，必须重新连接才能恢复
            # 响应行--frame;响应头--键值对；空行；响应体；空行
            yield (b'--frame\r\n'+
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
