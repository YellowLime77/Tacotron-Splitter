import os
import shutil

class DatasetCreator:
    def __init__(self, wavFiles, transcriptTexts):
        self.wavFiles = wavFiles
        self.transcriptTexts = transcriptTexts
    

    def create_dataset(self, tempFolder):
        wavsPath = os.path.join(tempFolder, 'wavs')
        filelistsPath = os.path.join(tempFolder, 'filelists')

        if not os.path.isdir(wavsPath):
            os.makedirs(wavsPath)
        if not os.path.isdir(filelistsPath):
            os.makedirs(filelistsPath)

        self.__copy_wav_files(self.wavFiles, wavsPath)

        self.__create_list(self.transcriptTexts, self.wavFiles, filelistsPath)
    
    def __copy_wav_files(self, wavFiles, wavsPath):
        for wavFile in wavFiles:
            shutil.copyfile(wavFile, os.path.join(wavsPath, os.path.basename(wavFile)))

    def __create_list(self, transcriptionTexts, wavFileNames, filelistsPath):
        file_contents = ""
        for transcription_text, wav_filename in zip(transcriptionTexts, wavFileNames):
            file_contents += f'wavs/{os.path.basename(wav_filename)}|{transcription_text}\n'
        
        with open(os.path.join(filelistsPath, 'list.txt'), 'w') as f:
            f.write(file_contents)

    def zip(self, datasetFolder, zipFile):
        shutil.make_archive(zipFile, 'zip', datasetFolder)