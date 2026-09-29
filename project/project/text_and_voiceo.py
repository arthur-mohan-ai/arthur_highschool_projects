# pip install SpeechRecognition pyaudio
import speech_recognition as sr
import time
import importlib

# pip install baidu-aip==4.16.10 chardet==5.1.0
# https://blog.csdn.net/yujinlong2002/article/details/126864522
from aip import AipSpeech
import speech_recognition as sr
import pyttsx3

# pip install translate==3.6.1
from translate import Translator

# 首先安装依赖，使用下面的命令
# pip install protobuf==3.20.0 transformers==4.27.1 icetk cpm_kernels

from transformers import AutoTokenizer, AutoModel


class RecognizerGoogle:
    def __init__(self):
        self.r = sr.Recognizer()

    def listen(self,rate=16000):
        """采集语音

        Args:
            rate (int, optional): 采样率. Defaults to 16000.

        Returns:
            AudioData: 采集到的语音数据
        """
        with sr.Microphone(sample_rate=rate) as source:
            speaker = SpeakerPyttsx3(voiceNo=0)
            speaker.say(text='请说话')
            print("请说话")
            # time.sleep(1)
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source=source)
        print("结束")
        return audio

    def recog(self,audio):
        """识别语音,这会调用google服务器,需要翻墙

        Args:
            audio (audio): 要识别的语音

        Returns:
            string: 识别结果字符串,识别失败返回0
        """
        try:
            print("开始识别")
            # text = self.r.recognize_google(audio, language='zh-CN')#被卡住
            text = self.r.recognize_google(audio, language='en')#被卡住
            print("You said: ", text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said.")
            return 0
        except sr.RequestError as e:
            print("Sorry, could not request results from Google Speech Recognition service; {0}".format(e))
            return 0


class RecognizerBaidu:
    def __init__(self,APP_ID = '32673559',API_KEY = 'EFNaLQ5yP5hhpFslVVCDNo46',SECRET_KEY = '6HTYnfzwwyHi1zKWCxZVsRoe3HhbxYOG'):
        self.client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        self.r = RecognizerGoogle()

    def listen(self,rate=16000):
        audio = self.r.listen(rate=16000)    

        with open('recording.wav', 'wb') as f:
            f.write(audio.get_wav_data())

    # 使用百度语音作为STT引擎
    def recog(self):
        with open('recording.wav', 'rb') as f:
            audio_data = f.read()

        result = self.client.asr(audio_data, 'wav', 16000)
        if result['err_no'] == 0:
            text = result['result'][0]
            print(text)
            return text
        else:
            print('Error:', result['err_msg'])
            return 0
        
class SpeakerPyttsx3:
    def __init__(self,rate=200,volume=1.0,voiceNo=0):        
        self.engine = pyttsx3.init()
        # 获取当前语音速率
        # rate = self.engine.getProperty('rate')
        # print(f'语音速率：{rate}')
        # 设置新的语音速率
        self.engine.setProperty('rate', rate)
        # 获取当前语音音量
        # volume = self.engine.getProperty('volume')
        # print(f'语音音量：{volume}')
        # 设置新的语音音量，音量最小为 0，最大为 1
        self.engine.setProperty('volume', volume)
        # 获取当前语音声音的详细信息
        voices = self.engine.getProperty('voices')
        print(f'语音声音详细信息：{voices}')

        # 1设置当前语音声音为女性，当前声音不能读中文,0设置当前语音声音为男性，当前声音可以读中文
        self.engine.setProperty('voice', voices[voiceNo].id)
        
        # 获取当前语音声音
        voice = self.engine.getProperty('voice')
        print(f'语音声音：{voice}')
        
    def __del__(self):
        self.engine.stop()

    def say(self,text):
        importlib.reload(pyttsx3)
        self.engine = pyttsx3.init()
        self.engine.say(text)
        self.engine.runAndWait()

class TranslateLanguage:
    def __init__(self,to_lang="chinese",from_lang="en"):
        # 以下是将简单句子从英语翻译成中文
        self.translator = Translator(to_lang=to_lang,from_lang=from_lang)

    def translate(self,text):
        translation = self.translator.translate(text)
        print(translation)
        return translation

class ChatGLMB6Tsinghua:
    def __init__(self,modelPath="THUDM/chatglm-6b",isUseGpu=True):
        self.tokenizer = AutoTokenizer.from_pretrained(modelPath, trust_remote_code=True)
        if isUseGpu:
            # self.model = AutoModel.from_pretrained(path, trust_remote_code=True).half().cuda()#用显卡
            self.model = AutoModel.from_pretrained(modelPath, trust_remote_code=True).half().quantize(4).cuda()#用显卡
        else:
            self.model = AutoModel.from_pretrained(modelPath, trust_remote_code=True).float()#用cpu

    def chat(self,text,history=None):
        if history:
            response, history = self.model.chat(self.tokenizer, text, history=history)
        else:
            response, history = self.model.chat(self.tokenizer, text, history=[])
        print(response)
        return response,history
    
if __name__ == "__main__":
    chater = ChatGLMB6Tsinghua()#使用默认，网络模型，GPUGPU
    chater = ChatGLMB6Tsinghua(modelPath="D:\\ChatGLM\\ChatGLM-webui\\model\\chatglm-6b",isUseGpu=False)#使用本地模型，CPU
    response, history = chater.chat(text="hello world",history=None)

    # tsl = TranslateLanguage(to_lang="chinese",from_lang="en")
    # tsl.translate(text="hello world")

    # speaker = SpeakerPyttsx3(voiceNo=0)
    # speaker.say(text="你好")

    # rb = RecognizerBaidu(APP_ID = '32673559',API_KEY = 'EFNaLQ5yP5hhpFslVVCDNo46',SECRET_KEY = '6HTYnfzwwyHi1zKWCxZVsRoe3HhbxYOG')
    # speaker = SpeakerPyttsx3(voiceNo=0)
    # while True:
    #     rb.listen(rate=16000)
    #     rst_text = rb.recog()
    #     if rst_text:
    #         speaker.say(text=rst_text)

    # rg = RecognizerGoogle()
    # while True:
    #     audio_dat = rg.listen(rate=16000)
    #     rst_text = rg.recog(audio=audio_dat)