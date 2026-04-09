import subprocess
from moviepy.editor import VideoFileClip
from pathlib import Path
import sys

url = sys.argv[1]

OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)

video = "vod.mp4"

# download
subprocess.run(["yt-dlp", "-o", video, url])

# get duration
clip = VideoFileClip(video)
duration = int(clip.duration)

# dynamic clips
if duration < 600:
    n, length = 2, 20
elif duration < 3600:
    n, length = 4, 30
else:
    n, length = 6, 40

interval = duration // n

for i in range(n):
    start = i * interval
    end = start + length
    
    sub = clip.subclip(start, end)
    out = OUTPUT / f"clip_{i}.mp4"
    sub.write_videofile(str(out), codec="libx264", audio_codec="aac")
