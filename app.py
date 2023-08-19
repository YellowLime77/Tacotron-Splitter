from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from whisper_functions import WhisperFunctions
from split_audio import AudioSplitter

app = Flask(__name__)
whisper_functions = WhisperFunctions("base")

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
        session['transcription'] = whisper_functions.transcribe(filename)
        return redirect(url_for('result'))
    
@app.route('/result')
def result():
    full_transcription = session['transcription']
    wavFile = session['wavFile']
    split_audio_from_transcription(wavFile, full_transcription)
    webpage = ''
    for segment in full_transcription['segments']:
        webpage += f'<p>start: {segment["start"]}, end: {segment["end"]}, text: {segment["text"]}</p>'
    return webpage

def split_audio_from_transcription(filename, transcription):
    audio_splitter = AudioSplitter(filename)
    for index, segment in enumerate(transcription['segments']):
        segment_segment = audio_splitter.segment_audio(segment["start"], segment["end"])
        audio_splitter.export_audio(segment_segment, f'segments/chunk{index}.wav')


if __name__ == '__main__':
    app.secret_key = 'WHAT A KEY!!!!'
    app.run(debug=True)