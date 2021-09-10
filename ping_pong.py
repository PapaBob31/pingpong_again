#  ping pong
import pygame
import random
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("ping pong")
win = pygame.display.set_mode((800, 500))
run = True
x = 750
y = 200
x2 = 50
y2 = 200
cx = 50
cy = 200
width = 15
height = 120
ball_vel = 10
vel = 10
vel_y = 0
vel_x = 0
ball_x = 740
ball_y = 300
radius = 10
left_score = 0
right_score = 0
game_pause = False
game_start = False
game_menu = True
serve = False
multiplayer = False
against_tw = False
vs_computer = False
v = True

while run:
    pygame.time.delay(15)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if game_menu:
            win.fill((0, 0, 0))
            font = pygame.font.SysFont("algerian", 100)
            text = pygame.font.SysFont("verdana", 15)
            win.blit(font.render("PING PONG", True, (255, 255, 255)), (150, 50))
            win.blit(text.render("VS Computer", True, (255, 255, 255)), (160, 310))
            win.blit(text.render("Against the wall", True, (255, 255, 255)), (360, 310))
            win.blit(text.render("MULTIPLAYER", True, (255, 255, 255)), (560, 310))
            pygame.draw.rect(win, (255, 255, 255), (150, 300, 150, 50), 2)
            pygame.draw.rect(win, (255, 255, 255), (350, 300, 150, 50), 2)
            pygame.draw.rect(win, (255, 255, 255), (550, 300, 150, 50), 2)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed(num_buttons=3):
                    pos = pygame.mouse.get_pos()
                    menu_pos = (pos[0]//250, pos[1]//350)
                    if pos[0] in range(550, 700):
                        if menu_pos == (2, 0):
                            game_menu = False
                            serve = True
                            multiplayer = True
                            against_tw = False
                            vs_computer = False
                    if pos[0] in range(350, 500):
                        if menu_pos == (1, 0):
                            game_menu = False
                            serve = True
                            multiplayer = False
                            against_tw = True
                            vs_computer = False
                    if pos[0] in range(150, 300):
                        if menu_pos == (0, 0):
                            game_menu = False
                            serve = True
                            multiplayer = False
                            against_tw = False
                            vs_computer = True
    game_score = pygame.font.SysFont("euphemia", 50)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        if y >= 0:
            y -= vel
    if keys[pygame.K_DOWN]:
        if y + height <= 500:
            y += vel
    if keys[pygame.K_w]:
        if y2 >= 0:
            y2 -= vel
    if keys[pygame.K_s]:
        if y2 + height <= 500:
            y2 += vel

    if multiplayer:
        win.fill((0, 0, 0))
        for num in range(5, 495, 55):
            pygame.draw.rect(win, (255, 255, 255,), (398, num, 5, 50))
        pygame.draw.rect(win, (255, 255, 255), (x2, y2, width, height))
        pygame.draw.rect(win, (255, 255, 255), (x, y, width, height))
        pygame.draw.circle(win, (100, 255, 255), (ball_x, ball_y), radius)
        win.blit(game_score.render(str(left_score), True, (255, 255, 255)), (310, 5))
        win.blit(game_score.render(str(right_score), True, (255, 255, 255)), (450, 5))
    elif against_tw:
        win.fill((0, 0, 0))
        pygame.draw.circle(win, (100, 255, 255), (ball_x, ball_y), radius)
        pygame.draw.rect(win, (255, 255, 255), (x, y, width, height))
    elif vs_computer:
        win.fill((0, 0, 0))
        for num in range(5, 495, 55):
            pygame.draw.rect(win, (255, 255, 255,), (398, num, 5, 50))
        pygame.draw.rect(win, (255, 255, 255), (cx, cy, width, height))
        pygame.draw.rect(win, (255, 255, 255), (x, y, width, height))
        pygame.draw.circle(win, (100, 255, 255), (ball_x, ball_y), radius)
        win.blit(game_score.render(str(left_score), True, (255, 255, 255)), (310, 5))
        win.blit(game_score.render(str(right_score), True, (255, 255, 255)), (450, 5))
    if serve:
        game_start = False
        ball_x = 740
        ball_y = 300
        vel_x = 0
        vel_y = 0
        if keys[pygame.K_SPACE]:
            if ball_y in range(y, y + 121):
                game_start = True
                serve = False

    if game_start:
        if multiplayer:
            if ball_x + radius == x:
                if ball_y in range(y, y + 121):
                    pygame.mixer.Sound("paddle_hits.mp3").play()
            elif ball_x + radius == x2 + 20:
                if ball_y in range(y2, y2 + 121):
                    pygame.mixer.Sound("paddle_hits.mp3").play()
            ball_x += vel_x
            ball_y += vel_y
            if ball_x + radius == x:
                if ball_y in range(y, y + 40):
                    vel_x = -ball_vel
                    vel_y = -ball_vel
                elif ball_y in range(y + 40, y + 80):
                    vel_x = -ball_vel
                    vel_y = 0
                elif ball_y in range(y + 80, y + 121):
                    vel_x = -ball_vel
                    vel_y = ball_vel
            if ball_x - radius == x2 + 20:
                if ball_y in range(y2, y2 + 40):
                    vel_x = ball_vel
                    vel_y = -ball_vel
                elif ball_y in range(y2 + 40, y2 + 80):
                    vel_x = ball_vel
                    vel_y = 0
                elif ball_y in range(y2 + 80, y2 + 121):
                    vel_x = ball_vel
                    vel_y = ball_vel

            if ball_y + radius == 0:
                pygame.mixer.Sound("bounce.mp3").play()
                if vel_x < 0:
                    vel_x = -ball_vel
                    vel_y = ball_vel
                elif vel_x > 0:
                    vel_x = ball_vel
                    vel_y = ball_vel

            if ball_y + radius == 500:
                pygame.mixer.Sound("bounce.mp3").play()
                if vel_x < 0:
                    vel_x = -ball_vel
                    vel_y = -ball_vel
                elif vel_x > 0:
                    vel_x = ball_vel
                    vel_y = -ball_vel
            if ball_x + radius <= 0:
                right_score += 1
                serve = True
            elif ball_x + radius >= 800:
                left_score += 1
                serve = True
            if game_pause:
                vel_x = 0
                vel_y = 0

        elif against_tw:
            if ball_x + radius == x:
                if ball_y in range(y, y + 121):
                    pygame.mixer.Sound("paddle_hits.mp3").play()
            ball_x += vel_x
            ball_y += vel_y
            if ball_x + radius == x:
                if ball_y in range(y, y + 40):
                    vel_x = -ball_vel
                    vel_y = -ball_vel
                elif ball_y in range(y + 40, y + 80):
                    vel_x = -ball_vel
                    vel_y = 0
                elif ball_y in range(y + 80, y + 121):
                    vel_x = -ball_vel
                    vel_y = ball_vel
            if ball_y + radius == 0:
                pygame.mixer.Sound("bounce.mp3").play()
                if vel_x < 0:
                    vel_x = -ball_vel
                    vel_y = ball_vel
                elif vel_x > 0:
                    vel_x = ball_vel
                    vel_y = ball_vel

            if ball_y + radius == 500:
                pygame.mixer.Sound("bounce.mp3").play()
                if vel_x < 0:
                    vel_x = -ball_vel
                    vel_y = -ball_vel
                elif vel_x > 0:
                    vel_x = ball_vel
                    vel_y = -ball_vel

            if ball_x + radius == 0:
                pygame.mixer.Sound("bounce.mp3").play()
                if vel_x < 0:
                    if vel_y > 0:
                        vel_x = ball_vel
                        vel_y = ball_vel
                    elif vel_y < 0:
                        vel_x = ball_vel
                        vel_y = -ball_vel
                    elif vel_y == 0:
                        if vel_x < 0:
                            vel_x = ball_vel
            if ball_x + radius >= 800:
                win.fill((225, 0, 0))
                serve = True
        elif vs_computer:
            ball_x += vel_x
            ball_y += vel_y
            if ball_x + radius == x:
                if ball_y in range(y, y + 40):
                    pygame.mixer.Sound("paddle_hits.mp3").play()
                    vel_x = -ball_vel
                    vel_y = -ball_vel
                elif ball_y in range(y + 40, y + 80):
                    pygame.mixer.Sound("paddle_hits.mp3").play()
                    vel_x = -ball_vel
                    vel_y = 0
                elif ball_y in range(y + 80, y + 121):
                    pygame.mixer.Sound("paddle_hits.mp3").play()
                    vel_x = -ball_vel
                    vel_y = ball_vel
            if ball_x + radius == cx + 20:
                if ball_y in range(cy, cy + 40):
                    pygame.mixer.Sound("paddle_hits.mp3").play()
                    vel_x = ball_vel
                    vel_y = -ball_vel
                elif ball_y in range(cy + 40, cy + 80):
                    pygame.mixer.Sound("paddle_hits.mp3").play()
                    vel_x = ball_vel
                    vel_y = 0
                elif ball_y in range(cy + 80, cy + 121):
                    pygame.mixer.Sound("paddle_hits.mp3").play()
                    vel_x = ball_vel
                    vel_y = ball_vel

            if ball_y + radius == 0:
                pygame.mixer.Sound("bounce.mp3").play()
                if vel_x < 0:
                    vel_x = -ball_vel
                    vel_y = ball_vel
                elif vel_x > 0:
                    vel_x = ball_vel
                    vel_y = ball_vel
            if ball_y + radius == 500:
                pygame.mixer.Sound("bounce.mp3").play()
                if vel_x < 0:
                    vel_x = -ball_vel
                    vel_y = -ball_vel
                elif vel_x > 0:
                    vel_x = ball_vel
                    vel_y = -ball_vel

            if vel_x < 0:
                if vel_y < 0:
                    if ball_y < random.randint(cy, cy + 120):
                        if cy >= 0:
                            cy -= 15
                elif vel_y == 0:
                    if ball_y in range(cy, cy + 121):
                        cy += 0
                    if ball_y < cy:
                        if cy >= 0:
                            cy -= 15
                    elif ball_y > (cy + 120):
                        if cy <= 500 - height:
                            cy += 15
                elif ball_y > random.randint(cy, cy + 120):
                    if cy <= 500 - height:
                        cy += 15
            if ball_x + radius <= 0:
                right_score += 1
                serve = True
            elif ball_x + radius >= 800:
                left_score += 1
                serve = True
    pygame.display.update()
pygame.quit()
