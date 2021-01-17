import pygame
import os
import json
from ctypes import windll
import getpass

from Data.font import Font

SetWindowPos = windll.user32.SetWindowPos

with open("Data/config.json") as file:
    data = json.load(file)
    file.close()

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((300, 100), pygame.NOFRAME)

SetWindowPos(pygame.display.get_wm_info()['window'], -1, data["window_position"][0], data["window_position"][1], 0, 0, 0x0001)

ctrl = False

font = Font("Data/small_font.png", (1, 1, 1), 3, 1)

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
                        sound = pygame.mixer.Sound(os.path.join(root, file))
                        try:
                            try:
                                image = pygame.image.load(os.path.join(root, dir +".jpg"))
                            except Exception:
                                image = pygame.image.load(os.path.join(root, dir +".png"))
                        except Exception:
                            image = None
                        songs.append([name, dir, sound, image])
                
    if len(songs) != 0:
        channel.play(songs[0][2])
    return songs, song_no

songs, song_no = scan()

while True:
    screen.fill((255, 255, 255))
    events = pygame.event.get()

    pygame.draw.polygon(screen, (0, 0, 0), [[0, 0], [199, 0], [199, 99], [0, 99]], 1)
    pygame.draw.polygon(screen, (0, 0, 0), [[199, 0], [299, 0], [299, 99], [199, 99]], 1)

    if not pygame.mixer.get_busy():
        if song_no < len(songs) - 1:
            song_no += 1
        else:
            song_no = 0
        
        channel.play(songs[song_no][2])

    song = songs[song_no]
    if len(song[0]) > 30:
        name = [song[0][:len(song[0]) // 2], song[0][len(song[0]) // 2:]]
        if len(name[0]) < 20:
            font.render(screen, f"{name[0]}", font.centre(f"{name[0]}", (100, 40)))
            font.render(screen, f"{name[1]}", font.centre(f"{name[1]}", (100, 60)))
            font.render(screen, f"{song[1]}", font.centre(f"{song[1]}", (100, 80)))
        else:
            name = [song[0][: len(song[0]) // 3], song[0][len(song[0]) // 3 : (len(song[0]) // 3) * 2], song[0][(len(song[0]) // 3) * 2 :]]
            font.render(screen, f"{name[0]}", font.centre(f"{name[0]}", (100, 20)))
            font.render(screen, f"{name[1]}", font.centre(f"{name[1]}", (100, 40)))
            font.render(screen, f"{name[2]}", font.centre(f"{name[2]}", (100, 60)))
            font.render(screen, f"{song[1]}", font.centre(f"{song[1]}", (100, 80)))
    else:
        font.render(screen, f"{song[0]}", font.centre(f"{song[0]}", (100, 40)))
        font.render(screen, f"{song[1]}", font.centre(f"{song[1]}", (100, 60)))

    font.render(screen, f"{volume}", font.centre(f"{volume}", (180, 90)))
    
    try:
        screen.blit(pygame.transform.scale(songs[song_no][3], (100, 100)), (200, 0))
    except Exception:
        font.render(screen, "Img not", font.centre("Img not", (250, 40)))
        font.render(screen, "found", font.centre("found", (250, 60)))

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
            
            elif event.key == pygame.K_UP:
                if volume < 100:
                    volume += 5
                    channel.set_volume(volume / 100)
            
            elif event.key == pygame.K_DOWN:
                if volume > 0:
                    volume -= 5
                    channel.set_volume(volume / 100)
            
            elif event.key == pygame.K_RIGHT:
                channel.stop()
                if song_no < len(songs) - 1:
                    song_no += 1
                else:
                    song_no = 0
        
                channel.play(songs[song_no][2])
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                ctrl = False
    
    pygame.display.update()
    clock.tick(60)