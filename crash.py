import pygame
import random
import sys
import time
import os

1. تشغيل محرك الألعاب والتشغيل الصوتي

pygame.init()
pygame.mixer.init()

2. قراءة مقاس شاشة التليفون لملء الشاشة بالكامل

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("متاهة محمد حسني الاحترافية")

الألوان

BLACK = (15, 15, 15)
YELLOW = (241, 196, 15)
PLAYER_COLOR = (46, 204, 113)
MONSTER_COLOR = (231, 76, 60)
ENRAGED_MONSTER_COLOR = (139, 0, 0)
EXIT_COLOR = (52, 152, 219)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED_BTN = (192, 57, 43)
DARK_GRAY = (30, 30, 30)
LIGHT_GRAY = (100, 100, 100)

ألوان الهدايا والموارد

HEART_ITEM_COLOR = (255, 105, 180)
SPEED_ITEM_COLOR = (255, 0, 128)
FREEZE_ITEM_COLOR = (0, 255, 255)
SWORD_ITEM_COLOR = (230, 126, 34)

مقاسات العناصر الثابتة بناءً على الشاشة

player_size = int(WIDTH * 0.08)
monster_size = int(WIDTH * 0.09)
exit_size_w = int(WIDTH * 0.15)
exit_size_h = int(HEIGHT * 0.02)
item_size = int(WIDTH * 0.07)
btn_w = int(WIDTH * 0.22)
btn_h = int(HEIGHT * 0.08)
attack_btn_w = int(WIDTH * 0.35)

سرعات اللعبة الأساسية

player_base_speed = int(WIDTH * 0.035)
player_speed = player_base_speed
monster_base_speed = WIDTH * 0.007

font = pygame.font.SysFont("Arial", int(WIDTH * 0.05))
small_font = pygame.font.SysFont("Arial", int(WIDTH * 0.04))
clock = pygame.time.Clock()

متغيرات الصوت والإعدادات

music_on = True
game_paused = False

متغيرات الهدايا

item_pos = [0, 0]
item_type = None
item_active = False

مؤقتات التأثيرات ومخزن السلاح

speed_boost_end_time = 0
freeze_monster_end_time = 0
has_sword = False
# تشغيل المزيكا
sound_file = None

if os.path.exists("music.mp3"):
    sound_file = "music.mp3"
elif os.path.exists("music"):
    sound_file = "music"

if sound_file:
    try:
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print("الملف موجود بس فيه مشكلة في صيغته:", e)
else:
    print("تنبيه: اللعبة مش لاقية ملف المزيكا!")


best_score = 0

