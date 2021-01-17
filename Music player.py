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

channel = pygame.mixer.Channel(1)
volume = 100

song_no = 0

def scan():
    songs = []
    song_no = 0
    for root, dirs, files in os.walk(f"C:/Users/{getpass.getuser()}/{data['play_folder']}"):
        for dir in dirs:
            for root, dirs, files in os.walk(f"C:/Users/{getpass.getuser()}/{data['play_folder']}/{dir}"):
                for file in files:
                    if file.split(".")[-1] == "wav" or file.split(".")[-1] == "mp3":
                        name = " ".join(file.split("_")).split(".")[0]
                        songs.append([name, dir, pygame.mixer.Sound(os.path.join(root, file)), pygame.image.load(os.path.join(root, dir +".jpg"))])
                
    if len(songs) != 0:
        channel.play(songs[0][2])
    return songs, song_no

songs, song_no = scan()

while True:
    screen.fill((255, 255, 255))
    events = pygame.event.get()

    pygame.draw.polygon(screen, (0, 0, 0), [[0, 0], [299, 0], [299, 99], [0, 99]], 1)

    song = songs[song_no]
    font.render(screen, f"{song[0]}", font.centre(f"{song[0]}", (100, 40)))
    font.render(screen, f"{song[1]}", font.centre(f"{song[1]}", (100, 60)))
    font.render(screen, f"{volume}", font.centre(f"{volume}", (180, 90)))
    
    screen.blit(pygame.transform.scale(songs[song_no][3], (100, 100)), (200, 0))

    if not pygame.mixer.get_busy():
        if song_no < len(songs) -1:
            song_no += 1
        else:
            song_no = 0
        
        channel.play(songs[0][2])

    for event in events:
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                pass
            
            elif event.button == 4: # mouse wheel up
                if volume < 100:
                    volume += 5
                    channel.set_volume(volume / 100)
            
            elif event.button == 5: # mouse wheel down
                if volume > 0:
                    volume -= 5
                    channel.set_volume(volume / 100)
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                ctrl = True
            
            elif ctrl:
                if event.key == pygame.K_DELETE:
                    pygame.quit()
                    quit()
                
                elif event.key == pygame.K_r:
                    pygame.mixer.stop()
                    songs, song_no = scan()
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                ctrl = False
    
    pygame.display.update()
    clock.tick(60)