import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Main Menu")
screen_width=screen.get_width()
screen_height=screen.get_height()
screen_center_x = screen_width // 2
screen_center_y = screen_height // 2

WHITE = (255,255,255)
LIGHT = (170,170,170)
DARK = (100,100,100)
BG = (52,78,91)

menubutton_size= (screen_width*0.09)

title_font= pygame.font.Font("assets/Conflict3040-WpnRV.ttf", 160)
font = pygame.font.SysFont("Corbel", 40)

try:
    menu_background = pygame.image.load("assets/menu_bg.png")
    menu_background = pygame.transform.scale(menu_background, (screen_width, screen_height))
except pygame.error:
    menu_background = pygame.Surface((screen_width, screen_height))
    menu_background.fill((52,78,91))

try:
    play_img = pygame.image.load("assets/menu_buttons/large_buttons/colored_large_buttons/playcol_button.png").convert_alpha()
    play_img = pygame.transform.scale(play_img, (menubutton_size, menubutton_size))
    play_mask = pygame.mask.from_surface(play_img)
    quit_img = pygame.image.load("assets/menu_buttons/large_buttons/colored_large_buttons/quitcol_button.png").convert_alpha()
    quit_img = pygame.transform.scale(quit_img, (menubutton_size, menubutton_size))
    quit_mask = pygame.mask.from_surface(quit_img)
except:
    play_img = pygame.Surface((menubutton_size, menubutton_size))
    play_img.fill((0, 255, 0))
    quit_img = pygame.Surface((menubutton_size, menubutton_size))
    quit_img.fill((0, 255, 0))

title_surface = title_font.render("PLACEHOLDER", True, (250, 230, 214)) 
title_rect = title_surface.get_rect(center=(screen_center_x, screen_center_y - 450)) 

def game():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((40, 40, 40))

        text = font.render("Game Started!", True, WHITE)

        text_rect = text.get_rect(center=(screen_center_x, screen_center_y))        
        screen.blit(text, text_rect)

        pygame.display.update()

def start_menu():
    play_button=play_img.get_rect()
    quit_button=quit_img.get_rect()

    play_button.center = (screen_center_x - 365 , screen_center_y - (menubutton_size // 2) - 20)
    quit_button.center = (screen_center_x + 365, screen_center_y - (menubutton_size // 2) - 20)
    
    while True:
        screen.blit(menu_background, (0,0))
        
        screen.blit(play_img, play_button.topleft)
        screen.blit(quit_img, quit_button.topleft)

        screen.blit(title_surface,title_rect)        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button ==1:
                    mouse_x, mouse_y = event.pos
                
                if play_button.collidepoint(mouse_x, mouse_y):
                    offset_x = mouse_x - play_button.x
                    offset_y = mouse_y - play_button.y
                    if play_mask.get_at((offset_x, offset_y)):
                        game()
                if quit_button.collidepoint(mouse_x, mouse_y):
                    offset_x = mouse_x - quit_button.x
                    offset_y = mouse_y - quit_button.y
                    if quit_mask.get_at((offset_x, offset_y)):
                        pygame.quit()
                    sys.exit()
                    
        pygame.display.update()

start_menu()
