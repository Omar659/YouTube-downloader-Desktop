from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
import os
import re
from pytube import Playlist, YouTube

class Downloader(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.link_label = tk.Label(self, text="Inserisci il link del video o della playlist:")
        self.link_label.pack()

        self.link_entry = tk.Entry(self)
        self.link_entry.pack()

        self.select_folder_frame = tk.Frame(self)
        self.select_folder_frame.pack()

        self.select_folder_label = tk.Label(self.select_folder_frame, text="Cartella di destinazione:")
        self.select_folder_label.pack(side="left")

        self.select_folder_path = tk.StringVar()
        self.select_folder_path.set("./.././download")

        self.select_folder_entry = tk.Entry(self.select_folder_frame, textvariable=self.select_folder_path)
        self.select_folder_entry.pack(side="left")

        self.select_folder_button = tk.Button(self.select_folder_frame, text="Sfoglia", command=self.select_folder)
        self.select_folder_button.pack(side="left")

        self.download_button = tk.Button(self, text="Download", command=self.download)
        self.download_button.pack()

        self.progress_bar = tk.ttk.Progressbar(self, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack()

    def select_folder(self):
        folder_path = filedialog.askdirectory(initialdir="./.././download")
        if folder_path:
            self.select_folder_path.set(folder_path)

    def download(self):
        url = self.link_entry.get()
        folder_path = self.select_folder_path.get()

        if 'playlist' in url:
            self.download_playlist(url, folder_path)
        else:
            self.download_video(url, folder_path)

    def download_video(self, url, folder_path):
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        file_name = stream.default_filename.replace("mp4", "mp3")
        file_path = os.path.join(folder_path, file_name)
        stream.download(folder_path)
        os.rename(os.path.join(folder_path, stream.default_filename), file_path)
        self.progress_bar['value'] = 100.0
        self.progress_bar['text'] = '100% completato'

    def download_playlist(self, url, folder_path):
        playlist = Playlist(url)
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        for i, video in enumerate(playlist.video_urls):
            try:
                yt = YouTube(video)
                stream = yt.streams.filter(only_audio=True).first()
                file_name = stream.default_filename.replace("mp4", "mp3")
                file_path = os.path.join(folder_path, str(i) + " - " + file_name)
                stream.download(folder_path)
                os.rename(os.path.join(folder_path, stream.default_filename), file_path)
                self.progress_bar['value'] = float(i+1)/len(playlist.video_urls) * 100.0
                self.update()
            except:
                continue
        self.progress_bar['value'] = 0

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Downloader")
    app = Downloader(master=root)
    app.mainloop()
