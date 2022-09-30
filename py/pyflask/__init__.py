import os, sys
real_path = os.path.dirname(os.path.realpath(__file__))
sub_path = os.path.split(real_path)[0]
os.chdir(sub_path)

import time
import pyttsx3

from flask import Flask, escape, request,  Response, g, make_response
from flask.templating import render_template
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.debug = True

def root_path():
	'''root 경로 유지'''
	real_path = os.path.dirname(os.path.realpath(__file__))
	sub_path = "\\".join(real_path.split("\\")[:-1])
	return os.chdir(sub_path)

''' Main page '''
@app.route('/')
def index():
	return render_template('index.html')

''' Description '''
@app.route('/description')
def description():
	return render_template('description.html')

''' Demonstrate '''
@app.route('/demonstrate')
def demonstrate():
	return render_template('demonstrate.html')

@app.route('/demonstrate/sample')
def demonstrate_sample():
	return render_template('demonstrate_sample.html')

@app.route('/demonstrate/option')
def demonstrate_opt():
	return render_template('demonstrate_opt.html')

@app.route('/w2l_post', methods=['GET','POST'])
def w2l_post():
	
	if request.method == 'POST':
		root_path()

		# User_text
		user_text = request.form['user_text']


		engine = pyttsx3.init()

		voices = engine.getProperty('voices')
		engine.setProperty('rate', 150)
		engine.setProperty('voice', voices[2].id)
		engine.save_to_file(str(user_text), 'pyflask/static/audio/test.wav')
		engine.runAndWait()

		root_path()
		#Refer_audio
		refer_audio = "test.wav"

		refer_video = "test.mp4"
		refer_video_path = 'video/sample/' + str(refer_video)

		# wav2lip 처리
		os.system('cd C:/Users/doori/PycharmProjects/pythonProject/py/pyflask/Wav2Lip-master && python inference.py --checkpoint_path ./checkpoints/wav2lip_gan.pth --outfile "../static/result/sample/result_voice.mp4" --audio "../static/audio/{}" --face "../static/video/sample/{}"'.format(str(refer_audio), str(refer_video)))

		root_path()

		# Wav2lip
		transfer_mp4 = "result_voice.mp4"
		transfer_mp4_path = 'result/sample/'+str(transfer_mp4)

	return render_template('w2l_post.html',
					refer_video = refer_video_path, transfer_mp4 = transfer_mp4_path)


@app.route('/w2l_post_opt', methods=['GET', 'POST'])
def w2l_post_opt():
	if request.method == 'POST':
		root_path()

		f = request.files['file']
		f.save('pyflask/static/video/user/' + secure_filename(f.filename))

		# User_text
		user_text = request.form['user_text']

		engine = pyttsx3.init()

		voices = engine.getProperty('voices')
		engine.setProperty('rate', 150)
		engine.setProperty('voice', voices[2].id)
		engine.save_to_file(str(user_text), 'pyflask/static/audio/test.wav')
		engine.runAndWait()

		# Refer_audio
		refer_audio = "test.wav"
		refer_video = str(secure_filename(f.filename))
		refer_video_path = 'video/user/' + str(secure_filename(f.filename))

		# wav2lip 처리
		os.system('cd C:/Users/doori/PycharmProjects/pythonProject/py/pyflask/Wav2Lip-master && python inference.py --checkpoint_path ./checkpoints/wav2lip_gan.pth --outfile "../static/result/user/result_voice.mp4" --audio "../static/audio/{}" --face "../static/video/user/{}"'.format(str(refer_audio), str(refer_video)))

		root_path()

		# Wav2lip
		transfer_mp4 = "result_voice.mp4"
		transfer_mp4_path = 'result/user/' + str(transfer_mp4)

	return render_template('w2l_post_opt.html',
						   refer_video=refer_video_path, transfer_mp4=transfer_mp4_path)
