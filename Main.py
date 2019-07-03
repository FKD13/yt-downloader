from flask import Flask, url_for, request, render_template, redirect, flash, jsonify
import downloader
from forms import *


app = Flask(__name__)
app.config['SECRET_KEY'] = '15a852521ab8c59fd045beee'


download_manager = downloader.DownloadManager()


@app.route('/')
def home():
    return render_template('home.html', form=DownloadForm())


@app.route('/download/', methods=['POST'])
def download():
    form = DownloadForm(request.form)
    if form.validate():
        id = download_manager.create_download_task(request.form['url'])
        download_manager.start_download_task(id)
        return render_template()
    return jsonify({'message': 'Malformed url'}), 400


@app.route('/status/<int:download_id>')
def status(download_id):
    try:
        return jsonify({'status': download_manager.status_download_task(download_id)}), 200
    except IndexError:
        return jsonify({'message': 'bad id'}), 400
