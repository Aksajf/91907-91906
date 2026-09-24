import pygame
import sys
import random

pygame.init()

#fullscreen so it works on any monitor size, grid math below is all based off this
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Main Menu")
screen_width = screen.get_width()
screen_height = screen.get_height()
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


menubutton_size = (screen_width * 0.09)

title_font = pygame.font.Font("assets/Conflict3040-WpnRV.ttf", 160)
font = pygame.font.SysFont("Corbel", 40)
ui_font = pygame.font.SysFont("Corbel", 30)
math_font = pygame.font.SysFont("Corbel", 60, bold=True)
small_font = pygame.font.SysFont("Corbel", 24)
wave_font = pygame.font.SysFont("Corbel", 90, bold=True)
powerup_font = pygame.font.SysFont("Corbel", 44, bold=True)

#backup surface incase the bg image is missing so it doesnt just crash
try:
    menu_background = pygame.image.load("assets/menu_bg.png")
    menu_background = pygame.transform.scale(menu_background, (screen_width, screen_height))
except pygame.error:
    menu_background = pygame.Surface((screen_width, screen_height))
    menu_background.fill((52,78,91))

#same idea, green squares as a fallback if the button images dont load
try:
    play_img = pygame.image.load("assets/menu_buttons/large_buttons/colored_large_buttons/playcol_button.png").convert_alpha()
    play_img = pygame.transform.scale(play_img, (menubutton_size, menubutton_size))
    play_mask = pygame.mask.from_surface(play_img)
    quit_img = pygame.image.load("assets/menu_buttons/large_buttons/colored_large_buttons/quitcol_button.png").convert_alpha()
    quit_img = pygame.transform.scale(quit_img, (menubutton_size, menubutton_size))
    quit_mask = pygame.mask.from_surface(quit_img)
except pygame.error:
    play_img = pygame.Surface((menubutton_size, menubutton_size))
    play_img.fill((0, 255, 0))
    quit_img = pygame.Surface((menubutton_size, menubutton_size))
    quit_img.fill((0, 255, 0))
    play_mask = pygame.mask.from_surface(play_img)
    quit_mask = pygame.mask.from_surface(quit_img)

title_surface = title_font.render("MATHALORIAN", True, (250, 230, 214))
title_rect = title_surface.get_rect(center=(screen_center_x, screen_center_y - 450))