def draw_safe_heart(surface, color, x, y, size):
"""رسم شكل قلب خفيف ومستقر جداً على معالجات الموبايل"""
r = size // 2
pygame.draw.circle(surface, color, (x + r//2, y + r//2), r//2)
pygame.draw.circle(surface, color, (x + size - r//2, y + r//2), r//2)
pygame.draw.rect(surface, color, (x, y + r//2, size, size - r//2))

def spawn_random_item():
global item_pos, item_type, item_active
if random.random() < 0.7:
item_type = random.choice(["HEART", "SPEED", "FREEZE", "SWORD"])
item_pos = [random.randint(0, WIDTH - item_size), random.randint(int(HEIGHT * 0.25), HEIGHT - (btn_h * 4))]
item_active = True
else:
item_active = False

def reset_positions():
global player_pos, monster_pos, exit_pos
player_pos = [WIDTH // 2 - (player_size // 2), HEIGHT - (btn_h * 2) - 150]
exit_pos = [random.randint(0, WIDTH - exit_size_w), random.randint(int(HEIGHT * 0.25), HEIGHT - (btn_h * 4))]

# حل مشكلة الكراش بوضع إحداثيات بديلة سريعة للوحش  
mx = random.randint(0, WIDTH - monster_size)  
my = random.randint(int(HEIGHT * 0.25), HEIGHT - (btn_h * 4))  
monster_pos = [mx, my]  
spawn_random_item()

تشغيل اللعبة

reset_positions()
score = 0
running_lives = 3
game_state = "PLAYING"

running = True
while running:
current_time = pygame.time.get_ticks() / 1000.0
clock.tick(30)
screen.fill(BLACK)

# مقاسات شاشة الإعدادات  
settings_btn_x = WIDTH - int(WIDTH * 0.15)  
settings_btn_y = 20  
settings_btn_w = int(WIDTH * 0.12)  
settings_btn_h = int(HEIGHT * 0.05)  
  
panel_w = int(WIDTH * 0.7)  
panel_h = int(HEIGHT * 0.3)  
panel_x = (WIDTH - panel_w) // 2  
panel_y = (HEIGHT - panel_h) // 2  
  
x_btn_w = int(panel_w * 0.15)  
x_btn_h = int(panel_h * 0.18)  
x_btn_x = panel_x + panel_w - x_btn_w - 15  
x_btn_y = panel_y + 15  
  
sound_btn_w = int(panel_w * 0.6)  
sound_btn_h = int(panel_h * 0.22)  
sound_btn_x = panel_x + (panel_w - sound_btn_w) // 2  
sound_btn_y = panel_y + int(panel_h * 0.5)  

attack_btn_x = (WIDTH - attack_btn_w) // 2  
attack_btn_y = HEIGHT - (btn_h * 3) - 30  

if current_time < speed_boost_end_time:  
    player_speed = player_base_speed * 1.6   
else:  
    player_speed = player_base_speed  

if game_state == "PLAYING":  
    is_enraged = (score > 0) and (score % 5 == 0)  
      
    if is_enraged:  
        current_monster_speed = (monster_base_speed + (score * 0.4)) * 1.7   
        current_monster_color = ENRAGED_MONSTER_COLOR  
    else:  
        current_monster_speed = monster_base_speed + (score * 0.4)  
        current_monster_color = MONSTER_COLOR  
      
    if score > best_score:  
        best_score = score  
          
    dev_text = font.render("Developer: Mohamed Hosny", True, YELLOW)  
    score_text = font.render(f"Score: {score}", True, WHITE)  
    best_score_text = font.render(f"Best: {best_score}", True, YELLOW)  
      
    lives_label = font.render("Hearts: ", True, MONSTER_COLOR)  
    screen.blit(dev_text, (20, 20))  
    screen.blit(score_text, (20, 20 + int(WIDTH * 0.06)))  
    screen.blit(best_score_text, (20, 20 + int(WIDTH * 0.12)))  
    screen.blit(lives_label, (20, 20 + int(WIDTH * 0.18)))  
      
    # رسم عداد القلوب الآمن  
    for i in range(running_lives):  
        draw_safe_heart(screen, MONSTER_COLOR, 180 + (i * int(WIDTH * 0.06)), 20 + int(WIDTH * 0.19), int(WIDTH * 0.04))  
      
    status_msg = ""  
    if is_enraged:  
        status_msg = f"LEVEL {score}: BOSS WAVE!"  
    elif current_time < speed_boost_end_time:  
        status_msg = "SPEED BOOST ACTIVE!"  
    elif current_time < freeze_monster_end_time:  
        status_msg = "MONSTER FROZEN!"  
      
    if has_sword and status_msg == "":  
        status_msg = "SWORD READY!"  

    status_text = small_font.render(status_msg, True, ENRAGED_MONSTER_COLOR if is_enraged else FREEZE_ITEM_COLOR)  
    screen.blit(status_text, (WIDTH - int(WIDTH * 0.58), 20 + int(WIDTH * 0.12)))  
      
    # زرار الترس مكتوب بشكل عادي وجذاب  
    pygame.draw.rect(screen, GRAY, (settings_btn_x, settings_btn_y, settings_btn_w, settings_btn_h))  
    settings_txt = small_font.render("SET", True, WHITE)  
    screen.blit(settings_txt, (settings_btn_x + int(settings_btn_w*0.15), settings_btn_y + int(settings_btn_h*0.1)))  
      
    pygame.draw.line(screen, GRAY, (0, int(HEIGHT * 0.25)), (WIDTH, int(HEIGHT * 0.25)), 2)  
      
    # رسم العناصر  
    pygame.draw.rect(screen, EXIT_COLOR, (exit_pos[0], exit_pos[1], exit_size_w, exit_size_h))  
    pygame.draw.rect(screen, PLAYER_COLOR, (player_pos[0], player_pos[1], player_size, player_size))  
      
    if has_sword:  
        pygame.draw.rect(screen, SWORD_ITEM_COLOR, (player_pos[0] + int(player_size*0.35), player_pos[1] - 20, int(player_size*0.3), 15))  

    pygame.draw.rect(screen, current_monster_color, (monster_pos[0], monster_pos[1], monster_size, monster_size))  
      
    # رسم الهدايا بأشكال ملونة واضحة ومستقرة ومكتوب جواها رمزها  
    if item_active:  
        if item_type == "HEART":  
            pygame.draw.rect(screen, HEART_ITEM_COLOR, (item_pos[0], item_pos[1], item_size, item_size), 0, 4)  
            item_label = small_font.render("H", True, WHITE)  
        elif item_type == "SPEED":  
            pygame.draw.rect(screen, SPEED_ITEM_COLOR, (item_pos[0], item_pos[1], item_size, item_size), 0, 4)  
            item_label = small_font.render("S", True, WHITE)  
        elif item_type == "FREEZE":  
            pygame.draw.rect(screen, FREEZE_ITEM_COLOR, (item_pos[0], item_pos[1], item_size, item_size), 0, 4)  
            item_label = small_font.render("F", True, BLACK)  
        elif item_type == "SWORD":  
            pygame.draw.rect(screen, SWORD_ITEM_COLOR, (item_pos[0], item_pos[1], item_size, item_size), 0, 4)  
            item_label = small_font.render("W", True, WHITE)  
        screen.blit(item_label, (item_pos[0] + int(item_size*0.25), item_pos[1] + int(item_size*0.1)))  

    # أزرار الحركة اللمسية  
    pygame.draw.rect(screen, (40, 40, 40), (20, HEIGHT - btn_h - 20, btn_w, btn_h))   
    pygame.draw.rect(screen, (40, 40, 40), (WIDTH - btn_w - 20, HEIGHT - btn_h - 20, btn_w, btn_h))   
    pygame.draw.rect(screen, (50, 50, 50), (WIDTH // 2 - (btn_w // 2), HEIGHT - (btn_h * 2) - 40, btn_w, btn_h))   
    pygame.draw.rect(screen, (30, 30, 30), (WIDTH // 2 - (btn_w // 2), HEIGHT - btn_h - 20, btn_w, btn_h))   
      
    screen.blit(font.render("<- L", True, WHITE), (20 + 20, HEIGHT - btn_h))  
    screen.blit(font.render("R ->", True, WHITE), (WIDTH - btn_w, HEIGHT - btn_h))  
    screen.blit(font.render("^ UP", True, WHITE), (WIDTH // 2 - 25, HEIGHT - (btn_h * 2) - 20))  
    screen.blit(font.render("v DN", True, WHITE), (WIDTH // 2 - 25, HEIGHT - btn_h))  

    if has_sword:  
        pygame.draw.rect(screen, SWORD_ITEM_COLOR, (attack_btn_x, attack_btn_y, attack_btn_w, btn_h), 0, 10)  
        attack_txt = font.render("ATTACK", True, WHITE)  
        screen.blit(attack_txt, (attack_btn_x + int(attack_btn_w*0.2), attack_btn_y + int(btn_h*0.15)))  

    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            running = False  
        if event.type == pygame.MOUSEBUTTONDOWN and not game_paused:  
            mx, my = pygame.mouse.get_pos()  
            if settings_btn_x <= mx <= settings_btn_x + settings_btn_w and settings_btn_y <= my <= settings_btn_y + settings_btn_h:  
                game_paused = True  
              
            if has_sword and attack_btn_x <= mx <= attack_btn_x + attack_btn_w and attack_btn_y <= my <= attack_btn_y + btn_h:  
                player_rect = pygame.Rect(player_pos[0] - 50, player_pos[1] - 50, player_size + 100, player_size + 100)  
                monster_rect = pygame.Rect(monster_pos[0], monster_pos[1], monster_size, monster_size)  
                if player_rect.colliderect(monster_rect):  
                    has_sword = False   
                    monster_pos = [random.choice([0, WIDTH - monster_size]), int(HEIGHT * 0.25)]  

    if not game_paused:  
        mouse_pressed = pygame.mouse.get_pressed()  
        if mouse_pressed[0]:   
            mx, my = pygame.mouse.get_pos()  
            if 20 <= mx <= 20 + btn_w and HEIGHT - btn_h - 20 <= my <= HEIGHT - 20:  
                player_pos[0] -= player_speed  
            if WIDTH - btn_w - 20 <= mx <= WIDTH - 20 and HEIGHT - btn_h - 20 <= my <= HEIGHT - 20:  
                player_pos[0] += player_speed  
            if WIDTH // 2 - (btn_w // 2) <= mx <= WIDTH // 2 + (btn_w // 2) and HEIGHT - (btn_h * 2) - 40 <= my <= HEIGHT - btn_h - 40:  
                player_pos[1] -= player_speed  
            if WIDTH // 2 - (btn_w // 2) <= mx <= WIDTH // 2 + (btn_w // 2) and HEIGHT - btn_h - 20 <= my <= HEIGHT - 20:  
                player_pos[1] += player_speed  

        if current_time >= freeze_monster_end_time:  
            if monster_pos[0] < player_pos[0]: monster_pos[0] += current_monster_speed  
            elif monster_pos[0] > player_pos[0]: monster_pos[0] -= current_monster_speed  
            if monster_pos[1] < player_pos[1]: monster_pos[1] += current_monster_speed  
            elif monster_pos[1] > player_pos[1]: monster_pos[1] -= current_monster_speed  

        if player_pos[0] < 0: player_pos[0] = 0  
        if player_pos[0] > WIDTH - player_size: player_pos[0] = WIDTH - player_size  
        if player_pos[1] < int(HEIGHT * 0.25): player_pos[1] = int(HEIGHT * 0.25)  
        if player_pos[1] > HEIGHT - (btn_h * 3) - 130: player_pos[1] = HEIGHT - (btn_h * 3) - 130  

        player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)  
          
        if item_active:  
            item_rect = pygame.Rect(item_pos[0], item_pos[1], item_size, item_size)  
            if player_rect.colliderect(item_rect):  
                item_active = False   
                if item_type == "HEART" and running_lives < 3:  
                    running_lives += 1  
                elif item_type == "SPEED":  
                    speed_boost_end_time = current_time + 5.0   
                elif item_type == "FREEZE":  
                    freeze_monster_end_time = current_time + 4.0   
                elif item_type == "SWORD":  
                    has_sword = True   

        exit_rect = pygame.Rect(exit_pos[0], exit_pos[1], exit_size_w, exit_size_h)  
        if player_rect.colliderect(exit_rect):  
            score += 1  
            reset_positions()  
            time.sleep(0.1)  

        monster_rect = pygame.Rect(monster_pos[0], monster_pos[1], monster_size, monster_size)  
        if player_rect.colliderect(monster_rect):  
            running_lives -= 1  
            has_sword = False   
            if running_lives > 0:  
                reset_positions()  
                time.sleep(0.2)  
            else:  
                game_state = "GAME_OVER"  

    # شاشة الإعدادات  
    if game_paused:  
        pygame.draw.rect(screen, DARK_GRAY, (panel_x, panel_y, panel_w, panel_h), 0, 15)  
        pygame.draw.rect(screen, LIGHT_GRAY, (panel_x, panel_y, panel_w, panel_h), 3, 15)  
          
        title_txt = font.render("Settings Panel", True, YELLOW)  
        screen.blit(title_txt, (panel_x + 25, panel_y + 15))  
          
        pygame.draw.rect(screen, RED_BTN, (x_btn_x, x_btn_y, x_btn_w, x_btn_h), 0, 5)  
        x_txt = small_font.render("X", True, WHITE)  
        screen.blit(x_txt, (x_btn_x + int(x_btn_w*0.3), x_btn_y + int(x_btn_h*0.1)))  
          
        sound_btn_color = PLAYER_COLOR if music_on else LIGHT_GRAY  
        pygame.draw.rect(screen, sound_btn_color, (sound_btn_x, sound_btn_y, sound_btn_w, sound_btn_h), 0, 8)  
          
        status_str = "Music: ON" if music_on else "Music: OFF"  
        sound_txt = small_font.render(status_str, True, WHITE)  
        screen.blit(sound_txt, (sound_btn_x + int(sound_btn_w*0.15), sound_btn_y + int(sound_btn_h*0.2)))  
          
        mouse_up_events = pygame.event.get(pygame.MOUSEBUTTONDOWN)  
        for event in mouse_up_events:  
            mx, my = pygame.mouse.get_pos()  
            if x_btn_x <= mx <= x_btn_x + x_btn_w and x_btn_y <= my <= x_btn_y + x_btn_h:  
                game_paused = False  
            if sound_btn_x <= mx <= sound_btn_x + sound_btn_w and sound_btn_y <= my <= sound_btn_y + sound_btn_h:  
                music_on = not music_on  
                if music_on: pygame.mixer.music.unpause()  
                else: pygame.mixer.music.pause()  

elif game_state == "GAME_OVER":  
    game_paused = False  
    end_font = pygame.font.SysFont("Arial", int(WIDTH * 0.08), "bold")  
    game_over_text = end_font.render("GAME OVER", True, MONSTER_COLOR)  
    final_score_text = font.render(f"Your Score: {score}", True, WHITE)  
    end_best_text = font.render(f"Your Best Score: {best_score}", True, YELLOW)  
    thanks_text = font.render("Thanks for playing Mohamed's Game!", True, YELLOW)  
      
    screen.blit(game_over_text, (WIDTH // 2 - int(WIDTH * 0.25), HEIGHT // 4))  
    screen.blit(final_score_text, (WIDTH // 2 - int(WIDTH * 0.15), HEIGHT // 4 + int(HEIGHT * 0.08)))  
    screen.blit(end_best_text, (WIDTH // 2 - int(WIDTH * 0.18), HEIGHT // 4 + int(HEIGHT * 0.14)))  
    screen.blit(thanks_text, (WIDTH // 2 - int(WIDTH * 0.4), HEIGHT // 4 + int(HEIGHT * 0.22)))  
      
    replay_w, replay_h = int(WIDTH * 0.4), int(HEIGHT * 0.08)  
    replay_x = WIDTH // 2 - (replay_w // 2)  
    replay_y = HEIGHT // 2 + int(HEIGHT * 0.08)  
      
    pygame.draw.rect(screen, RED_BTN, (replay_x, replay_y, replay_w, replay_h))  
    replay_txt = font.render("REPLAY", True, WHITE)  
    screen.blit(replay_txt, (replay_x + int(replay_w * 0.25), replay_y + int(replay_h * 0.25)))  
      
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            running = False  
        if event.type == pygame.MOUSEBUTTONDOWN:  
            mx, my = pygame.mouse.get_pos()  
            if replay_x <= mx <= replay_x + replay_w and replay_y <= my <= replay_y + replay_h:  
                score = 0   
                running_lives = 3   
                has_sword = False  
                speed_boost_end_time = 0  
                freeze_monster_end_time = 0  
                reset_positions()  
                game_state = "PLAYING"  

pygame.display.update()

pygame.quit()
sys.exit()