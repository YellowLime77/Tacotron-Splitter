import whisper

class WhisperFunctions:
    def __init__(self, model_type: str):
        self.model = whisper.load_model(model_type)

    def transcribe(self, file):
        return self.model.transcribe(file)