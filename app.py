"""
A simple web app using Flask that splits audio and transcribes it using OpenAI's Whisper

( ͡°( ͡° ͜ʖ( ͡° ͜ʖ ͡°)ʖ ͡°) ͡°)

🟢🍋
"""

# Imports
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from werkzeug.utils import secure_filename

import os

import json
import shutil

from whisper_functions import WhisperFunctions
from split_audio import AudioSplitter
from custom_timer import Timer
from create_dataset import DatasetCreator

# Setup objects
app = Flask(__name__)
whisper_functions = WhisperFunctions("base")
timer = Timer()

@app.route("/")
def index():
    """The main page that lets you upload the audio file"""

    return render_template('hello.html')

@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    """URL for the main page to upload the file to"""

    if request.method == 'POST':
        # Saves uploaded file to the disk
        f = request.files['audioFile']
        filename = os.path.join('static', secure_filename(f.filename))
        f.save(filename)

        # For tracking how long the transcription takes
        timer.start()

        # Saves the wav filename to the session
        session['wavFile'] = filename

        # Saves the transcription to a text file
        with open(os.path.join('static', 'transcription.txt'), 'w') as file:
            json.dump(whisper_functions.transcribe(filename), file)

        return redirect(url_for('result'))
    
@app.route('/result')
def result():
    """
    Preview of the generated dataset
    
    Shows time elapsed for Whisper to transcribe the audio,
    provides a download button to download the dataset,
    and contains a table to preview the audio and the corresponding transcription
    """

    # Gets the wav filename from the session
    wavFile = session['wavFile']

    # Gets transcript from file
    with open(os.path.join('static', 'transcription.txt'), 'r') as file:
        full_transcription = json.load(file)

    split_audio_from_transcription(wavFile, full_transcription)

    # Sets up lists of wav filenames and transcription segment texts to send to both the webpage and to the dataset creator
    segment_folder_name = 'segments'
    static_segment_folder_name = os.path.join("static", segment_folder_name)
    wavFiles = [url_for('static', filename=segment_folder_name + "/" + f) for f in os.listdir(static_segment_folder_name) if os.path.isfile(os.path.join(static_segment_folder_name, f))]
    transcriptTexts = [segment['text'] for segment in full_transcription['segments']]


    # Dataset creator
    # Just another variable for the dataset creator
    wavFilePaths = [os.path.join(static_segment_folder_name, f) for f in os.listdir(static_segment_folder_name) if os.path.isfile(os.path.join(static_segment_folder_name, f))]
    wavFilePaths = sorted(wavFilePaths, key=lambda x: int(''.join([character for character in list(x) if character.isdigit()])))

    # Changeable variables for the dataset creator
    temp_dataset_folder = 'temp_dataset'
    zip_filename = 'dataset'

    # Calls the dataset creator methods
    dataset_creator = DatasetCreator(wavFilePaths, transcriptTexts)
    dataset_creator.create_dataset(temp_dataset_folder)
    dataset_creator.zip(temp_dataset_folder, zip_filename)

    return render_template('results.html', elapsed_time=timer.stop(), wavFiles_transcriptTexts=zip(wavFiles, transcriptTexts))

@app.route('/downloaddataset', methods=['GET', 'POST'])
def downloaddataset():
    """Basic URL that sends the dataset zip file to download"""

    return send_from_directory('static', 'dataset.zip')

def split_audio_from_transcription(filename, transcription):
    """Internal function to call split_audio.py's segmenter and to export it to a segment folder"""

    # Initializes the audio splitter
    audio_splitter = AudioSplitter(filename)

    # Goes through each transcription segment (from whisper's output) and calls AudioSplitter methods to save it to a specialized folder
    for index, segment in enumerate(transcription['segments']):
        segment_segment = audio_splitter.segment_audio(segment["start"], segment["end"])
        audio_splitter.export_audio(segment_segment, f'static/segments/chunk{index}.wav')

if __name__ == '__main__':
    # 🤫
    app.secret_key = 'a not so secret key'

    # Remove temp static files
    try:
        shutil.rmtree('static')
    except:
        print('prob first time running')
    os.makedirs('static/segments')

    if 1 + 1 == 3:
        print('BREAKTHROUGH!!!!')
    else:
        print('damn')

    # Starts the Flask app
    app.run(debug=True)