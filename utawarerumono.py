import pygame
import random

pygame.init()

# 定数設定
WIDTH, HEIGHT = 800, 400
TILE_SIZE = 40
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE

# 画像読み込み
background = pygame.image.load('black.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
warrior_img = pygame.image.load('warrior.png')
warrior_img = pygame.transform.scale(warrior_img, (30, 30))
monster_img = pygame.image.load('robot.png')
monster_img = pygame.transform.scale(monster_img, (30, 30))

# 初期位置
warrior_pos = [10, 5]
monster_pos = [0, 0]

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monster and Warrior Game")

turn = "warrior"  # ターン制御用
game_over = False

while not game_over:
    win.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN and turn == "warrior":
            if event.key == pygame.K_LEFT and warrior_pos[0] > 0:
                warrior_pos[0] -= 1
                turn = "monster"
            elif event.key == pygame.K_RIGHT and warrior_pos[0] < GRID_WIDTH - 1:
                warrior_pos[0] += 1
                turn = "monster"
            elif event.key == pygame.K_UP and warrior_pos[1] > 0:
                warrior_pos[1] -= 1
                turn = "monster"
            elif event.key == pygame.K_DOWN and warrior_pos[1] < GRID_HEIGHT - 1:
                warrior_pos[1] += 1
                turn = "monster"
                
    if turn == "monster":
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)
        for dx, dy in directions:
            new_x = monster_pos[0] + dx
            new_y = monster_pos[1] + dy
            if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and [new_x, new_y] != warrior_pos:
                monster_pos = [new_x, new_y]
                break
        turn = "warrior"
    
    # 描画
    win.blit(warrior_img, (warrior_pos[0] * TILE_SIZE, warrior_pos[1] * TILE_SIZE))
    win.blit(monster_img, (monster_pos[0] * TILE_SIZE, monster_pos[1] * TILE_SIZE))
    pygame.display.flip()

    pygame.time.wait(200)  # 少し待ち時間を設ける

pygame.quit()

