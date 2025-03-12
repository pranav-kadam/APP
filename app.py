from flask import Flask, request, send_file, render_template
import subprocess
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
MERGED_FOLDER = "merged"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MERGED_FOLDER, exist_ok=True)

def get_video_duration(video_path):
    """Returns the duration of the video in seconds."""
    result = subprocess.run(
        ["ffprobe", "-i", video_path, "-show_entries", "format=duration", "-v", "quiet", 
         "-of", "csv=p=0"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    return float(result.stdout.strip()) if result.stdout else 0

@app.route("/", methods=["GET", "POST"])
def upload_files():
    if request.method == "POST":
        if "video" not in request.files or "audio" not in request.files:
            return "Please upload both video and audio files", 400
        
        video = request.files["video"]
        audio = request.files["audio"]

        video_path = os.path.join(UPLOAD_FOLDER, secure_filename(video.filename))
        audio_path = os.path.join(UPLOAD_FOLDER, secure_filename(audio.filename))
        output_path = os.path.join(MERGED_FOLDER, "merged.mp4")

        video.save(video_path)
        audio.save(audio_path)

        video_duration = get_video_duration(video_path)

        command = [
            "ffmpeg", "-i", video_path, "-stream_loop", "-1", "-i", audio_path,  # Loop audio if shorter
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-t", str(video_duration),  # Ensure the output length matches the video
            "-shortest", output_path, "-y"
        ]
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
