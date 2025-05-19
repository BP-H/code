"""Fallback persona implementation defining the Persona protocol.

The :class:`Persona` class represents the minimal interface expected by the
spawn system. Real persona modules may override some or all methods, but the
protocol consists of three optional hooks in addition to initialization:

``generate(text)``
    Return the persona's textual response to ``text``.

``speak(audio=None)``
    Handle text-to-speech or audio processing if the persona supports voice.

``embody(*args, **kwargs)``
    Consume realtime embodiment data for animation or other effects.
"""


class Persona:
    """Base stub used when a persona does not supply its own class."""

    def __init__(
        self, host: str | None = None, persona_path: str | None = None, **kwargs
    ) -> None:
        """Store ``host`` identifier and ``persona_path`` for later use."""

        self.host = host
        self.path = persona_path

    def generate(self, text: str):
        """Return the persona's response to ``text``."""

        return text

    def speak(self, audio=None):
        """Optionally process or synthesize ``audio``."""

        return audio

    def embody(self, *args, **kwargs):
        """Accept realtime embodiment data."""

        return None
