class Persona:
    def __init__(
        self, host: str | None = None, persona_path: str | None = None, **kwargs
    ):
        self.host = host
        self.path = persona_path

    def generate(self, text: str):
        return text

    def speak(self, audio=None):
        return audio

    def embody(self, *args, **kwargs):
        return None
