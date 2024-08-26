import os
import random
import pygame


class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.music_files = []
        self.current_index = 0
        self.is_playing = False

    def load_music(self, folder_path):
        self.music_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if
                            file.endswith('.mp3')]
        if self.music_files:
            self.current_index = 0
            self.play_music()

    def play_music(self):
        if not self.is_playing:
            pygame.mixer.music.load(self.music_files[self.current_index])
            pygame.mixer.music.play()
            self.is_playing = True

    def pause_music(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True

    def next_music(self):
        self.current_index = (self.current_index + 1) % len(self.music_files)
        self.play_music()

    def previous_music(self):
        self.current_index = (self.current_index - 1) % len(self.music_files)
        self.play_music()

    def shuffle_music(self):
        random.shuffle(self.music_files)
        self.current_index = 0
        self.play_music()
