import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pytube import YouTube, Playlist
from threading import Thread
import os

class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        
        self.root.geometry("400x380")
        self.root.resizable(1, 1)
        
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#fff")
        self.style.configure("TButton", background="#4CAF50", foreground="#404040", font=("Helvetica", 10, "bold"))
        
        self.style.configure("TLabel", background="#fff", foreground="#333", font=("Helvetica", 10))
        
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill="both", expand=True)
        
        self.link_label = ttk.Label(self.main_frame, text="Link del video o della playlist:")
        self.link_label.pack(anchor="w", pady=(0, 10))
        
        self.link_entry = ttk.Entry(self.main_frame, width=50)
        self.link_entry.pack(pady=(0, 10))
        
        self.path_label = ttk.Label(self.main_frame, text="Cartella di download:")
        self.path_label.pack(anchor="w", pady=(0, 10))
        
        self.path_entry = ttk.Entry(self.main_frame, width=50)
        self.path_entry.pack(pady=(0, 10))
        
        self.browse_button = ttk.Button(self.main_frame, text="Sfoglia", command=self.browse_path)
        self.browse_button.pack(pady=(0, 10))
        
        self.download_type = tk.StringVar()
        self.download_type.set("video")
        
        self.video_radio = ttk.Radiobutton(self.main_frame, text="Scarica video", variable=self.download_type, value="video")
        self.video_radio.pack(anchor="w", pady=(0, 10))
        
        self.audio_radio = ttk.Radiobutton(self.main_frame, text="Scarica solo audio (MP3)", variable=self.download_type, value="audio")
        self.audio_radio.pack(anchor="w", pady=(0, 10))
        
        self.progress_label = ttk.Label(self.main_frame, text="Progresso:")
        self.progress_label.pack(anchor="w", pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(self.main_frame, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=(0, 10))
        
        self.download_button = ttk.Button(self.main_frame, text="Scarica", command=self.start_download)
        self.download_button.pack(pady=(0, 10))
    
    def browse_path(self):
        path = filedialog.askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(tk.END, path)
    
    def download_video(self, link, path):
        try:
            yt = YouTube(link)
            if self.download_type.get() == "video":
                video = yt.streams.get_highest_resolution()
                filename = video.default_filename
                video.download(path)
            else:
                audio = yt.streams.filter(only_audio=True).first()
                filename = audio.default_filename.replace("mp4", "mp3")
                file_path = os.path.join(path, filename)
                audio.download(path)
                audio_path = os.path.join(path, audio.default_filename)
                os.rename(os.path.join(path, audio.default_filename), file_path)            
            messagebox.showinfo("Download completato", "Il file è stato scaricato con successo!")
        except Exception as e:
            messagebox.showerror("Errore", str(e))
    
    def download_playlist(self, link, path):
        try:
            playlist = Playlist(link)
            total_videos = len(playlist.video_urls)
            downloaded_videos = 0
            
            for url in playlist.video_urls:
                yt = YouTube(url)
                if self.download_type.get() == "video":
                    video = yt.streams.get_highest_resolution()
                    filename = str(downloaded_videos + 1) + " - " + video.default_filename
                    video.download(path)
                else:
                    audio = yt.streams.filter(only_audio=True).first()
                    filename = audio.default_filename.replace("mp4", "mp3")
                    file_path = os.path.join(path, str(downloaded_videos + 1) + " - " + filename)
                    audio.download(path)
                    os.rename(os.path.join(path, audio.default_filename), file_path)                
                downloaded_videos += 1
                self.progress_bar["value"] = (downloaded_videos / total_videos) * 100
                self.root.update_idletasks()
            
            messagebox.showinfo("Download completato", "La playlist è stata scaricata con successo!")
        except Exception as e:
            messagebox.showerror("Errore", str(e))
    
    def start_download(self):
        link = self.link_entry.get()
        path = self.path_entry.get()
        
        if not link or not path:
            messagebox.showwarning("Attenzione", "Inserisci il link e la cartella di download!")
            return
        
        if "playlist?list=" in link:
            thread = Thread(target=self.download_playlist, args=(link, path))
        else:
            thread = Thread(target=self.download_video, args=(link, path))
        
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = DownloaderApp(root)
    root.mainloop()
