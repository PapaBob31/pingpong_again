# ping pong
import pygame
import random
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("ping pong")
win = pygame.display.set_mode((780, 500))
font = pygame.font.SysFont("algerian", 100)
text = pygame.font.SysFont("verdana", 15)
game_score = pygame.font.SysFont("euphemia", 50)
run = True
game_menu = True
game_start = False
menu_x = 150
menu_y = 300
versus_computer = False
against_wall = False
multiplayer = False
serve = True
white = (255, 255, 255)
left_score = 0
right_score = 0
reset = False


class player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 15
        self.height = 120
        self.x_serve_pos = x
        self.y_serve_pos = y
        self.vel = 10

    def draw(self):
        pygame.draw.rect(win, white, (self.x, self.y, self.width, self.height))

    def move(self): 
        if self.x == 730:
            if self.y > 0:
                if keys[pygame.K_UP]:
                    self.y -= self.vel
            if self.y + self.height < 500:
                if keys[pygame.K_DOWN]:
                    self.y += self.vel
        elif self.x == 35:
            if self.y > 0:
                if keys[pygame.K_w]:
                    self.y -= self.vel
            if self.y < 500:
                if keys[pygame.K_s]:
                    self.y += self.vel

    def reset_positions(self):
        self.x = self.x_serve_pos
        self.y = self.y_serve_pos


class computerPlayer:
    def __init__(self):
        self.x = 35
        self.y = 180
        self.width = 15
        self.height = 120
        self.vel = 15
        self.random_no = random.randrange(0, 90, 10)
        self.random_vel = 0
        self.in_range = False

    def draw(self):
        pygame.draw.rect(win, white, (self.x, self.y, self.width, self.height))

    def random_velocity(self):
        vel = [0, 10, -10]
        random_vel =  random.choice(vel)
        return random_vel

    def move(self, ball):
        if ball.vel_x < 0:
            if ball.y in range(self.y+40, self.y+80) and ball.vel_y == 0:
                if self.y > 0 and self.random_vel < 0:
                    self.y += self.random_vel
                    print(self.random_vel)
                    self.in_range = True
                if self.y + self.height < 500 and self.random_vel > 0:
                    self.y += self.random_vel
                    print(self.random_vel)
                    self.in_range = True
            elif ball.y not in range(self.y, self.y+121) or ball.vel_y != 0:
                self.in_range = False
                
            if not self.in_range:
                if ball.y < self.y + self.random_no:
                    if self.y > 0: 
                        self.y -= self.vel
                if ball.y > self.y + self.random_no:
                    if self.y + self.height < 500:
                        self.y += self.vel
            
    def reset_position(self):
        self.x = 35
        self.y = 180
       

class gameBall:
    def __init__(self):
        self.x = 720
        self.y = 250
        self.radius = 10
        self.vel_x = 0
        self.vel_y = 0
        self.vel = 15

    def draw(self):
        pygame.draw.circle(win, (100, 255, 255), (self.x, self.y), self.radius)

    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def collision_with_walls_movement(self):
        global serve, left_score, right_score, reset
        if self.y - self.radius == 0:
            pygame.mixer.Sound("bounce.mp3").play()
            if self.vel_x < 0:
                self.vel_x = -self.vel
                self.vel_y = self.vel
            elif self.vel_x > 0:
                self.vel_x = self.vel
                self.vel_y = self.vel

        if self.y + self.radius == 500:
            pygame.mixer.Sound("bounce.mp3").play()
            if self.vel_x < 0:
                self.vel_x = -self.vel
                self.vel_y = -self.vel
            elif self.vel_x > 0:
                self.vel_x = self.vel
                self.vel_y = -self.vel

        if multiplayer or versus_computer:
            if self.x + self.radius <= 0:
                right_score += 1
                win.fill((225, 0, 0))
                reset = True
                serve = True
            if self.x + self.radius >= 780:
                left_score += 1
                win.fill((225, 0, 0))
                reset = True
                serve = True

    def collision_with(self, player):
        if player == player1:
            if self.x + self.radius == player.x:
                if self.y in range(player.y, player.y + 40):
                    self.vel_x = -self.vel
                    self.vel_y = -self.vel
                if self.y in range(player.y + 40, player.y + 80):
                    self.vel_x = -self.vel
                    self.vel_y = 0
                if self.y in range(player.y + 80, player.y + 121):
                    self.vel_x = -self.vel
                    self.vel_y = self.vel

        elif player == player2 or player == computer:
            if player.x + player.width == self.x - self.radius:
                if self.y in range(player.y, player.y + 40):
                    self.vel_x = self.vel
                    self.vel_y = -self.vel
                if self.y in range(player.y + 40, player.y + 80):
                    self.vel_x = self.vel
                    self.vel_y = 0
                if self.y in range(player.y + 80, player.y + 121):
                    self.vel_x = self.vel
                    self.vel_y = self.vel


