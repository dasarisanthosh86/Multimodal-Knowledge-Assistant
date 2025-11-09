import os
import tempfile
import whisper
from moviepy.editor import VideoFileClip

# ✅ Load Whisper model only once (to save load time)
try:
    print("🔊 Loading Whisper model...")
    model = whisper.load_model("base")
    print("✅ Whisper model loaded successfully.")
except Exception as e:
    print(f"❌ Failed to load Whisper model: {e}")
    model = None


def extract_from_audio(file_path: str) -> str:
    """
    Transcribe audio file (.mp3, .wav) using Whisper.
    Returns extracted text.
    """
    if model is None:
        print("❌ Whisper model not available.")
        return None

    try:
        print(f"🎧 Transcribing audio: {file_path}")
        result = model.transcribe(file_path)
        text = result.get("text", "").strip()
        if not text:
            print("⚠️ No speech detected in audio.")
            return None
        print("✅ Audio transcription successful.")
        return text
    except Exception as e:
        print(f"❌ Error during audio transcription: {e}")
        return None


def extract_from_video(file_path: str) -> str:
    """
    Extracts audio from a video file and transcribes it.
    Supported formats: .mp4, .mov, .avi
    """
    if model is None:
        print("❌ Whisper model not available.")
        return None

    try:
        print(f"🎥 Extracting audio from video: {file_path}")

        # Create a temporary audio file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_audio:
            audio_path = tmp_audio.name

        # Extract audio
        clip = VideoFileClip(file_path)
        clip.audio.write_audiofile(audio_path, verbose=False, logger=None)
        clip.close()

        # Transcribe extracted audio
        text = extract_from_audio(audio_path)

        # Clean up
        os.remove(audio_path)

        if text:
            print("✅ Video transcription successful.")
        else:
            print("⚠️ No transcribable audio found in video.")
        return text

    except Exception as e:
        print(f"❌ Error during video transcription: {e}")
        return None
