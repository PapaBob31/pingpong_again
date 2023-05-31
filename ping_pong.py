# ping pong
import pygame
import random
from time import time as current_time
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("ping pong")
win = pygame.display.set_mode((780, 500))
font = pygame.font.SysFont("algerian", 100)
text = pygame.font.SysFont("verdana", 20)
game_score = pygame.font.SysFont("euphemia", 50)
white = (255, 255, 255)


class player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 15
        self.height = 120
        self.x_serve_pos = x
        self.y_serve_pos = y
        self.vel = 10
        self.serve = False

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

    def reset_position(self):
        self.x = self.x_serve_pos
        self.y = self.y_serve_pos


class Computer:
    x = 35
    y = 190
    width = 15
    height = 120
    vel = 10
    random_position = None
    smart_movement = False
    can_move = False
    collision_point_y = None
    serve = False
    return_to_best_pos = False

    @staticmethod
    def draw():
        pygame.draw.rect(win, white, (Computer.x, Computer.y, Computer.width, Computer.height))

    @staticmethod
    def move():
        if Computer.return_to_best_pos:
            if Computer.y < 190:
                Computer.y += Computer.vel
            elif Computer.y > 190:
                Computer.y -= Computer.vel
            else:
                Computer.return_to_best_pos = False
        if not (Computer.can_move and Computer.collision_point_y):
            return
        if not Computer.random_position:
            Computer.random_position = random.choice([[0, 40],[41, 80],[81, 120]])
        if not((Computer.y+Computer.random_position[0])<=Computer.collision_point_y and (Computer.y+Computer.random_position[1])>=Computer.collision_point_y):
            if Computer.collision_point_y < (Computer.y+Computer.random_position[0]):
                if Computer.y > 0:
                    Computer.y -= Computer.vel
            elif Computer.collision_point_y > (Computer.y+Computer.random_position[1]):
                if Computer.y + 120 < 500:
                    Computer.y += Computer.vel
        else:
            Computer.can_move = False
        
    @staticmethod       
    def reset_position():
        Computer.x = 35
        Computer.y = 190
        Computer.random_position = None
       

class Ball:
    x = 720
    y = 250
    radius = 10
    vel_x = 0
    vel_y = 0
    vel = 15
    hit_top_wall = False
    hit_bottom_wall = False

    @staticmethod
    def draw():
        pygame.draw.circle(win, (100, 255, 255), (Ball.x, Ball.y), Ball.radius)

    @staticmethod
    def move():
        Ball.x += Ball.vel_x
        Ball.y += Ball.vel_y
            
    @staticmethod
    def collision_with_walls_movement():
        if Ball.y - Ball.radius == 0:
            pygame.mixer.Sound("bounce.mp3").play()
            Ball.vel_y = Ball.vel

        if Ball.y + Ball.radius == 500:
            pygame.mixer.Sound("bounce.mp3").play()
            Ball.vel_y = -Ball.vel
            

        if Ball.vel_x < 0:
            if Ball.x <= 285:
                Computer.can_move = True

            elif Ball.vel_y == 0 and Ball.x <= 360:
                Computer.can_move = True

        if Ball.x + Ball.radius <= 0:
            GameState.update_score(False)
        elif Ball.x + Ball.radius >= 780:
            GameState.update_score(True)
                
    @staticmethod
    def collision_with(player):
        if not (Ball.x == 60 or Ball.x == 720):
            return
        if not (Ball.y >= player.y and Ball.y <= player.y+120):
            return

        if Ball.x == 60 and player == player2:
            Ball.vel_x = Ball.vel
        elif Ball.x == 720  and player == player1:
            Ball.vel_x = -Ball.vel
        else:
            return

        if (Ball.y >= player.y and Ball.y <= player.y+40):
            Ball.vel_y = -Ball.vel
        elif (Ball.y >= player.y+41 and Ball.y <= player.y+80):
            Ball.vel_y = 0
        elif (Ball.y >= player.y+81 and Ball.y <= player.y+120):
            Ball.vel_y = Ball.vel

        # return
        if player == player1:
            if Ball.vel_y < 0:
                if Ball.y < 180:
                    Computer.collision_point_y = 300 + Ball.y
                else:
                    Computer.collision_point_y = 680 - Ball.y
            elif Ball.vel_y > 0:
                if Ball.y > 320:
                   Computer.collision_point_y = Ball.y - 300  
                else:
                    Computer.collision_point_y = 320-Ball.y
            else:
                Computer.collision_point_y = Ball.y
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
    left_score = 0
    right_score = 0
    time_started = 0

    @staticmethod
    def display_game_menu():
        win.fill((0, 0, 0))
        win.blit(font.render("PING PONG", True, white), (150, 50))
        win.blit(text.render("VS Computer", True, white), (200, 310))
        win.blit(text.render("MULTIPLAYER", True, white), (400, 310))
        pygame.draw.rect(win, white, (GameState.menu_x, GameState.menu_y, 180, 50), 2)

    @staticmethod
    def highlight_option(move_right):
        if move_right:
            GameState.menu_x += 200
        else:
            GameState.menu_x -= 200

        if GameState.menu_x > 380:
            GameState.menu_x = 180
        elif GameState.menu_x < 180:
            GameState.menu_x = 380

    @staticmethod
    def select_option():
        GameState.start = True
        GameState.player_to_serve = player1
        if GameState.menu_x == 180:
            GameState.multiplayer = False
            return Computer
        if GameState.menu_x == 380:
            GameState.multiplayer = True
            return player(35, 190)

    @staticmethod
    def update_score(right):
        if right:
            GameState.right_score += 1
            GameState.player_to_serve = player1
        else:
            GameState.left_score += 1
            GameState.player_to_serve = player2
            player2.can_move = True
            GameState.time_started = current_time()
        win.fill((225, 0, 0))
        Ball.vel_x = 0
        Ball.vel_y = 0
        player1.reset_position()
        player2.reset_position()


player1 = player(730, 190)
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
                GameState.player_to_serve = None
        elif GameState.player_to_serve == player1:
            Ball.x = 720
            Ball.y = 250
            if keys[pygame.K_SPACE] and (Ball.y >= player1.y and Ball.y <= player1.y+120):
                GameState.player_to_serve = None

        win.fill((0, 0, 0))
        pygame.draw.rect(win, (0, 0, 0), (0, 0, 388, 500))
        win.blit(game_score.render(str(GameState.left_score), True, white), (310, 5))
        pygame.draw.rect(win, (0, 0, 0), (393, 0, 393, 500))
        win.blit(game_score.render(str(GameState.right_score), True, white), (450, 5))
        for num in range(5, 495, 55):
            pygame.draw.rect(win, white, (398, num, 5, 50))

        player1.draw()
        player2.draw()
        Ball.draw()
        player1.move()
        if GameState.player_to_serve == player2:
            if (current_time() - GameState.time_started) >= 0.5:
                player2.move()
        else:
            player2.move()
        Ball.move()
        if not GameState.player_to_serve:
            Ball.collision_with(player1)
            Ball.collision_with(player2)
        Ball.collision_with_walls_movement()
   
    pygame.display.update()
pygame.quit()