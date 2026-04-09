import subprocess, os
import numpy as np
import librosa
import whisper
from pathlib import Path
from moviepy.editor import VideoFileClip

WHISPER_MODEL = "tiny"

def download_vod(url, output):
    subprocess.run(["yt-dlp", "-o", output, url])
    return output

def extract_audio(video, audio):
    subprocess.run([
        "ffmpeg","-y","-i",video,"-vn",
        "-acodec","pcm_s16le","-ar","16000","-ac","1",audio
    ])
    return audio

def analyse_audio(audio_path):
    y, sr = librosa.load(audio_path)
    rms = librosa.feature.rms(y=y)[0]

    threshold = rms.mean() + 1.5 * rms.std()
    spikes = np.where(rms > threshold)[0]

    return spikes, rms

def transcribe(audio_path):
    model = whisper.load_model(WHISPER_MODEL)
    result = model.transcribe(audio_path)
    return result["segments"]

def generate_clips(video_path, spikes, output_dir, duration=45, max_clips=5):
    clip = VideoFileClip(video_path)
    fps = clip.fps

    highlights = []
    used = set()

    for s in spikes:
        t = s * 0.5  # approx seconds

        if any(abs(t - u) < 30 for u in used):
            continue

        start = max(0, t - duration // 2)
        end = start + duration

        output = output_dir / f"clip_{len(highlights)}.mp4"

        sub = clip.subclip(start, end)
        sub.write_videofile(str(output), codec="libx264", audio_codec="aac", logger=None)

        highlights.append(str(output))
        used.add(t)

        if len(highlights) >= max_clips:
            break

    return highlights

def run_pipeline(url, job_id):
    base = Path("clips") / job_id
    base.mkdir(parents=True, exist_ok=True)

    video = str(base / "vod.mp4")
    audio = str(base / "audio.wav")

    download_vod(url, video)
    extract_audio(video, audio)

    spikes, _ = analyse_audio(audio)
    segments = transcribe(audio)

    clips = generate_clips(video, spikes, base)

    return clips
