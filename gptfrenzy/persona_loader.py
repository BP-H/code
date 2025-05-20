"""Fallback persona implementation defining the Persona protocol.

The :class:`Persona` class represents the minimal interface expected by the
spawn system. Real persona modules may override some or all methods, but the
protocol consists of three optional hooks in addition to initialization:

``generate(text)``
    Coroutine returning the persona's textual response to ``text``.

``speak(audio=None)``
    Coroutine that handles text-to-speech or audio processing if supported.

``embody(*args, **kwargs)``
    Coroutine consuming realtime embodiment data for animation or other effects.
"""


class Persona:
    """Base stub used when a persona does not supply its own class."""

    def __init__(
        self, host: str | None = None, persona_path: str | None = None, **kwargs
    ) -> None:
        """Store ``host`` identifier and ``persona_path`` for later use."""

        self.host = host
        self.path = persona_path

    async def generate(self, text: str):
        """Return the persona's response to ``text``."""

        return text

    async def speak(self, audio=None):
        """Optionally process or synthesize ``audio``."""

        return audio

    async def embody(self, *args, **kwargs):
        """Accept realtime embodiment data."""

        return None
