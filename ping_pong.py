import pygame
import random
from time import time as current_time
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("ping pong")
win = pygame.display.set_mode((780, 500))
title_font = pygame.font.SysFont("algerian", 100)
options_font = pygame.font.SysFont("verdana", 20)
score_font = pygame.font.SysFont("euphemia", 50)
white = (255, 255, 255)


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 15
        self.height = 120
        self.x_serve_pos = x
        self.y_serve_pos = y
        self.vel = 10
        self.score = 0
        self.area_color = (0, 0, 0)
        self.time_area_color_changed = 0

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

    def reset(self):
        self.x = self.x_serve_pos
        self.y = self.y_serve_pos

    def area_color_to_black(self):
        if self.area_color != (0, 0, 0):
            if current_time() - self.time_area_color_changed >= 0.2:
                self.area_color = (0, 0, 0)


class Computer:
    x = 35
    y = 190
    width = 15
    height = 120
    vel = 10
    score = 0
    random_position = None
    can_move = False
    collision_point_y = None
    return_to_best_pos = False
    area_color = (0, 0, 0)
    time_area_color_changed = 0

    @classmethod
    def draw(cls):
        pygame.draw.rect(win, white, (cls.x, cls.y, cls.width, cls.height))

    @classmethod
    def move(cls):
        if cls.return_to_best_pos:
            if cls.y < 190:
                cls.y += cls.vel
            elif cls.y > 190:
                cls.y -= cls.vel
            else:
                cls.return_to_best_pos = False
        if not (cls.can_move and cls.collision_point_y):
            return
        if not cls.random_position:
            cls.random_position = random.choice([[0, 40],[41, 80],[81, 120]])

        if not((cls.y+cls.random_position[0])<=cls.collision_point_y and (cls.y+cls.random_position[1])>=cls.collision_point_y):
            if cls.collision_point_y < (cls.y+cls.random_position[0]):
                if cls.y > 0:
                    cls.y -= cls.vel
            elif cls.collision_point_y > (cls.y+cls.random_position[1]):
                if cls.y + cls.height < 500:
                    cls.y += cls.vel
        else:
            cls.can_move = False
        
    @classmethod      
    def reset(cls):
        cls.y = 190
        cls.random_position = None
        cls.can_move = True
        cls.collision_point_y = None

    @classmethod
    def area_color_to_black(cls):
        if cls.area_color != (0, 0, 0):
            if current_time() - cls.time_area_color_changed >= 0.2:
                cls.area_color = (0, 0, 0)
       

class Ball:
    x = 720
    y = 250
    radius = 10
    vel_x = 0
    vel_y = 0

    @classmethod
    def draw(cls):
        pygame.draw.circle(win, (100, 255, 255), (cls.x, cls.y), cls.radius)

    @classmethod
    def move(cls):
        cls.x += cls.vel_x
        cls.y += cls.vel_y
            
    @classmethod
    def collision_with_walls_movement(cls):
        if cls.y - cls.radius == 0:
            pygame.mixer.Sound("bounce.mp3").play()
            cls.vel_y = 15

        elif cls.y + cls.radius == 500:
            pygame.mixer.Sound("bounce.mp3").play()
            cls.vel_y = -15
            
        if cls.vel_x < 0:
            if cls.x <= 285:
                Computer.can_move = True

        if cls.x + cls.radius <= 0:
            GameState.update_score(player1)
        elif cls.x + cls.radius >= 780:
            GameState.update_score(player2)
                
    @classmethod
    def check_collision_with(cls, player, new_vel):
        if (cls.y >= player.y and cls.y <= player.y+40):
            cls.vel_y = -15
        elif (cls.y >= player.y+41 and cls.y <= player.y+80):
            cls.vel_y = 0
        elif (cls.y >= player.y+81 and cls.y <= player.y+120):
            cls.vel_y = 15
        else:
            return
        cls.vel_x = new_vel

        if player == player1:
            if cls.vel_y < 0:
                if cls.y < 180:
                    Computer.collision_point_y = 300 + cls.y
                else:
                    Computer.collision_point_y = 680 - cls.y
            elif cls.vel_y > 0:
                if cls.y > 320:
                   Computer.collision_point_y = cls.y - 300 
                else:
                    Computer.collision_point_y = 320 - cls.y
            else:
                Computer.collision_point_y = cls.y
        else:
            Computer.collision_point_y = None
            Computer.return_to_best_pos = random.choice([True, False])
            Computer.random_position = None


