import os
import tkinter as tk
from tkinter import filedialog
from player import MusicPlayer  # اضافه کردن این خط برای وارد کردن کلاس MusicPlayer


class MusicPlayerGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Music Player")
        self.window.geometry("1024x768")
        self.window.configure(bg='#1e1e1e')

        self.player = MusicPlayer()  # ایجاد نمونه‌ای از MusicPlayer

        # منوی کناری
        self.sidebar = tk.Frame(self.window, bg='#292929', width=200)
        self.sidebar.pack(side='left', fill='y')

        # دکمه‌های منوی کناری
        self.home_button = tk.Button(self.sidebar, text="Home", fg='white', bg='#292929', relief='flat', anchor='w',
                                     padx=20)
        self.home_button.pack(fill='x', pady=10)

        self.music_library_button = tk.Button(self.sidebar, text="Music Library", fg='white', bg='#292929',
                                              relief='flat', anchor='w', padx=20)
        self.music_library_button.pack(fill='x', pady=10)

        self.video_library_button = tk.Button(self.sidebar, text="Video Library", fg='white', bg='#292929',
                                              relief='flat', anchor='w', padx=20)
        self.video_library_button.pack(fill='x', pady=10)

        self.play_queue_button = tk.Button(self.sidebar, text="Play Queue", fg='white', bg='#292929', relief='flat',
                                           anchor='w', padx=20)
        self.play_queue_button.pack(fill='x', pady=10)

        self.playlists_button = tk.Button(self.sidebar, text="Playlists", fg='white', bg='#292929', relief='flat',
                                          anchor='w', padx=20)
        self.playlists_button.pack(fill='x', pady=10)

        self.settings_button = tk.Button(self.sidebar, text="Settings", fg='white', bg='#292929', relief='flat',
                                         anchor='w', padx=20, command=self.open_folder_dialog)
        self.settings_button.pack(side='bottom', fill='x', pady=10)

        # بخش اصلی برای نمایش آلبوم‌ها یا آهنگ‌ها
        self.main_frame = tk.Frame(self.window, bg='#1e1e1e')
        self.main_frame.pack(side='right', expand=True, fill='both')

        self.canvas = tk.Canvas(self.main_frame, bg='#1e1e1e')
        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#1e1e1e')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # اضافه کردن آلبوم‌ها (به عنوان نمونه)
        self.album_frames = []
        for i in range(20):
            album_frame = tk.Frame(self.scrollable_frame, bg='#2a2a2a', width=150, height=150)
            album_frame.grid(row=i // 4, column=i % 4, padx=20, pady=20)
            album_label = tk.Label(album_frame, text=f"Album {i + 1}", bg='#2a2a2a', fg='white')
            album_label.pack(expand=True)
            self.album_frames.append(album_frame)

        # نوار پخش در پایین صفحه
        self.bottom_bar = tk.Frame(self.window, bg='#292929', height=50)
        self.bottom_bar.pack(side='bottom', fill='x')

        self.song_label = tk.Label(self.bottom_bar, text="Song Title - Artist", fg='white', bg='#292929')
        self.song_label.pack(side='left', padx=10)

        self.play_button = tk.Button(self.bottom_bar, text="Play", bg='#292929', fg='white', relief='flat')
        self.play_button.pack(side='left')

        self.pause_button = tk.Button(self.bottom_bar, text="Pause", bg='#292929', fg='white', relief='flat')
        self.pause_button.pack(side='left')

        self.next_button = tk.Button(self.bottom_bar, text="Next", bg='#292929', fg='white', relief='flat')
        self.next_button.pack(side='left')

        self.prev_button = tk.Button(self.bottom_bar, text="Prev", bg='#292929', fg='white', relief='flat')
        self.prev_button.pack(side='left')

        self.volume_slider = tk.Scale(self.bottom_bar, from_=0, to=100, orient='horizontal', bg='#292929', fg='white',
                                      relief='flat')
        self.volume_slider.pack(side='right', padx=10)

    def open_folder_dialog(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.player.load_music(folder_path)
            self.update_album_list()

    def update_album_list(self):
        for frame in self.album_frames:
            frame.destroy()
        self.album_frames = []

        for index, file in enumerate(self.player.music_files):
            album_frame = tk.Frame(self.scrollable_frame, bg='#2a2a2a', width=150, height=150)
            album_frame.grid(row=index // 4, column=index % 4, padx=20, pady=20)
            album_label = tk.Label(album_frame, text=os.path.basename(file), bg='#2a2a2a', fg='white')
            album_label.pack(expand=True)
            self.album_frames.append(album_frame)


if __name__ == "__main__":
    main_window = tk.Tk()
    app = MusicPlayerGUI(main_window)
    main_window.mainloop()
