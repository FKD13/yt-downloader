from threading import *
import youtube_dl


class DownloadManager:
    """
    A manager for all video Downloads

    Only one of these should be used at once
    """
    def __init__(self):
        self._downloads = []
        self._download_logger = DownloadLogger()

    def create_download_task(self, url: str):
        """
        Create a DownloadTask for the specified url
        :param url:
            the url to download
        :return id:
            the id of the created task, this u can use later to start the download and request status
        """
        self._downloads.append(DownloadTask(url, self._download_logger))
        return len(self._downloads) - 1

    def start_download_task(self, id: int):
        """
        Start a specific task
        :param id:
            the id of the task that should be started
        :return:
            None
        """
        self._downloads[id].start()

    def status_download_task(self, id: int):
        """

        :param id:
            the id of the task to get the status from
        :return status:
            1 -> alive, 0 -> dead
        """
        return self._downloads[id].status()  # the possible error should not be handled here


class DownloadLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


class DownloadTask(Thread):
    def __init__(self, url: str, download_logger: DownloadLogger):
        super().__init__()
        self.url = url
        self._state = 0  # not started
        # TODO change hardcoded path to read from config
        self._download_options = {'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}], 'outtmpl': '/home/fklinck/Downloads/%(title)s.%(ext)s', 'logger': download_logger}

    def run(self):
        self._state = 1  # running
        try:
            with youtube_dl.YoutubeDL(self._download_options) as ydl:
                ydl.download([self.url])
            self._state = 2  # succeeded
        except Exception as e:
            print(e)
            self._state = 3  # crashed

    def status(self):
        return self._state
