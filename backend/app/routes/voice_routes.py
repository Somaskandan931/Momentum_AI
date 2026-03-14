"""
Voice Routes — accepts browser microphone audio, transcribes via Whisper,
and parses the transcript into a structured action for the frontend.
"""

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from backend.app.auth.jwt_handler import get_current_user
from voice_interface.speech_to_text import transcribe_audio_bytes
from voice_interface.command_parser import parse_command

router = APIRouter()


@router.post("/command")
async def voice_command(
    audio: UploadFile = File(...),
    project_id: str = Form(...),
    current_user: dict = Depends(get_current_user),
):
    """
    Accept a browser audio blob (typically .webm), transcribe it with Whisper,
    parse the text into a structured action, and return both to the frontend.
    Called by VoiceCommand.jsx as POST /api/voice/command.
    """
    audio_bytes = await audio.read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Empty audio file received")

    # Determine file extension — browser usually sends .webm
    extension = "webm"
    if audio.filename and "." in audio.filename:
        extension = audio.filename.rsplit(".", 1)[-1].lower()

    try:
        transcript = transcribe_audio_bytes(audio_bytes, file_extension=extension)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {e}")

    action = parse_command(transcript)

    return {
        "transcript": transcript,
        "action": action,
        "project_id": project_id,
    }