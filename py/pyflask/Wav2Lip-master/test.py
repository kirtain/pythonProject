import pyttsx3

engine = pyttsx3.init()

engine.say("텍스트 음성 변환에 대한 나의 첫 번째 코드 ")
engine.say("감사합니다, Geeksforgeeks")
engine.save_to_file("감사합니다", 'speech.wav')
engine.runAndWait()