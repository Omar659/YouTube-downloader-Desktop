import youtube_dl
from pytube import Playlist
import threading
import os
import string

class Downloader():
    def __init__(self):
        self.finished = 0

    def download_video(self, link, i):
        video_url = link
        with youtube_dl.YoutubeDL() as ydl:
            video_info = ydl.extract_info(video_url, download=False)
            filename = ydl.prepare_filename(video_info)
            filename = "downloads/" + str(i) + " - " + ".".join(filename.split(".")[:-1]) + ".mp3"
        options={
            'format':'bestaudio/best',
            'keepvideo':False,
            'outtmpl':filename,
            'quiet': True
        }

        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])
        self.finished += 1

    def download_playlist(self, link):
        # playlist = Playlist('https://youtube.com/playlist?list=PLRSaCixmTE8qrRsGZWGcwuWuQ9hgRZF8T')
        playlist = Playlist(link)
        threads = []
        for i, url in enumerate(playlist.video_urls):
            download_thread = threading.Thread(target = self.download_video, args = [url, i])
            threads.append(download_thread)
        for thread in threads:
            thread.start()
        finish = False
        while not finish:
            finish = True
            c_finished = 0
            for i, thread in enumerate(threads):
                if thread.is_alive():
                    finish = False
                else:
                    c_finished += 1
            print("\rCompleted: " + str(c_finished) + "/" + str(len(threads)), end="")
        print("\rCompleted: " + str(c_finished) + "/" + str(len(threads)), end="")
        print("\n######\nFINISH\n######")
        exit(0)

if __name__=='__main__':
    downloader = Downloader()
    pl_vi = input("Playlist or video? (p/v)\n")
    if pl_vi.lower() == "v":
        link = input("Insert link: ")
        downloader.download_video(link)
    elif pl_vi.lower() == "p":
        link = input("Insert link: ")
        downloader.download_playlist(link)
    else:
        raise Exception('Insert "p" or "v"')