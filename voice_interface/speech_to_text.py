"""
Speech-to-text module using OpenAI Whisper.
Converts audio input to text for command parsing.
"""
import openai
import os
import tempfile

openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe_audio_file(file_path: str) -> str:
    """
    Transcribe an audio file to text using Whisper.

    Args:
        file_path: Path to audio file (.mp3, .wav, .m4a, .webm)

    Returns:
        Transcribed text string
    """
    with open(file_path, "rb") as audio_file:
        response = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
    return response.strip()


def transcribe_audio_bytes(audio_bytes: bytes, file_extension: str = "webm") -> str:
    """
    Transcribe raw audio bytes.
    Used by the FastAPI endpoint for browser microphone input.

    Args:
        audio_bytes:    Raw audio data
        file_extension: Format of the audio (webm, wav, mp3, m4a)

    Returns:
        Transcribed text string
    """
    with tempfile.NamedTemporaryFile(suffix=f".{file_extension}", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        text = transcribe_audio_file(tmp_path)
    finally:
        os.unlink(tmp_path)

    return text
