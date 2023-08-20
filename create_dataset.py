import os
import shutil

class DatasetCreator:
    """Takes in generated audio files and its corresponding transcriptions, then processes them into a folder and zips it up for download"""

    def __init__(self, wavFiles, transcriptTexts):
        # Loads in the wav file paths and the transcript segment text
        self.wavFiles = wavFiles
        self.transcriptTexts = transcriptTexts

    def create_dataset(self, tempFolder):
        """Takes audio and transcriptions and organizes them into a specified folder"""

        # Creates folders to organize the dataset files into
        # Folder paths
        wavsPath = os.path.join(tempFolder, 'wavs')
        filelistsPath = os.path.join(tempFolder, 'filelists')

        # Creates the paths if they don't exist
        if not os.path.isdir(wavsPath):
            os.makedirs(wavsPath)
        if not os.path.isdir(filelistsPath):
            os.makedirs(filelistsPath)

        # Actually puts the files in the folders
        self.__copy_wav_files(self.wavFiles, wavsPath)
        self.__create_list(self.transcriptTexts, self.wavFiles, filelistsPath)
    
    def __copy_wav_files(self, wavFiles, wavsPath):
        """Private method to copy wav files over to the specified folder"""

        for wavFile in wavFiles:
            shutil.copyfile(wavFile, os.path.join(wavsPath, os.path.basename(wavFile)))

    def __create_list(self, transcriptionTexts, wavFileNames, filelistsPath):
        """Creates the list.txt with audio file paths and their transcriptions"""

        # For export
        file_contents = ""

        # Writes line-by-line the audio file path and the corresponding transcription text
        for transcription_text, wav_filename in zip(transcriptionTexts, wavFileNames):
            file_contents += f'wavs/{os.path.basename(wav_filename)}|{transcription_text}\n'
        
        # Export
        with open(os.path.join(filelistsPath, 'list.txt'), 'w') as f:
            f.write(file_contents)

    def zip(self, datasetFolder, zipFile):
        """Mr Zippy to do the (insert pun here)"""

        # Zips up the temp dataset file into a zip file
        shutil.make_archive(os.path.join('static', zipFile), 'zip', datasetFolder)

        # Removes the temp dataset folder
        shutil.rmtree(datasetFolder)