#everything moves on a grid of cells so enemies/player line up in columns, min 3 so it doesnt break on tiny screens
CELL_SIZE = 90
grid_columns = max(3, screen_width // CELL_SIZE)
grid_rows = max(3, screen_height // CELL_SIZE)
player_row_minimum = max(0, grid_rows - 4)
player_row_maximum = grid_rows - 1
player_size = CELL_SIZE - 20
enemy_size = CELL_SIZE-20
boss_size = CELL_SIZE*2-10
BULLET_WIDTH = 10
BULLET_HEIGHT = 20
BULLET_SPEED = 16

WAVE_COUNT = 9
STARTING_LIVES = 3
MAX_LIVES = 5
MAX_ESCAPES = 3
INVULNERABILITY_DURATION = 600
WAVE_INTRO_DURATION = 2000

BASE_FIRE_RATE = 400
FAST_FIRE_RATE = 150
SLOW_FIRE_RATE = 900
MULTISHOT_DURATION = 6000

BOSS_DESCEND_SPEED = 0.5
BOSS_SIDE_SPEED = 3.0
BOSS_STARTING_HP = 20

#every reward you can get from answering a math question right, apply_powerup uses these
POWERUP_TYPES = ["fast_fire", "shield", "multishot", "oneup", "nuke"]
POWERUP_MESSAGES = {"fast_fire": "Reward: Attack Speed Up!", "shield": "Reward: Shield!", "multishot": "Reward: MultiShot!", "oneup": "Reward: Extra Life!", "nuke": "Reward: Nuke!",}

POWER_COLOURS = {"fast_fire": GREEN, "shield": CYAN, "multishot": PURPLE, "oneup": RED, "nuke": ORANGE}
POWERUP_MESSAGES_DURATION = 2500

LEADERBOARD_FILE = "leaderboard.txt"

#enemy and boss objects, was using dicts before but classes are cleaner and this is what my assessment wants anyway


class Enemy:
    def __init__(self, wave):
        column = random.randint(0, grid_columns - 1)
        self.x = col_x(column)
        self.y = float(-enemy_size)
        self.speed = wave_enemy_speed(wave)
        self.rect = pygame.Rect(0, 0, enemy_size, enemy_size)


class Boss:
    def __init__(self):
        self.x = float(col_x(grid_columns // 2))
        self.y = float(-boss_size)
        self.hp = BOSS_STARTING_HP
        self.max_hp = BOSS_STARTING_HP
        self.dir = 1
        self.rect = pygame.Rect(0, 0, boss_size, boss_size)

#turns a column/row number into actual pixel coords so everything lines up on the grid


def col_x(col):
    return col*CELL_SIZE+CELL_SIZE//2


def row_y(row):
    return row* CELL_SIZE + CELL_SIZE//2


def is_boss_wave(wave):
    #a boss shows up every 3rd wave so wave 3, 6 and 9 out of 9 total
    return wave % 3 == 0

#reads the txt file and gives back top 10 highest scores, just an empty list if the file isnt there yet


def load_leaderboard():
    entries = []
    try:
        lb_file = open(LEADERBOARD_FILE, "r")
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

#adds the new score in, re sorts, then overwrites the whole file with just the top 10


def save_leaderboard_entry(name, score):
    entries = load_leaderboard()
    entries.append((name, score))
    entries.sort(key=lambda e: e[1], reverse=True)
    entries = entries[:10]
    lb_file = open(LEADERBOARD_FILE, "w")
    for entry in entries:
        lb_file.write(entry[0] + "," + str(entry[1]) + "\n")
    lb_file.close()
    return entries

#difficulty ramps up with stage number, stage goes up every time a boss dies


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

#these 3 are what makes each wave harder than the last, more enemies, faster, spawning quicker


def wave_enemy_count(wave):
    return 4 + (wave - 1) * 1


def wave_enemy_speed(wave):
    return 2.5 + (wave - 1) * 0.2


def wave_spawn_rate(wave):
    return max(500, 1100 - (wave - 1) * 40)

#just wraps the classes now, kept the function names so i didnt have to change every call site


def create_enemy(wave):
    return Enemy(wave)


def create_boss():
    return Boss()

#called when you answer a math question right, picks which reward to actually give you


#takes a single chosen powerup name and applies its effect to the passed in state dict
def apply_powerup(powerup_type, current_time, game_vars):
    if powerup_type == "fast_fire":
        game_vars["current_fire_rate"] = FAST_FIRE_RATE
        game_vars["buff_end_time"] = current_time + 5000
        game_vars["fire_status"] = "Attack Speed Up!"
        game_vars["fire_status_colour"] = GREEN

    elif powerup_type == "shield":
        game_vars["shield_active"] = True

    elif powerup_type == "multishot":
        game_vars["multishot_end_time"] = max(game_vars["multishot_end_time"], current_time) + MULTISHOT_DURATION

    elif powerup_type == "oneup":
        game_vars["lives"] = min(MAX_LIVES, game_vars["lives"] + 1)

    elif powerup_type == "nuke":
        #wipes every enemy on screen and chips the boss, looping over a copy so removing doesnt break the loop
        for enemy in game_vars["enemies"][:]:
            game_vars["enemies"].remove(enemy)
        if game_vars["boss"] is not None:
            game_vars["boss"].hp -= 8
            if game_vars["boss"].hp <= 0:
                game_vars["boss"] = None

    return game_vars

#background grid lines, just cosmetic


def draw_grid(surface):
    for gx in range(grid_columns + 1):
        x = gx * CELL_SIZE
        pygame.draw.line(surface, (35, 45, 65), (x, 0), (x, screen_height), 1)
    for gy in range(grid_rows + 1):
        y = gy * CELL_SIZE
        pygame.draw.line(surface, (35, 45, 65), (0, y), (screen_width, y), 1)

#top left hud, score/wave/lives/escapes/attack speed and any active effects


def draw_stats_panel(surface, stats):
    panel_x, panel_y = 20, 20
    lives_text = ("Lives: " + "Heart " * stats["lives"]).strip() if stats["lives"] > 0 else "Lives: 0"
    lines = [(f"Score: {stats['total_score']}", WHITE), (f"Wave: {stats['wave'] if not is_boss_wave(stats['wave']) else 'boss'} / {WAVE_COUNT}", WHITE),(f"Lives: {stats['lives']}", RED if stats["lives"] <= 1 else WHITE), (f"Escapes: {stats['escapes']} / {MAX_ESCAPES}", ORANGE if stats["escapes"] > 0 else WHITE),
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


#the main game loop, this is basically the whole game including input, movement, collisions, and drawing
def game():
    clock = pygame.time.Clock()

    #player starts bottom middle of the grid
    player_column = grid_columns //2
    player_row = player_row_maximum
    player_width = player_size
    player_height = player_size
    bullets = []
    enemies = []
    boss = None
    start_time = pygame.time.get_ticks()
    math_score = 0

    #normal fire rate until a powerup changes it
    current_fire_rate = BASE_FIRE_RATE
    last_shot_time = 0
    buff_end_time = 0
    fire_status = "Normal"
    fire_status_colour = WHITE

    current_powerup_message = ""
    current_powerup_colour = WHITE
    power_message_until = 0
    lives = STARTING_LIVES
    escapes = 0
    invulnerability_until = 0
    shield_active = False
    multishot_end_time = 0

    #wave 1, easiest math stage, nothing spawned yet
    wave = 1
    math_stage = 1
    enemies_spawned_this_wave = 0
    enemy_spawn_timer = 0
    boss_spawned = False

    #state controls what screen/mode we're in, either wave_intro, playing, game_over or win
    state = "wave_intro"
    wave_intro_start = pygame.time.get_ticks()
    total_score = 0
    game_over_reason = ""

    name_input = ""
    score_saved = False

    #tracks the current on screen math question, if any
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
                #typing your name in and saving the score once the run is over
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
                    #wasd or arrow keys move the player one grid cell at a time
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        player_column = max(0, player_column - 1)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        player_column = min(grid_columns - 1, player_column + 1)
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        player_row = max(player_row_minimum, player_row - 1)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        player_row = min(player_row_maximum, player_row + 1)

                    #enter submits your typed answer, right answer = random powerup, wrong = fire rate debuff
                    if math_question_active:
                        if event.key == pygame.K_RETURN:
                            if player_input == correct_answer:
                                math_score += 100
                                #bundling everything apply_powerup might need to change into one dict since it cant touch these locals directly
                                chosen_powerup = random.choice(POWERUP_TYPES)
                                game_vars = {"current_fire_rate": current_fire_rate, "buff_end_time": buff_end_time,"fire_status": fire_status, "fire_status_colour": fire_status_colour, "shield_active": shield_active, "multishot_end_time": multishot_end_time, "lives": lives, "enemies": enemies, "boss": boss}

                                game_vars = apply_powerup(chosen_powerup, current_time, game_vars)
                                current_fire_rate = game_vars["current_fire_rate"]
                                buff_end_time = game_vars["buff_end_time"]
                                fire_status = game_vars["fire_status"]
                                fire_status_colour = game_vars["fire_status_colour"]
                                shield_active = game_vars["shield_active"]
                                multishot_end_time = game_vars["multishot_end_time"]
                                lives = game_vars["lives"]
                                boss = game_vars["boss"]

                                current_powerup_message = POWERUP_MESSAGES[chosen_powerup]
                                current_powerup_colour = POWER_COLOURS[chosen_powerup]
                                power_message_until = current_time + POWERUP_MESSAGES_DURATION
                            else:
                                #wrong answer just slows your fire rate down
                                current_fire_rate = SLOW_FIRE_RATE
                                fire_status = "Attack Speed Down!"
                                fire_status_colour = RED
                                buff_end_time = current_time + 5000
                            math_question_active = False
                        elif event.key == pygame.K_BACKSPACE:
                            player_input = player_input[:-1]
                        #only lets numbers in, minus sign only allowed as the first character
                        elif event.unicode.isnumeric() or (event.unicode == "-" and len(player_input) == 0):
                            player_input += event.unicode

        player_rect = pygame.Rect(0, 0, player_width, player_height)
        player_rect.center = (col_x(player_column), row_y(player_row))

        #ran out of time on the question, counts the same as a wrong answer
        if math_question_active and current_time - math_start_time > math_time_limit:
            current_fire_rate = SLOW_FIRE_RATE
            fire_status = "Attack Speed Down!"
            fire_status_colour = RED
            buff_end_time = current_time + 5000
            math_question_active = False
            last_question_time = current_time

        #banner timer runs out, drop into playing and spawn the boss if its a boss wave
        if state == "wave_intro":
            if current_time - wave_intro_start > WAVE_INTRO_DURATION:
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
            #fire rate buff/debuff wears off after its timer
            if current_time > buff_end_time and buff_end_time != 0:
                current_fire_rate = BASE_FIRE_RATE
                fire_status = "Normal"
                fire_status_colour = WHITE
                buff_end_time = 0

            #pops up a new math question every 8 seconds if one isnt already showing
            if not math_question_active and current_time - last_question_time > math_question_interval:
                question_text, correct_answer = gen_math_question(math_stage)
                player_input = ""
                math_question_active = True
                math_start_time = current_time

            #holding space fires, multishot hits 3 columns at once instead of 1
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                if current_time - last_shot_time > current_fire_rate:
                    last_shot_time = current_time
                    fire_columns = [player_column]
                    if current_time < multishot_end_time:
                        fire_columns = [player_column - 1, player_column, player_column + 1]
                    for fc in fire_columns:
                        if 0 <= fc < grid_columns:
                            bullet = pygame.Rect(0, 0, BULLET_WIDTH, BULLET_HEIGHT)
                            bullet.centerx = col_x(fc)
                            bullet.bottom = player_rect.top
                            bullets.append(bullet)

            #normal waves trickle enemies in, boss waves dont spawn regular enemies
            if not is_boss_wave(wave):
                if enemies_spawned_this_wave < wave_enemy_count(wave) and \
                        current_time - enemy_spawn_timer > wave_spawn_rate(wave):
                    enemies.append(create_enemy(wave))
                    enemies_spawned_this_wave += 1
                    enemy_spawn_timer = current_time

            #move bullets up and clear out any that went off the top of the screen
            for bullet in bullets[:]:
                bullet.y -= BULLET_SPEED
                if bullet.bottom < 0:
                    bullets.remove(bullet)

            #move every enemy down, then check all 3 ways an enemy can go away either hits a player, gets shot, or escapes off the bottom
            for enemy in enemies[:]:
                enemy.y += enemy.speed
                enemy.rect.size = (enemy_size, enemy_size)
                enemy.rect.centerx = enemy.x
                enemy.rect.y = int(enemy.y)

                removed = False

                #enemy hits the player, shield eats the hit once then turns off, otherwise you lose a life
                if current_time >= invulnerability_until and enemy.rect.colliderect(player_rect):
                    enemies.remove(enemy)
                    removed = True
                    if shield_active:
                        shield_active = False
                        invulnerability_until = current_time + INVULNERABILITY_DURATION
                    else:
                        lives -= 1
                        invulnerability_until = current_time + INVULNERABILITY_DURATION
                        if lives <= 0:
                            state = "game_over"
                            game_over_reason = "You ran out of lives!"

                #got shot by a bullet instead
                if not removed:
                    for bullet in bullets[:]:
                        if enemy.rect.colliderect(bullet):
                            bullets.remove(bullet)
                            enemies.remove(enemy)
                            removed = True
                            break

                #enemy made it past the player, counts as an escape unless shield blocks it
                if not removed and enemy.rect.top > screen_height:
                    enemies.remove(enemy)
                    if shield_active:
                        shield_active = False
                    else:
                        escapes += 1
                        if escapes >= MAX_ESCAPES:
                            state = "game_over"
                            game_over_reason = "Too many enemies got past you!"

            #boss slides side to side while descending, bounces off the screen edges
            if boss is not None:
                boss.y += BOSS_DESCEND_SPEED
                boss.x += BOSS_SIDE_SPEED * boss.dir
                half = boss_size / 2
                if boss.x - half < 0:
                    boss.x = half
                    boss.dir = 1
                elif boss.x + half > screen_width:
                    boss.x = screen_width - half
                    boss.dir = -1

                boss.rect.size = (boss_size, boss_size)
                boss.rect.centerx = int(boss.x)
                boss.rect.y = int(boss.y)

                if current_time >= invulnerability_until and boss.rect.colliderect(player_rect):
                    if shield_active:
                        shield_active = False
                        invulnerability_until = current_time + INVULNERABILITY_DURATION
                    else:
                        lives -= 1
                        invulnerability_until = current_time + INVULNERABILITY_DURATION
                        if lives <= 0:
                            state = "game_over"
                            game_over_reason = "The boss beat you!"

                if boss is not None and boss.rect.top > screen_height:
                    state = "game_over"
                    game_over_reason = "The boss got past you!"

                #chip away boss hp with bullets, killing it bumps the math difficulty up a stage
                if boss is not None:
                    for bullet in bullets[:]:
                        if boss.rect.colliderect(bullet):
                            bullets.remove(bullet)
                            boss.hp -= 1
                            if boss.hp <= 0:
                                boss = None
                                math_stage = min(3, math_stage + 1)
                                break

            #checks if the wave is done, normal waves need every enemy spawned and dead, boss waves just need the boss dead
            if state == "playing":
                if not is_boss_wave(wave):
                    if enemies_spawned_this_wave >= wave_enemy_count(wave) and not enemies:
                        wave += 1
                        state = "wave_intro"
                        wave_intro_start = current_time
                else:
                    if boss_spawned and boss is None:
                        #beat the boss on the last wave = win, otherwise its just onto the next wave
                        if wave >= WAVE_COUNT:
                            state = "win"
                        else:
                            wave += 1
                            state = "wave_intro"
                            wave_intro_start = current_time

            #score is strictly based on answering math questions correctly
            total_score = math_score

        #everything below here just draws the current state to the screen every frame
        screen.fill((20, 25, 40))

        if state in ("playing", "wave_intro"):
            draw_grid(screen)

            #flicker the player sprite while invulnerable so you can tell youre still safe
            draw_player = True
            if current_time < invulnerability_until:
                draw_player = (current_time // 100) % 2 == 0
            if draw_player:
                colour = CYAN if shield_active else (100, 200, 255)
                pygame.draw.rect(screen, colour, player_rect)
            for bullet in bullets:
                pygame.draw.rect(screen, YELLOW, bullet)
            for enemy in enemies:
                pygame.draw.rect(screen, RED, enemy.rect)
            if boss is not None:
                pygame.draw.rect(screen, GOLD, boss.rect)
                bar_width = boss_size
                bar_x = boss.rect.centerx - bar_width // 2
                bar_y = boss.rect.top - 16
                pygame.draw.rect(screen, DARK, (bar_x, bar_y, bar_width, 10))
                fill_w = int(bar_width * max(0, boss.hp) / boss.max_hp)
                pygame.draw.rect(screen, RED, (bar_x, bar_y, fill_w, 10))

            stats = {"total_score": total_score, "wave": wave, "lives": lives, "escapes": escapes, "fire_status": fire_status, "fire_status_colour": fire_status_colour, "shield_active": shield_active, "multishot_end_time": multishot_end_time, "current_time": current_time}
            draw_stats_panel(screen, stats)

            #the math question box with the countdown bar underneath
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

            #dark overlay + big wave banner while the intro is showing
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

        #death screen, shows the reason you died plus final score and a name entry box
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

        #same idea as game over but for beating the final boss
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

#title screen, loops between the menu itself and the leaderboard view depending on menu_state


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
                        #using the mask instead of just the rect so clicking the transparent corners of the button image doesnt count
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

        #leaderboard view, just lists the top scores and esc takes you back
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


#calls eveyrthing
if __name__ == "__main__":
    start_menu()
