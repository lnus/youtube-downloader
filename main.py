from flask import Flask, render_template, request
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
        yt_resolutions.desc().first().download()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST" and "iurl" in request.form:
        url = request.form["iurl"]
        d.download_video(url)

    return render_template("index.html")

if __name__ == "__main__":
    d = Downloader()
    app.run()