class GameState():
    menu_x = 180
    menu_y = 300
    start = False
    multiplayer = True
    player_to_serve = None
    time_started = 0

    @classmethod
    def display_game_menu(cls):
        win.fill((0, 0, 0))
        win.blit(title_font.render("PING PONG", True, white), (150, 50))
        win.blit(options_font.render("VS Computer", True, white), (200, 310))
        win.blit(options_font.render("MULTIPLAYER", True, white), (400, 310))
        pygame.draw.rect(win, white, (cls.menu_x, cls.menu_y, 180, 50), 2)

    @classmethod
    def highlight_option(cls, move_right):
        if move_right:
            cls.menu_x += 200
        else:
            cls.menu_x -= 200

        if cls.menu_x > 380:
            cls.menu_x = 180
        elif cls.menu_x < 180:
            cls.menu_x = 380

    @classmethod
    def select_option(cls):
        cls.start = True
        cls.player_to_serve = player1
        if cls.menu_x == 180:
            cls.multiplayer = False
            return Computer
        if cls.menu_x == 380:
            cls.multiplayer = True
            return Player(35, 190)

    @classmethod
    def update_score(cls, player):
        player.score += 1
        if player == player1:
            cls.player_to_serve = player2
            player2.area_color = (70, 0, 0)
            player2.time_area_color_changed = current_time()
        else:
            cls.player_to_serve = player1
            player1.area_color = (70, 0, 0)
            player1.time_area_color_changed = current_time()

        if cls.player_to_serve == player2 and player2 == Computer:
            cls.time_started = current_time()

        Ball.vel_x = 0
        Ball.vel_y = 0
        player1.reset()
        player2.reset()

    @classmethod
    def update_serving_player(cls):
        cls.player_to_serve.area_color = (0, 50, 0)
        cls.player_to_serve.time_area_color_changed = current_time()
        cls.player_to_serve = None


player1 = Player(730, 190)
player2 = None
run = True

while run:
    pygame.time.delay(15)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if not GameState.start:
                if event.key == pygame.K_LEFT:
                    GameState.highlight_option(False)
                if event.key == pygame.K_RIGHT:
                    GameState.highlight_option(True)
                if event.key == pygame.K_x:
                    player2 = GameState.select_option()

    if not GameState.start:
        GameState.display_game_menu()
    if GameState.start:
        keys = pygame.key.get_pressed()

        if GameState.player_to_serve == Computer:
            Ball.x = 60
            Ball.y = 250
            Computer.collision_point_y = Ball.y
            if Computer.can_move == False: # computer is in proper ball range
                GameState.update_serving_player()

        elif type(GameState.player_to_serve) == Player:
            Ball.x = 720
            Ball.y = 250
            if keys[pygame.K_SPACE] and (Ball.y >= player1.y and Ball.y <= player1.y+120):
                GameState.update_serving_player()

        win.fill((0, 0, 0))
        player2.area_color_to_black()
        pygame.draw.rect(win, player2.area_color, (0, 0, 398, 500))
        win.blit(score_font.render(str(player2.score), True, white), (310, 5))
        player1.area_color_to_black()
        pygame.draw.rect(win, player1.area_color, (403, 0, 393, 500))
        win.blit(score_font.render(str(player1.score), True, white), (450, 5))
        for num in range(5, 495, 55):
            pygame.draw.rect(win, white, (398, num, 5, 50))

        player1.draw()
        player2.draw()
        Ball.draw()
        player1.move()
        if GameState.player_to_serve == player2:
            if (current_time() - GameState.time_started) >= 0.6:
                player2.move()
        else:
            player2.move()
        Ball.move()
        if not GameState.player_to_serve:
            if Ball.x == 720:
                Ball.check_collision_with(player1, -15)
            elif Ball.x == 60:
                Ball.check_collision_with(player2, 15)
        Ball.collision_with_walls_movement()
   
    pygame.display.update()
pygame.quit()