from flask import Flask, render_template, request, send_from_directory
from pytube import YouTube
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')  # Assuming you have an index.html in a "templates" folder.

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    choice = request.form.get('choice')
    resolution = request.form.get('resolution')

    yt = YouTube(url)
    
    if choice == "video":
        stream = yt.streams.filter(progressive=True, file_extension="mp4", resolution=resolution).first()
    elif choice == "audio":
        stream = yt.streams.filter(only_audio=True).first()
    elif choice == "thumbnail":
        # For thumbnail, you'll need to download separately and send.
        return "Thumbnail download not yet implemented"

    download_path = stream.download(DOWNLOAD_FOLDER)
    filename = os.path.basename(download_path)

    # Return file for download
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
