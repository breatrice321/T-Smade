# play music

from mutagen.mp3 import MP3
import pygame 
import os  
import time


def play_music():
    # achieve the name of music
    file_dir = "./extra_data/music/"
    files = os.listdir(file_dir)

    # play music
    time_init = time.time()
    state = True
    while state:
        for file_mp3 in files:
            pygame.init()  
            pygame.mixer.init()  

            print("play music " + file_mp3)
            audio = MP3(file_dir + file_mp3)
            duration = audio.info.length  
            print(duration)
            pygame.mixer.music.load(file_dir + file_mp3)  
            # pygame.mixer.music.set_volume(0.4)          
            pygame.mixer.music.play()  
            time.sleep(duration)
            pygame.mixer.music.stop()

            if time.time() - time_init > 598:
                break

        if time.time() - time_init > 598:
            state = False

if __name__ == "__main__":
    play_music()