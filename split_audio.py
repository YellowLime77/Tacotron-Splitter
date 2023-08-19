from pydub import AudioSegment

class AudioSplitter:
    def __init__(self, filename: str):
        self.originalAudio = AudioSegment.from_wav(filename)
    
    def segment_audio(self, start: float, end: float):
        start_in_ms = start*1000
        end_in_ms = end*1000
        segmented_audio = self.originalAudio[start_in_ms:end_in_ms]
        return segmented_audio
    
    def export_audio(self, audio: AudioSegment, export_filename: str):
        audio.export(export_filename, format="wav")
