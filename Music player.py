import pygame
import os
import json
from ctypes import windll
import getpass
from font import Font

SetWindowPos = windll.user32.SetWindowPos
with open("config.json") as file:
    data = json.load(file)
    file.close()

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((300, 100), pygame.NOFRAME)

SetWindowPos(pygame.display.get_wm_info()['window'], -1, data["window_position"][0], data["window_position"][1], 0, 0, 0x0001)

ctrl = False

font = Font("small_font.png", (1, 1, 1), 3, 1)

songs = []
song_no = 0

# for root, dirs, files in os.walk(f"C:/Users/{getpass.getuser()}/{data["play_folder"]}"):
for root, dirs, files in os.walk(f"C:/Users/{getpass.getuser()}/Music/Music Player"):
    for file in files:
        if file.split(".")[-1] == "wav" or file.split(".")[-1] == "mp3":
            songs.append([file, pygame.mixer.Sound(os.path.join(root, file)), pygame.image.load(os.path.join(root, file.split(".")[0] +".jpg"))])
    for dir in dirs:
        for file in dir:
            if file.split(".")[-1] == "wav" or file.split(".")[-1] == "mp3":
                songs.append([file, pygame.mixer.Sound(os.path.join(root, file)), pygame.image.load(os.path.join(root, file.split(".")[0] +".jpg"))])

if len(songs) != 0:
    songs[0][1].play()

while True:
    screen.fill((255, 255, 255))
    events = pygame.event.get()

    pygame.draw.polygon(screen, (0, 0, 0), [[0, 0], [299, 0], [299, 99], [0, 99]], 1)

    # screen.blit(font.fontsheet, (1, 1))

    name = " ".join(songs[song_no][0].split("_"))
    # font.render(screen, f"{name}", font.centre(f"{name}", (100, 50)))
    font.render(screen, f"{name}", (1, 1))
    screen.blit(pygame.transform.scale(songs[song_no][2], (100, 100)), (200, 0))

    if not pygame.mixer.get_busy():
        if song_no < len(songs) -1:
            song_no += 1
        else:
            song_no = 0
        
        songs[song_no][1].play()

    for event in events:
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                pass
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                ctrl = True
            
            elif ctrl:
                if event.key == pygame.K_DELETE:
                    pygame.quit()
                    quit()
                
                elif event.key == pygame.K_r:
                    pygame.mixer.stop()
                    songs = []
                    for root, dirs, files in os.walk(f"C:/Users/{getpass.getuser()}/Music", topdown=False):
                        for file in files:
                            if file.split(".")[-1] == "wav" or file.split(".")[-1] == "mp3":
                                songs.append(pygame.mixer.Sound(os.path.join(root, file)))
                        for dir in dirs:
                            for file in dir:
                                if file.split(".")[-1] == "wav" or file.split(".")[-1] == "mp3":
                                    songs.append(pygame.mixer.Sound(os.path.join(root, file)))
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                ctrl = False
    
    pygame.display.update()
    clock.tick(60)