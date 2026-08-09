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
CYAN = (80, 220, 220)
PURPLE = (180, 80, 255)
ORANGE = (255, 140, 0)
GOLD = (255, 215, 0)


menubutton_size= (screen_width*0.09)

title_font= pygame.font.Font("assets/Conflict3040-WpnRV.ttf", 160)
font = pygame.font.SysFont("Corbel", 40)
ui_font = pygame.font.SysFont("Corbel", 30)
math_font = pygame.font.SysFont("Corbel", 60, bold=True)
small_font = pygame.font.SysFont("Corbel", 24)
wave_font = pygame.font.SysFont("Corbel", 90, bold=True)
powerup_font = pygame.font.SysFont("Corbel", 44, bold=True)

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
    play_mask = pygame.mask.from_surface(play_img)
    quit_mask = pygame.mask.from_surface(quit_img)

title_surface = title_font.render("PLACEHOLDER", True, (250, 230, 214)) 
title_rect = title_surface.get_rect(center=(screen_center_x, screen_center_y - 450)) 

cell_size = 90
grid_columns = max(3, screen_width // cell_size)
grid_rows = max(3, screen_height // cell_size)
player_row_minimum = max(0, grid_rows - 4)
player_row_maximum = grid_rows - 1
player_size = cell_size - 20
enemy_size = cell_size-20
boss_size = cell_size*2-10
bullet_width = 10
bullet_height = 20
bullet_speed = 16

wave_count = 9
starting_lives = 3
max_lives = 5
max_escapes = 3
invulnerability_duration= 600
wave_intro_duration = 2000 

base_fire_rate = 400
fast_fire_rate = 150
slow_fire_rate = 900
multishot_duration = 6000

boss_descend_speed = 0.5
boss_side_speed = 3.0
boss_starting_hp = 20

powerup_types = ["fast_fire", "shield", "multishot", "oneup", "nuke"]
powerup_messages = {"fast_fire": "Reward: Attack Speed Up!", "shield": "Reward: Shield!", "multishot": "Reward: MultiShot!", "oneup": "Reward: Extra Life!", "nuke": "Reward: Nuke!",}

power_colours= {"fast_fire": GREEN, "shield": CYAN, "multishot": PURPLE, "oneup": RED, "nuke": ORANGE,}
powerup_messages_duration = 2500

leaderboard_file = "leaderboard.txt"

def col_x(col):
    return col*cell_size+cell_size//2

def row_y(row):
    return row* cell_size + cell_size//2

def is_boss_wave(wave):
    #a boss shows up every 3rd wave so wave 3, 6 and 9 out of 9 total
    return wave % 3 == 0

def load_leaderboard():
    entries = []
    try:
        lb_file = open(leaderboard_file, "r")
        for line in lb_file:
            line = line.strip()
            if line == "":
                continue
            parts = line.split(",")
            if len(parts) == 2:
                name = parts[0]
                score = int(parts[1])
                entries.append((name, score))
        lb_file.close()
    except FileNotFoundError:
        entries = []
    entries.sort(key=lambda e: e[1], reverse=True)
    return entries[:10]

def save_leaderboard_entry(name, score):
    entries = load_leaderboard()
    entries.append((name, score))
    entries.sort(key=lambda e: e[1], reverse=True)
    entries = entries[:10]
    lb_file = open(leaderboard_file, "w")
    for entry in entries:
        lb_file.write(entry[0] + "," + str(entry[1]) + "\n")
    lb_file.close()
    return entries

def gen_math_question(stage):
    if stage == 1:
        #basic arithmetic addition, subtraction, multiplication, division
        operator = random.choice(["+", "-", "*", "/"])
        if operator == "+":
            a, b = random.randint(1, 20), random.randint(1, 20)
            answer = a + b
        elif operator =="-":
            a, b = random.randint(1, 30), random.randint(1, 10)
            answer = a - b
        elif operator == "*":
            a, b = random.randint(2, 9), random.randint(2, 9)
            answer = a * b
        else:
            b = random.randint(2, 10)
            answer = random.randint(2, 10)
            a = b * answer
        return f"{a} {operator} {b}", str(answer)

    elif stage == 2:
        # fractions and percentages
        kind = random.choice(["fraction", "percentage"])
        if kind == "fraction":
            d = random.choice([2, 3, 4, 5, 10])
            k = random.randint(2, 10)
            base = d * k
            n = random.randint(1, d - 1)
            answer = k * n
            return f"{n}/{d} of {base}", str(answer)
        else:
            percent = random.choice([10, 20, 25, 50])
            if percent == 10:
                base = random.randint(2, 20) * 10
            elif percent == 20:
                base = random.randint(2, 20) * 5
            elif percent == 25:
                base = random.randint(2, 20) * 4
            else:
                base = random.randint(2, 20) * 2
            answer = percent * base // 100
            return f"{percent}% of {base}", str(answer)

    else:
        #exponents, powers and roots
        kind = random.choice(["square", "cube", "sqrt", "power"])
        if kind == "square":
            a = random.randint(2, 15)
            return f"{a}^2", str(a * a)
        elif kind == "cube":
            a = random.randint(2, 9)
            return f"{a}^3", str(a ** 3)
        elif kind == "sqrt":
            r = random.randint(2, 12)
            a = r * r
            return f"sqrt({a})", str(r)
        else:
            base = random.randint(2, 5)
            exp = random.randint(2, 4)
            return f"{base}^{exp}", str(base ** exp)
        
def wave_enemy_count(wave):
    return 4 + (wave - 1) * 1
 
def wave_enemy_speed(wave):
    return 2.5 + (wave - 1) * 0.2
 
def wave_spawn_rate(wave):
    return max(500, 1100 - (wave - 1) * 40)

def create_enemy(wave):
    column = random.randint(0, grid_columns - 1)
    return {"x": col_x(column), "y": float(-enemy_size), "speed": wave_enemy_speed(wave), "rect": pygame.Rect(0, 0, enemy_size, enemy_size),}

def create_boss():
    return {"x": float(col_x(grid_columns // 2)), "y": float(-boss_size),"hp": boss_starting_hp,"max_hp": boss_starting_hp, "dir": 1,"rect": pygame.Rect(0, 0,boss_size, boss_size),}

def apply_powerup(powerup_types, current_time, game_vars):
    if powerup_types == "fast_fire":
        game_vars["current_fire_rate"] = fast_fire_rate
        game_vars["buff_end_time"] = current_time + 5000
        game_vars["fire_status"] = "Attack Speed Up!"
        game_vars["fire_status_colour"] = GREEN
 
    elif powerup_types == "shield":
        game_vars["shield_active"] = True
 
    elif powerup_types == "multishot":
        game_vars["multishot_end_time"] = max(game_vars["multishot_end_time"], current_time) + multishot_duration
 
    elif powerup_types == "oneup":
        game_vars["lives"] = min(max_lives, game_vars["lives"] + 1)
 
    elif powerup_types == "nuke":
        for enemy in game_vars["enemies"][:]:
            game_vars["kill_score"] += 5
            game_vars["enemies"].remove(enemy)
        if game_vars["boss"] is not None:
            game_vars["boss"]["hp"] -= 8
            if game_vars["boss"]["hp"] <= 0:
                game_vars["kill_score"] += 100
                game_vars["boss"] = None
 
    return game_vars

def draw_grid(surface):
    for gx in range(grid_columns + 1):
        x = gx * cell_size
        pygame.draw.line(surface, (35, 45, 65), (x, 0), (x, screen_height), 1)
    for gy in range(grid_rows + 1):
        y = gy * cell_size
        pygame.draw.line(surface, (35, 45, 65), (0, y), (screen_width, y), 1)

def draw_stats_panel(surface, stats):
    panel_x, panel_y = 20, 20
    lives_text = ("Lives: " + "Heart " * stats["lives"]).strip() if stats["lives"] > 0 else "Lives: 0"
    lines = [(f"Score: {stats['total_score']}", WHITE), (f"Wave: {stats['wave'] if not is_boss_wave(stats['wave']) else 'boss'} / {wave_count}", WHITE),(f"Lives: {stats['lives']}", RED if stats["lives"] <= 1 else WHITE), (f"Escapes: {stats['escapes']} / {max_escapes}", ORANGE if stats["escapes"] > 0 else WHITE),
    (f"Attack Speed: {stats['fire_status']}", stats["fire_status_colour"])]

    active_effects = []
    if stats["shield_active"]:
        active_effects.append("Shield: ON")
    if stats["current_time"] < stats["multishot_end_time"]:
        secs_left = (stats["multishot_end_time"] - stats["current_time"]) / 1000
        active_effects.append(f"MultiShot: {secs_left:.1f}s")
    if active_effects:
        lines.append((" | ".join(active_effects), CYAN))
 
    for i, (text, colour) in enumerate(lines):
        surf = ui_font.render(text, True, colour)
        surface.blit(surf, (panel_x, panel_y + i * 34))


def game():
    clock=pygame.time.Clock()

    player_column = grid_columns //2
    player_row = player_row_maximum
    player_width = player_size
    player_height = player_size    
    bullets = []
    enemies = []    
    boss = None 
    start_time=pygame.time.get_ticks()
    kill_score =0

    current_fire_rate=base_fire_rate
    last_shot_time = 0
    buff_end_time= 0
    fire_status ="Normal"
    fire_status_colour = WHITE

    current_powerup_message = ""
    current_powerup_colour = WHITE
    power_message_until = 0
    lives = starting_lives
    escapes = 0
    invulnerability_until = 0
    shield_active = False
    multishot_end_time = 0

    wave=1
    math_stage = 1
    enemies_spawned_this_wave = 0
    enemy_spawn_timer = 0
    boss_spawned= False

    state = "wave_intro" 
    wave_intro_start = pygame.time.get_ticks()
    total_score = 0
    game_over_reason = ""

    name_input = ""
    score_saved = False

    math_question_active = False
    question_text = ""
    correct_answer = ""
    player_input = ""
    math_start_time = 0
    last_question_time = pygame.time.get_ticks()
    math_question_interval = 8000
    math_time_limit = 5000
    
    while True:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
 
            if event.type == pygame.KEYDOWN:
                if state in ("game_over", "win"):
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_RETURN:
                        if not score_saved:
                            entry_name = name_input.strip() if name_input.strip() != "" else "PLAYER"
                            save_leaderboard_entry(entry_name, total_score)
                            score_saved = True
                    elif event.key == pygame.K_BACKSPACE:
                        name_input = name_input[:-1]
                    elif event.unicode.isalnum() and len(name_input) < 12:
                        name_input += event.unicode.upper()
                elif state in ("playing", "wave_intro"):

                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        player_column = max(0, player_column - 1)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        player_column = min(grid_columns - 1, player_column + 1)
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        player_row = max(player_row_minimum, player_row - 1)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        player_row = min(player_row_maximum, player_row + 1)
 
                    if math_question_active:
                        if event.key == pygame.K_RETURN:
                            if player_input == correct_answer:
                                chosen_powerup = random.choice(powerup_types)
                                game_vars = {"current_fire_rate": current_fire_rate, "buff_end_time": buff_end_time,"fire_status": fire_status, "fire_status_colour": fire_status_colour, "shield_active": shield_active, "multishot_end_time": multishot_end_time, "lives": lives, "enemies": enemies, "boss": boss, "kill_score": kill_score,}

                                game_vars = apply_powerup(chosen_powerup, current_time, game_vars)
                                current_fire_rate = game_vars["current_fire_rate"]
                                buff_end_time = game_vars["buff_end_time"]
                                fire_status = game_vars["fire_status"]
                                fire_status_colour = game_vars["fire_status_colour"]
                                shield_active = game_vars["shield_active"]
                                multishot_end_time = game_vars["multishot_end_time"]
                                lives = game_vars["lives"]
                                boss = game_vars["boss"]
                                kill_score = game_vars["kill_score"]
 
                                current_powerup_message = powerup_messages[chosen_powerup]
                                current_powerup_colour = power_colours[chosen_powerup]
                                power_message_until = current_time + powerup_messages_duration
                            else:
                                current_fire_rate = slow_fire_rate
                                fire_status = "Attack Speed Down!"
                                fire_status_colour = RED
                                buff_end_time = current_time + 5000
                            math_question_active = False
                        elif event.key == pygame.K_BACKSPACE:
                            player_input = player_input[:-1]
                        elif event.unicode.isnumeric() or (event.unicode == "-" and len(player_input) == 0):
                            player_input += event.unicode

        player_rect = pygame.Rect(0, 0, player_width, player_height)
        player_rect.center = (col_x(player_column), row_y(player_row))

        if math_question_active and current_time - math_start_time > math_time_limit:
            current_fire_rate = slow_fire_rate
            fire_status = "Attack Speed Down!"
            fire_status_colour = RED
            buff_end_time = current_time + 5000
            math_question_active = False
            last_question_time = current_time

        if state == "wave_intro":
            if current_time - wave_intro_start > wave_intro_duration:
                state = "playing"
                bullets.clear()
                enemies_spawned_this_wave = 0
                enemy_spawn_timer = current_time
                if is_boss_wave(wave):
                    boss = create_boss()
                    boss_spawned = True
                else:
                    boss = None

        elif state == "playing":
            if current_time > buff_end_time and buff_end_time != 0:
                current_fire_rate = base_fire_rate
                fire_status = "Normal"
                fire_status_colour = WHITE
                buff_end_time = 0

            if not math_question_active and current_time - last_question_time > math_question_interval:
                question_text, correct_answer = gen_math_question(math_stage)
                player_input = ""
                math_question_active = True
                math_start_time = current_time
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                if current_time - last_shot_time > current_fire_rate:
                    last_shot_time = current_time
                    fire_columns = [player_column]
                    if current_time < multishot_end_time:
                        fire_columns = [player_column - 1, player_column, player_column + 1]
                    for fc in fire_columns:
                        if 0 <= fc < grid_columns:
                            bullet = pygame.Rect(0, 0, bullet_width, bullet_height)
                            bullet.centerx = col_x(fc)
                            bullet.bottom = player_rect.top
                            bullets.append(bullet)
            
            if not is_boss_wave(wave):
                if enemies_spawned_this_wave < wave_enemy_count(wave) and \
                        current_time - enemy_spawn_timer > wave_spawn_rate(wave):
                    enemies.append(create_enemy(wave))
                    enemies_spawned_this_wave += 1
                    enemy_spawn_timer = current_time

            for bullet in bullets[:]:
                bullet.y -= bullet_speed
                if bullet.bottom < 0:
                    bullets.remove(bullet)

            for enemy in enemies[:]:
                enemy["y"] += enemy["speed"]
                enemy["rect"].size = (enemy_size, enemy_size)
                enemy["rect"].centerx = enemy["x"]
                enemy["rect"].y = int(enemy["y"])
 
                removed = False
 
                if current_time >= invulnerability_until and enemy["rect"].colliderect(player_rect):
                    kill_score += 5
                    enemies.remove(enemy)
                    removed = True
                    if shield_active:
                        shield_active = False
                        invulnerability_until = current_time + invulnerability_duration
                    else:
                        lives -= 1
                        invulnerability_until = current_time + invulnerability_duration
                        if lives <= 0:
                            state = "game_over"
                            game_over_reason = "You ran out of lives!"

                if not removed:
                    for bullet in bullets[:]:
                        if enemy["rect"].colliderect(bullet):
                            bullets.remove(bullet)
                            enemies.remove(enemy)
                            kill_score += 5
                            removed = True
                            break

                if not removed and enemy["rect"].top > screen_height:
                    enemies.remove(enemy)
                    if shield_active:
                        shield_active = False
                    else:
                        escapes += 1
                        if escapes >= max_escapes:
                            state = "game_over"
                            game_over_reason = "Too many enemies got past you!"

            if boss is not None:
                boss["y"] += boss_descend_speed
                boss["x"] += boss_side_speed * boss["dir"]
                half = boss_size / 2
                if boss["x"] - half < 0:
                    boss["x"] = half
                    boss["dir"] = 1
                elif boss["x"] + half > screen_width:
                    boss["x"] = screen_width - half
                    boss["dir"] = -1
 
                boss["rect"].size = (boss_size, boss_size)
                boss["rect"].centerx = int(boss["x"])
                boss["rect"].y = int(boss["y"])
 
                if current_time >= invulnerability_until and boss["rect"].colliderect(player_rect):
                    if shield_active:
                        shield_active = False
                        invulnerability_until = current_time + invulnerability_duration
                    else:
                        lives -= 1
                        invulnerability_until = current_time + invulnerability_duration
                        if lives <= 0:
                            state = "game_over"
                            game_over_reason = "The boss beat you!"

                if boss is not None and boss["rect"].top > screen_height:
                    state = "game_over"
                    game_over_reason = "The boss got past you!"
 
                if boss is not None:
                    for bullet in bullets[:]:
                        if boss["rect"].colliderect(bullet):
                            bullets.remove(bullet)
                            boss["hp"] -= 1
                            kill_score += 2
                            if boss["hp"] <= 0:
                                kill_score += 100
                                boss = None
                                math_stage = min(3, math_stage + 1)
                                break
            if state == "playing":
                if not is_boss_wave(wave):
                    if enemies_spawned_this_wave >= wave_enemy_count(wave) and not enemies:
                        kill_score += 20 * wave
                        wave += 1
                        state = "wave_intro"
                        wave_intro_start = current_time
                else:
                    if boss_spawned and boss is None:
                        if wave >= wave_count:
                            state = "win"
                        else:
                            wave += 1
                            state = "wave_intro"
                            wave_intro_start = current_time

            time_alive = (current_time - start_time) // 1000
            total_score = time_alive + kill_score

        screen.fill((20, 25, 40))
 
        if state in ("playing", "wave_intro"):
            draw_grid(screen)
 
            draw_player = True
            if current_time < invulnerability_until:
                draw_player = (current_time // 100) % 2 == 0
            if draw_player:
                colour = CYAN if shield_active else (100, 200, 255)
                pygame.draw.rect(screen, colour, player_rect)
            for bullet in bullets:
                pygame.draw.rect(screen, YELLOW, bullet)
            for enemy in enemies:
                pygame.draw.rect(screen, RED, enemy["rect"])
            if boss is not None:
                pygame.draw.rect(screen, GOLD, boss["rect"])
                bar_width = boss_size
                bar_x = boss["rect"].centerx - bar_width // 2
                bar_y = boss["rect"].top - 16
                pygame.draw.rect(screen, DARK, (bar_x, bar_y, bar_width, 10))
                fill_w = int(bar_width * max(0, boss["hp"]) / boss["max_hp"])
                pygame.draw.rect(screen, RED, (bar_x, bar_y, fill_w, 10))

            stats = {"total_score": total_score, "wave": wave, "lives": lives, "escapes": escapes, "fire_status": fire_status, "fire_status_colour": fire_status_colour, "shield_active": shield_active, "multishot_end_time": multishot_end_time, "current_time": current_time}
            draw_stats_panel(screen, stats)

            if math_question_active:
                panel_rect = pygame.Rect(screen_center_x - 200, 50, 400, 150)
                pygame.draw.rect(screen, (30, 30, 50), panel_rect)
                pygame.draw.rect(screen, WHITE, panel_rect, 3)
 
                q_surf = font.render(f"{question_text} = ?", True, WHITE)
                q_rect = q_surf.get_rect(center=(screen_center_x, 90))
                screen.blit(q_surf, q_rect)
 
                ans_surf = math_font.render(player_input, True, YELLOW)
                ans_rect = ans_surf.get_rect(center=(screen_center_x, 150))
                screen.blit(ans_surf, ans_rect)
 
                time_left = math_time_limit - (current_time - math_start_time)
                bar_width = int(max(0, time_left) / math_time_limit * 380)
                pygame.draw.rect(screen, RED, (screen_center_x - 190, 180, bar_width, 10))
 
            if current_time < power_message_until:
                rsurf = powerup_font.render(current_powerup_message, True, current_powerup_colour)
                rrect = rsurf.get_rect(center=(screen_center_x, 230))
                screen.blit(rsurf, rrect)

            if state == "wave_intro":
                overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 140))
                screen.blit(overlay, (0, 0))
                label = "BOSS WAVE" if is_boss_wave(wave) else f"WAVE {wave}"
                wsurf = wave_font.render(label, True, GOLD if is_boss_wave(wave) else WHITE)
                wrect = wsurf.get_rect(center=(screen_center_x, screen_center_y - 40))
                screen.blit(wsurf, wrect)
                sub = ui_font.render("Wave Starting", True, LIGHT)
                srect = sub.get_rect(center=(screen_center_x, screen_center_y + 40))
                screen.blit(sub, srect)
        
        elif state == "game_over":
            game_over_text = title_font.render("GAME OVER", True, RED)
            game_over_rect = game_over_text.get_rect(center=(screen_center_x, screen_center_y - 200))
            screen.blit(game_over_text, game_over_rect)
 
            reason_surf = ui_font.render(game_over_reason, True, LIGHT)
            reason_rect = reason_surf.get_rect(center=(screen_center_x, screen_center_y - 100))
            screen.blit(reason_surf, reason_rect)
 
            final_score_text = font.render(f"Final Score: {total_score}", True, WHITE)
            final_score_rect = final_score_text.get_rect(center=(screen_center_x, screen_center_y - 40))
            screen.blit(final_score_text, final_score_rect)
 
            wave_reached_text = font.render(f"Wave reached: {wave}", True, WHITE)
            wave_reached_rect = wave_reached_text.get_rect(center=(screen_center_x, screen_center_y + 20))
            screen.blit(wave_reached_text, wave_reached_rect)

            if not score_saved:
                name_prompt = ui_font.render("Type your name and press ENTER to save your score:", True, LIGHT)
                name_prompt_rect = name_prompt.get_rect(center=(screen_center_x, screen_center_y + 90))
                screen.blit(name_prompt, name_prompt_rect)
                name_surf = font.render(name_input + "_", True, YELLOW)
                name_rect = name_surf.get_rect(center=(screen_center_x, screen_center_y + 140))
                screen.blit(name_surf, name_rect)
            else:
                saved_text = ui_font.render("Score saved to the leaderboard!", True, GREEN)
                saved_rect = saved_text.get_rect(center=(screen_center_x, screen_center_y + 110))
                screen.blit(saved_text, saved_rect)
 
            esc_text = ui_font.render("Press esc to return to the Main Menu", True, LIGHT)
            esc_rect = esc_text.get_rect(center=(screen_center_x, screen_center_y + 190))
            screen.blit(esc_text, esc_rect)

        elif state == "win":
            win_text = title_font.render("YOU WIN!", True, GOLD)
            win_rect = win_text.get_rect(center=(screen_center_x, screen_center_y - 200))
            screen.blit(win_text, win_rect)
 
            sub_surf = ui_font.render("The boss has been defeated.", True, LIGHT)
            sub_rect = sub_surf.get_rect(center=(screen_center_x, screen_center_y - 100))
            screen.blit(sub_surf, sub_rect)
 
            final_score_text = font.render(f"Final Score: {total_score}", True, WHITE)
            final_score_rect = final_score_text.get_rect(center=(screen_center_x, screen_center_y - 40))
            screen.blit(final_score_text, final_score_rect)

            if not score_saved:
                name_prompt = ui_font.render("Type your name and press ENTER to save your score:", True, LIGHT)
                name_prompt_rect = name_prompt.get_rect(center=(screen_center_x, screen_center_y + 30))
                screen.blit(name_prompt, name_prompt_rect)
                name_surf = font.render(name_input + "_", True, YELLOW)
                name_rect = name_surf.get_rect(center=(screen_center_x, screen_center_y + 80))
                screen.blit(name_surf, name_rect)
            else:
                saved_text = ui_font.render("Score saved to the leaderboard!", True, GREEN)
                saved_rect = saved_text.get_rect(center=(screen_center_x, screen_center_y + 50))
                screen.blit(saved_text, saved_rect)
 
            esc_text = ui_font.render("Press esc to return to the Main Menu", True, LIGHT)
            esc_rect = esc_text.get_rect(center=(screen_center_x, screen_center_y + 130))
            screen.blit(esc_text, esc_rect)

        pygame.display.update()
        clock.tick(60)

def start_menu():
    play_button = play_img.get_rect()
    quit_button = quit_img.get_rect()
 
    play_button.center = (screen_center_x - 365, screen_center_y - (menubutton_size // 2) - 20)
    quit_button.center = (screen_center_x + 365, screen_center_y - (menubutton_size // 2) - 20)

    leaderboard_button = pygame.Rect(0, 0, 320, 60)
    leaderboard_button.center = (screen_center_x, screen_center_y + 220)

    menu_state = "menu"
 
    while True:
        if menu_state == "menu":
            screen.blit(menu_background, (0, 0))
            screen.blit(play_img, play_button.topleft)
            screen.blit(quit_img, quit_button.topleft)
            screen.blit(title_surface, title_rect)

            pygame.draw.rect(screen, (30, 30, 50), leaderboard_button)
            pygame.draw.rect(screen, WHITE, leaderboard_button, 3)
            lb_label = ui_font.render("LEADERBOARD", True, WHITE)
            lb_label_rect = lb_label.get_rect(center=leaderboard_button.center)
            screen.blit(lb_label, lb_label_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
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
                        if leaderboard_button.collidepoint(mouse_x, mouse_y):
                            menu_state = "leaderboard"
 
            pygame.display.update()

        elif menu_state == "leaderboard":
            screen.fill((20, 25, 40))
            lb_title = title_font.render("LEADERBOARD", True, GOLD)
            lb_title_rect = lb_title.get_rect(center=(screen_center_x, 180))
            screen.blit(lb_title, lb_title_rect)

            entries = load_leaderboard()
            start_y = 340
            if not entries:
                empty_text = ui_font.render("No scores yet - go set one!", True, LIGHT)
                empty_rect = empty_text.get_rect(center=(screen_center_x, start_y))
                screen.blit(empty_text, empty_rect)
            else:
                for i, entry in enumerate(entries):
                    entry_name = entry[0]
                    entry_score = entry[1]
                    line_text = font.render(f"{i + 1}. {entry_name} - {entry_score}", True, WHITE)
                    line_rect = line_text.get_rect(center=(screen_center_x, start_y + i * 50))
                    screen.blit(line_text, line_rect)

            esc_text = ui_font.render("Press esc to return to the Main Menu", True, LIGHT)
            esc_rect = esc_text.get_rect(center=(screen_center_x, screen_height - 80))
            screen.blit(esc_text, esc_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu_state = "menu"
 
            pygame.display.update()
 
 
if __name__ == "__main__":
    start_menu()