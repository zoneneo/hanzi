# coding=utf-8
import pyttsx3
msg ='''今天我，寒夜里看雪飘过,怀着冷却了的心窝漂远方,风雨里追赶，雾里分不清影踪,天空海阔你与我,可会变,谁没在变
少次，迎着冷眼与嘲笑
从没有放弃过心中的理想
一刹那恍惚， 若有所失的感觉
不知不觉已变淡
心里爱（谁明白我）
原谅我这一生不羁放纵爱自由
也会怕有一天会跌倒
背弃了理想 ，谁人都可以
哪会怕有一天只你共我
'''
msg ='''
只言片语，
少言寡语，
一言两语，
千言万语，
自言自语。
'''
engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 100)

volume = engine.getProperty('volume')
engine.setProperty('volume', 1.0)


# 标准的粤语发音
voices = engine.setProperty('voice', "com.apple.speech.synthesis.voice.sin-ji")

# 普通话发音
# voices = engine.setProperty('voice', "com.apple.speech.synthesis.voice.ting-ting.premium")

# 台湾甜美女生普通话发音
voices = engine.setProperty('voice', "com.apple.speech.synthesis.voice.mei-jia")
print('准备开始语音播报...')
# 输入语音播报词语

# engine.say(msg)
# engine.runAndWait()

voices = engine.getProperty('voices')
# for voice in voices:
#     print(voice)
#     engine.setProperty('voice',voice.id)
#     engine.say('The quick brown fox jumped over the lazy dog.')
#     engine.runAndWait()

engine.setProperty('voice',voices[2].id)
engine.say('사랑해. 나한테시집올수있니?')
engine.runAndWait()
engine.say('I love you,,can you marry me?')
engine.runAndWait()
engine.stop()

