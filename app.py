from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename

import os

from whisper_functions import WhisperFunctions
from split_audio import AudioSplitter
from custom_timer import Timer

app = Flask(__name__)
whisper_functions = WhisperFunctions("base")
timer = Timer()

@app.route("/")
def index():
    return render_template('hello.html')

@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['audioFile']
        filename = f.filename
        f.save(secure_filename(filename))
        session['wavFile'] = filename
        timer.start()
        session['transcription'] = whisper_functions.transcribe(filename)
        return redirect(url_for('result'))
    
@app.route('/result')
def result():
    full_transcription = session['transcription']
    wavFile = session['wavFile']
    split_audio_from_transcription(wavFile, full_transcription)

    segment_folder_name = 'segments'
    static_segment_folder_name = os.path.join("static", segment_folder_name)
    wavFiles = [url_for('static', filename=segment_folder_name + "/" + f) for f in os.listdir(static_segment_folder_name) if os.path.isfile(os.path.join(static_segment_folder_name, f))]
    transcriptTexts = [segment['text'] for segment in full_transcription['segments']]

    return render_template('results.html', elapsed_time=timer.stop(), wavFiles_transcriptTexts=zip(wavFiles, transcriptTexts))

def split_audio_from_transcription(filename, transcription):
    audio_splitter = AudioSplitter(filename)
    for index, segment in enumerate(transcription['segments']):
        segment_segment = audio_splitter.segment_audio(segment["start"], segment["end"])
        audio_splitter.export_audio(segment_segment, f'static/segments/chunk{index}.wav')


if __name__ == '__main__':
    app.secret_key = 'WHAT A KEY!!!!'
    app.run(debug=True)