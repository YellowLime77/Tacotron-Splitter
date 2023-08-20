from pydub import AudioSegment

class AudioSplitter:
    """Takes in time stamps and splits the long audio based on that"""
    
    def __init__(self, filename: str):
        """Loads the audio"""

        self.originalAudio = AudioSegment.from_wav(filename)
    
    def segment_audio(self, start: float, end: float) -> AudioSegment:
        """The splitter based on time stamps"""

        # turns secs to ms
        start_in_ms = start*1000
        end_in_ms = end*1000

        # Cool pythonic way to just segment the audio
        segmented_audio = self.originalAudio[start_in_ms:end_in_ms]
        
        return segmented_audio
    
    def export_audio(self, audio: AudioSegment, export_filename: str):
        """Turns the audio segment into a file"""

        audio.export(export_filename, format="wav")
