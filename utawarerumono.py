import pygame
import random


pygame.init()

# 定数設定
WIDTH, HEIGHT = 1400, 800
TILE_SIZE = 80
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE

# 画像読み込み
background = pygame.image.load('Kankokukan.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
warrior_img = pygame.image.load('Moubu.png')
warrior_img = pygame.transform.scale(warrior_img, (60, 60))
monster_img = pygame.image.load('Kanmei.png')
monster_img = pygame.transform.scale(monster_img, (60, 60))

# 初期位置とHP
warrior_pos = [11, 7]
warrior_hp = 100
monster_pos = [11, 3]
monster_hp = 60
turn = "warrior"
game_over = False
warrior_moves = 0 #戦士が1ターンに動く回数を追跡

#HPバー表示用
MAX_WARRIOR_HP = 100
MAX_MONSTER_HP = 60

def is_directly_next_to_warrior(monster, warrior):
    return (monster[0] == warrior[0] and abs(monster[1] - warrior[1]) == 1) or \
           (monster[1] == warrior[1] and abs(monster[0] - warrior[0]) == 1)

def is_directly_next_to_monster(monster, warrior):
    return (monster[0] == warrior[0] and abs(monster[1] - warrior[1]) == 1) or \
           (monster[1] == warrior[1] and abs(monster[0] - warrior[0]) == 1)


win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monster and Warrior Game")
font = pygame.font.SysFont('Arial', 24)

#'攻撃'のテキスト
ATTACK_TEXT_X = 10
ATTACK_TEXT_Y = 10
ATTACK_TEXT_W, ATTACK_TEXT_H = 60, 30

# BGMのロードと再生
pygame.mixer.init()
pygame.mixer.music.load('Battle-bgm.mp3')
pygame.mixer.music.play(-1)

while not game_over:
    win.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if (ATTACK_TEXT_X <= mouse_pos[0] <= ATTACK_TEXT_X + ATTACK_TEXT_W and
                    ATTACK_TEXT_Y <= mouse_pos[1] <= ATTACK_TEXT_Y + ATTACK_TEXT_H):
                monster_hp -= random.randint(10, 20)
                warrior_moves += 1
                
                if warrior_moves == 2:
                    turn = "monster"
                    warrior_moves = 0
                    if monster_hp <= 0:
                        game_over = True
#=========================================================================
        if turn == "warrior" and event.type == pygame.KEYDOWN:#プレイヤーには操作が＋αで付いている
            new_x, new_y = warrior_pos[0], warrior_pos[1]

            # 条件が真の場合、"攻撃"という文字を描画します。
            if event.key == pygame.K_LEFT and new_x > 0:
                new_x -= 1
            elif event.key == pygame.K_RIGHT and new_x < GRID_WIDTH - 1:
                new_x += 1
            elif event.key == pygame.K_UP and new_y > 0:
                new_y -= 1
            elif event.key == pygame.K_DOWN and new_y < GRID_HEIGHT - 1:
                new_y += 1

            # ここで新しい位置がモンスターと隣接していないことを確認
            if [new_x, new_y] != monster_pos:
                warrior_pos = [new_x, new_y]
                if warrior_moves < 2:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                        warrior_moves += 1
                if warrior_moves == 2:
                    turn = "monster"
                    warrior_moves = 0

#=================================================================               
   
    if turn == "monster":
        if is_directly_next_to_warrior(monster_pos, warrior_pos):
            damage = random.randint(10, 20)
            warrior_hp -= damage
            turn = "warrior"
            if warrior_hp <= 0:
                game_over = True
        else:
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            random.shuffle(directions)
            for dx, dy in directions:
                new_x = monster_pos[0] + dx
                new_y = monster_pos[1] + dy
                if (0 <= new_x < GRID_WIDTH and 
                    0 <= new_y < GRID_HEIGHT and 
                    [new_x, new_y] != warrior_pos and 
                    not is_directly_next_to_warrior([new_x, new_y], warrior_pos)): 
                    monster_pos = [new_x, new_y]
                    break
            turn = "warrior"


    
    warrior_hp_percentage = warrior_hp / MAX_WARRIOR_HP
    monster_hp_percentage = monster_hp / MAX_MONSTER_HP

    pygame.draw.rect(win, (255, 0, 0), (10, HEIGHT - 40, 200, 20))
    pygame.draw.rect(win, (0, 255, 0), (10, HEIGHT - 40, 200 * warrior_hp_percentage, 20))

    pygame.draw.rect(win, (255, 0, 0), (WIDTH - 210, HEIGHT - 40, 200, 20))
    pygame.draw.rect(win, (0, 255, 0), (WIDTH - 210, HEIGHT - 40, 200 * monster_hp_percentage, 20))



    # 描画
    win.blit(warrior_img, (warrior_pos[0] * TILE_SIZE, warrior_pos[1] * TILE_SIZE))
    win.blit(monster_img, (monster_pos[0] * TILE_SIZE, monster_pos[1] * TILE_SIZE))
    
    warrior_hp_text = font.render(f'Warrior HP: {warrior_hp}', True, (255, 255, 255))
    monster_hp_text = font.render(f'Monster HP: {monster_hp}', True, (255, 255, 255))
    win.blit(warrior_hp_text, (10, 10))
    win.blit(monster_hp_text, (WIDTH - 200, 10))

    if game_over:
        game_over_text = font.render('Game Over', True, (255, 0, 0))
        win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))

    if turn == "warrior" and warrior_moves < 2 and is_directly_next_to_monster(monster_pos, warrior_pos):
        attack_font = pygame.font.SysFont(None, 55)
        attack_text = attack_font.render('攻撃', True, (255,0,0))
        win.blit(attack_text, (ATTACK_TEXT_X, ATTACK_TEXT_Y))

    pygame.display.flip()

    pygame.time.wait(200)  # 少し待ち時間を設ける

    pygame.mixer.music.stop()

pygame.quit()