def display_game_menu():
    win.fill((0, 0, 0))
    win.blit(font.render("PING PONG", True, white), (150, 50))
    win.blit(text.render("VS Computer", True, white), (170, 310))
    win.blit(text.render("Against the wall", True, white), (370, 310))
    win.blit(text.render("MULTIPLAYER", True, white), (570, 310))
    pygame.draw.rect(win, white, (menu_x, menu_y, 150, 50), 2)

computer = computerPlayer()
ball = gameBall()
player1 = player(730, 180)
player2 = player(35, 180)

while run:
    pygame.time.delay(15)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if game_menu:
                if event.key == pygame.K_LEFT:
                    if menu_x != 150:
                        menu_x -= 200
                    else:
                        menu_x = 550
                if event.key == pygame.K_RIGHT:
                    if menu_x != 550:
                        menu_x += 200
                    else:
                        menu_x = 150
                if event.key == pygame.K_x:
                    if menu_x == 150:
                        versus_computer = True
                        game_start = True
                        game_menu = False
                    if menu_x == 350:
                        against_wall = True
                        game_start = True
                        game_menu = False
                    if menu_x == 550:
                        multiplayer = True
                        game_start = True
                        game_menu = False

    if game_menu:
        display_game_menu()
    if game_start:
        keys = pygame.key.get_pressed()
        if serve:
            ball.x = 720
            ball.y = 250
            ball.vel_x = 0
            ball.vel_y = 0
            if reset:
                player1.reset_positions()
                player2.reset_positions()
                computer.reset_position()
                reset = False
            if keys[pygame.K_SPACE]:
                if ball.y in range(player1.y, player1.y + 121):
                    serve = False

        win.fill((0, 0, 0))
        if versus_computer or multiplayer:
            win.blit(game_score.render(str(left_score), True, white), (310, 5))
            win.blit(game_score.render(str(right_score), True, white), (450, 5))
            for num in range(5, 495, 55):
                pygame.draw.rect(win, white, (398, num, 5, 50))

        if versus_computer:
            player1.draw()
            player1.move()
            computer.move(ball)
            computer.draw()
            ball.draw()
            ball.move()
            ball.collision_with(player1)
            if not serve:
                if ball.x + ball.radius == player1.x:
                    computer.random_vel = computer.random_velocity()
                    computer.random_no = random.randrange(0, 90, 10)
            ball.collision_with(computer)
            ball.collision_with_walls_movement()

        elif against_wall:
            player1.draw()
            player1.move()
            ball.draw()
            ball.move()
            ball.collision_with(player1)
            ball.collision_with_walls_movement()
            if ball.x - ball.radius <= 0:
                pygame.mixer.Sound("bounce.mp3").play()
                if ball.vel_y > 0:
                    ball.vel_x = ball.vel
                    ball.vel_y = ball.vel
                elif ball.vel_y < 0:
                    ball.vel_x = ball.vel
                    ball.vel_y = -ball.vel
                elif ball.vel_y == 0:
                    ball.vel_x = ball.vel
            if ball.x + ball.radius >= 780:
                win.fill((225, 0, 0))
                reset = True
                serve = True

        elif multiplayer:
            player1.draw()
            player2.draw()
            ball.draw()
            player1.move()
            player2.move()
            ball.move()
            ball.collision_with(player1)
            ball.collision_with(player2)
            ball.collision_with_walls_movement()
            
    pygame.display.update()
pygame.quit()