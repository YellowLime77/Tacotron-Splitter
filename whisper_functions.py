import whisper

class WhisperFunctions:
    """
    It just loads the model and transcribes audio.
    I thought this class would be longer 🙃
    """

    def __init__(self, model_type: str):
        """Loads everything up, and then tries to become Gauss"""

        # Loads model (normally base)
        self.model = whisper.load_model(model_type)

    def transcribe(self, file) -> dict:
        """Uses the Whisper model to transcribe the audio"""

        # Self explanatory
        return self.model.transcribe(file)

        print('hello')