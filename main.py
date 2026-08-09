import pygame
import sys
import random

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
RED = (255, 50, 50)
GREEN = (50, 255, 50)
YELLOW = (255, 255, 50)

menubutton_size= (screen_width*0.09)

title_font= pygame.font.Font("assets/Conflict3040-WpnRV.ttf", 160)
font = pygame.font.SysFont("Corbel", 40)
ui_font = pygame.font.SysFont("Corbel", 30)
math_font = pygame.font.SysFont("Corbel", 60, bold=True)

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

def gen_math_question():
    operators = ["+", "-", "*"]
    operator = random.choice(operators)
    if operator == "+":
        a, b = random.randint(1, 20), random.randint(1, 20)
        answer = a + b
    elif operator =="-":
        a, b = random.randint(1, 30), random.randint(1, 10)
        answer = a - b
    else:
        a, b = random.randint(2, 9), random.randint(2, 9)
        answer = a * b
    return f"{a} {operator} {b}", str(answer)
        
        
def game():
    clock=pygame.time.Clock()

    player_rect = pygame.Rect(screen_center_x - 25, screen_height - 100, 50, 50)
    player_speed = 7

    bullets=[]
    enemies=[]

    start_time = pygame.time.get_ticks()
    kill_score = 0

    enemy_spawn_timer=0
    enemy_spawn_rate = 1500

    base_fire_rate = 400
    fast_fire_rate = 150
    slow_fire_rate = 900
    current_fire_rate = base_fire_rate

    last_shot_time = 0
    buff_end_time=0
    fire_status = "Normal"
    fire_status_colour = WHITE

    math_question_active = False
    question_text = ""
    correct_answer = ""
    player_input = ""
    math_start_time = 0
    last_question_time = pygame.time.get_ticks()
    math_question_interval = 8000
    math_time_limit = 5000
    game_over = False
    
    while True:
        current_time=pygame.time.get_ticks()
        
        for event in pygame.event.get():
              if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

              if event.type == pygame.KEYDOWN and math_question_active and not game_over:
                if event.key == pygame.K_RETURN:

                    if player_input == correct_answer:
                        current_fire_rate = fast_fire_rate
                        fire_status=("Attack Speed up!")
                        fire_status_colour=GREEN
                    else:
                        current_fire_rate = slow_fire_rate
                        fire_status=("Attack Speed down!")
                        fire_status_colour=RED

                    buff_end_time = current_time + 5000
                    math_question_active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_input = player_input[:-1]
                elif event.unicode.isnumeric() or (event.unicode == "-" and len(player_input) == 0):
                    player_input += event.unicode

              if event.type == pygame.KEYDOWN and game_over:
                  if event.key == pygame.K_ESCAPE:
                    return

        if not game_over:
            if current_time > buff_end_time and buff_end_time != 0:
                current_fire_rate= base_fire_rate
                fire_status = "Normal"
                fire_status_colour= WHITE
                buff_end_time =0

        if not math_question_active and current_time - last_question_time > math_question_interval:
            question_text, correct_answer = gen_math_question()
            player_input = ""
            math_question_active = True
            math_start_time = current_time

        if math_question_active and current_time - math_start_time > math_time_limit:
            current_fire_rate = slow_fire_rate
            fire_status = "Attack Speed Down!"
            fire_status_colour=RED
            buff_end_time = current_time + 5000
            math_question_active = False
            last_question_time = current_time

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_rect.x += player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_rect.y += player_speed

        if keys[pygame.K_SPACE]:
            if current_time - last_shot_time > current_fire_rate:
                bullet=pygame.Rect(player_rect.centerx - 5, player_rect.top, 10, 20)
                last_shot_time = current_time
                bullets.append(bullet)
                last_shot_time = current_time

        if current_time - enemy_spawn_timer > enemy_spawn_rate:
            enemy_x = random.randint(0, screen_width - 40)
            enemy = pygame.Rect(enemy_x, - 40, 40, 40)
            enemies.append(enemy)
            enemy_spawn_timer=current_time
            enemy_spawn_rate = max(500, enemy_spawn_rate-10)

        for bullet in bullets[:]:
            bullet.y -= 15
            if bullet.bottom < 0:
                bullets.remove(bullet)

        for enemy in enemies[:]:
            enemy.y += 5
            if enemy.colliderect(player_rect):
                game_over=True
            hit=False
            for bullet in bullets[:]:
                if enemy.colliderect(bullet):
                    if bullet in bullets: bullets.remove(bullet)
                    hit = True
                    kill_score += 5
                    break
            if hit:
                if enemy in enemies: enemies.remove(enemy)
            elif enemy.top > screen_height:
                enemies.remove(enemy)
            
        time_alive = (current_time-start_time) // 1000
        total_score = time_alive+kill_score
                    
        screen.fill((20, 25, 40))

        if not game_over:
            pygame.draw.rect(screen, (100, 200, 255), player_rect)

            for bullet in bullets:
                pygame.draw.rect(screen, YELLOW, bullet)

            for enemy in enemies:
                pygame.draw.rect(screen, RED, enemy)
            
        

            score_text = ui_font.render(f"Score: {total_score}", True, WHITE)
            screen.blit(score_text, (20,20))

            status_text = ui_font.render(f"Attack Speed: {fire_status}", True, fire_status_colour)
            screen.blit(status_text, (20,60))

            if math_question_active:
                panel_rect= pygame.Rect(screen_center_x - 200, 50, 400, 150)
                pygame.draw.rect(screen, (30, 30, 50), panel_rect)
                pygame.draw.rect(screen, WHITE, panel_rect, 3)

                q_surf = math_font.render(f"{question_text} = ?", True, WHITE)
                q_rect = q_surf.get_rect(center=(screen_center_x, 90))
                screen.blit(q_surf, q_rect)

                ans_surf = math_font.render(player_input, True, YELLOW)
                ans_rect = ans_surf.get_rect(center=(screen_center_x, 150))
                screen.blit(ans_surf, ans_rect)

                time_left = math_time_limit- ( current_time- math_start_time)
                bar_width= int((time_left / math_time_limit) * 380)
                pygame.draw.rect(screen, RED, (screen_center_x - 190, 180, bar_width, 10))
        else:
            game_over_text=title_font.render("GAME OVER", True, RED)
            game_over_rect = game_over_text.get_rect(center=(screen_center_x, screen_center_y - 100))
            screen.blit(game_over_text, game_over_rect)

            final_score_text = font.render(f"Final Score: {total_score}", True, WHITE)
            final_score_rect= final_score_text.get_rect(center=(screen_center_x, screen_center_y + 50))
            screen.blit(final_score_text, final_score_rect)

            esc_text= ui_font.render("Press esc to return to the Main Menu", True, LIGHT)
            esc_rect = esc_text.get_rect(center=(screen_center_x, screen_center_y + 120))
            screen.blit(esc_text, esc_rect)

        pygame.display.update()
        clock.tick(60)

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
