from flask import Flask, render_template, request, send_file
from pytube import YouTube

app = Flask(__name__)

class Downloader(object):
    """Downloads the files and serves them to the user"""
    def __init__(self):
        print("Downloader loaded successfully!")

    def download_video(self, url):
        """Downloads the video entered in the field."""
        yt = YouTube(url)
        yt_filtered = yt.streams.filter(progressive=True, file_extension="mp4")
        yt_resolutions = yt_filtered.order_by("resolution")

        # Downloads the first video that fits the description
        video = yt_resolutions.desc().first()
        video.download()

        # Returns the filename
        return video.default_filename


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["GET", "POST"])
def download():
    if request.method == "POST" and "iurl" in request.form:
        url = request.form["iurl"]

        # Downloads video and gets filename
        filename = d.download_video(url)

        # Serves user the file
        return send_file(filename, as_attachment=True)

    else:
        return render_template("error.html")

if __name__ == "__main__":
    d = Downloader()
    app.run(debug = True)
