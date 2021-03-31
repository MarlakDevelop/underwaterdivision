import pygame


def play_game():
    pygame.mixer.music.load('assets/music/game.mp3')
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)


def play_menu():
    pygame.mixer.music.load('assets/music/menu.mp3')
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)


def stop_music():
    pygame.mixer.music.stop()
