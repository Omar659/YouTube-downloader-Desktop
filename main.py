import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pytubefix import YouTube, Playlist
from threading import Thread
import os

class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader Semplificato")
        self.root.geometry("450x450")
        self.root.resizable(False, False)

        # Stile
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", background="#FF0000", foreground="white", font=("Helvetica", 10, "bold"), borderwidth=0)
        self.style.map("TButton", background=[('active', '#CC0000')])
        self.style.configure("TLabel", background="#f0f0f0", foreground="#333", font=("Helvetica", 10))
        self.style.configure("TEntry", fieldbackground="#fff")
        self.style.configure("TRadiobutton", background="#f0f0f0")
        
        # Frame principale
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill="both", expand=True)

        # --- WIDGETS ---
        self.link_label = ttk.Label(self.main_frame, text="Link del video o della playlist:")
        self.link_label.pack(anchor="w", pady=(0, 5))
        
        self.link_entry = ttk.Entry(self.main_frame, width=50)
        self.link_entry.pack(fill="x", pady=(0, 10))
        
        self.path_label = ttk.Label(self.main_frame, text="Cartella di download:")
        self.path_label.pack(anchor="w", pady=(0, 5))
        
        self.path_frame = ttk.Frame(self.main_frame)
        self.path_frame.pack(fill="x", pady=(0, 10))
        self.path_entry = ttk.Entry(self.path_frame, width=40)
        self.path_entry.pack(side="left", fill="x", expand=True)
        self.browse_button = ttk.Button(self.path_frame, text="Sfoglia", command=self.browse_path)
        self.browse_button.pack(side="left", padx=(5, 0))
        
        self.download_type = tk.StringVar(value="video")
        self.video_radio = ttk.Radiobutton(self.main_frame, text="Scarica video (MP4)", variable=self.download_type, value="video")
        self.video_radio.pack(anchor="w", pady=(0, 5))
        self.audio_radio = ttk.Radiobutton(self.main_frame, text="Scarica solo audio (formato m4a)", variable=self.download_type, value="audio")
        self.audio_radio.pack(anchor="w", pady=(0, 20))
        
        self.download_button = ttk.Button(self.main_frame, text="Scarica", command=self.start_download_thread)
        self.download_button.pack(pady=(0, 10), ipady=5, fill='x')
        
        self.progress_label = ttk.Label(self.main_frame, text="")
        self.progress_label.pack(anchor="w", pady=(10, 5))
        
        self.progress_bar = ttk.Progressbar(self.main_frame, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=(0, 10), fill='x')

        self.status_label = ttk.Label(self.main_frame, text="Pronto per il download.", font=("Helvetica", 9, "italic"))
        self.status_label.pack(anchor="w", pady=(5, 0))
    
    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(tk.END, path)

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        self.progress_bar["value"] = percentage
        self.progress_label.config(text=f"{int(percentage)}% - {bytes_downloaded/1024/1024:.2f} MB / {total_size/1024/1024:.2f} MB")
        self.root.update_idletasks()

    def start_download_thread(self):
        link = self.link_entry.get()
        path = self.path_entry.get()
        
        if not link or not path:
            messagebox.showwarning("Attenzione", "Inserisci sia il link sia la cartella di download!")
            return

        if not os.path.isdir(path):
            messagebox.showerror("Errore", "La cartella di download non è valida.")
            return

        self.download_button.config(state=tk.DISABLED, text="Download in corso...")
        self.progress_bar["value"] = 0
        self.progress_label.config(text="")
        
        thread = Thread(target=self.download_logic, args=(link, path), daemon=True)
        thread.start()

    def download_logic(self, link, path):
        try:
            urls = []
            is_playlist = "playlist?list=" in link
            
            if is_playlist:
                self.status_label.config(text="Sto analizzando la playlist...")
                p = Playlist(link)
                urls = p.video_urls
                self.status_label.config(text=f"Trovati {len(urls)} video nella playlist.")
            else:
                urls.append(link)

            for i, url in enumerate(urls):
                yt = YouTube(url, on_progress_callback=self.on_progress)
                self.status_label.config(text=f"({i+1}/{len(urls)}) Scaricando: {yt.title[:40]}...")
                self.root.update_idletasks()
                
                if self.download_type.get() == "video":
                    stream = yt.streams.get_highest_resolution()
                else: # Audio
                    stream = yt.streams.get_audio_only()
                
                stream.download(path)

            self.status_label.config(text="Download completato con successo!")
            messagebox.showinfo("Finito!", "Tutti i file sono stati scaricati correttamente.")

        except Exception as e:
            error_message = f"Errore: {str(e)}"
            self.status_label.config(text=error_message)
            messagebox.showerror("Errore di Download", error_message)
        finally:
            self.download_button.config(state=tk.NORMAL, text="Scarica")
            self.progress_bar["value"] = 0
            self.progress_label.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    app = DownloaderApp(root)
    root.mainloop()