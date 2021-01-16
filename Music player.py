import pygame
import os
import json
from ctypes import windll
import getpass

SetWindowPos = windll.user32.SetWindowPos
with open("config.json") as file:
    data = json.load(file)
    file.close()

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((300, 100), pygame.NOFRAME)

SetWindowPos(pygame.display.get_wm_info()['window'], -1, data["window_position"][0], data["window_position"][1], 0, 0, 0x0001)

ctrl = False

songs = []
for root, dirs, files in os.walk(f"C:/Users/{getpass.getuser()}/Music", topdown=False):
    for file in files:
        if file.split(".")[-1] == "wav" or file.split(".")[-1] == "mp3":
            songs.append(pygame.mixer.Sound(os.path.join(root, file)))
    for dir in dirs:
        for file in dir:
            if file.split(".")[-1] == "wav" or file.split(".")[-1] == "mp3":
                songs.append(pygame.mixer.Sound(os.path.join(root, file)))

print(len(songs))

while True:
    screen.fill((255, 255, 255))
    events = pygame.event.get()

    pygame.draw.polygon(screen, (0, 0, 0), [[0, 0], [299, 0], [299, 99], [0, 99]], 1)

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
                    # Refresh
                    pass
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                ctrl = False
    
    pygame.display.update()
    clock.tick(60)