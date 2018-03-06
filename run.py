from flask import Flask, render_template, request, send_file
from pytube import YouTube
import atexit
import os
import glob

# For scheduling the deletion of mp4 files from the server.
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

# Function to delete all mp4's from server
def delete_mp4():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for mp4 in glob.iglob(os.path.join(dir_path, "*.mp4")):
        os.remove(mp4)

# Schedule deletion of files from server
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
        func=delete_mp4,
        trigger=IntervalTrigger(minutes=10),
        id="deletion_job",
        name="Deletes all mp4's from the server every 10 minutes.",
        replace_existing=True
        )

# Shut down scheduler when exiting the server
atexit.register(lambda: scheduler.shutdown())

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

"""
if __name__ == "__main__":
    # Clears the .mp4 files at startup
    delete_mp4()

    # Sets up the downloader
    d = Downloader()

    # Runs the server
    app.run()
"""
