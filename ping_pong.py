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
    """Base Class for instances of the paddle used by players of the game."""
    def __init__(self, x):
        self.x = x
        self.y = 190
        self.width = 15
        self.height = 120
        self.vel = 10
        self.score = 0
        self.area_color = (0, 0, 0) # Background color of a player's half of the screen
        self.time_area_color_changed = 0

    def draw(self):
        """Renders paddle"""
        pygame.draw.rect(win, white, (self.x, self.y, self.width, self.height))

    def move(self):
        """Moves paddle"""
        # player1 movement controls
        if self.x == 730:
            if self.y > 0:
                if keys[pygame.K_UP]:
                    self.y -= self.vel
            if self.y + self.height < 500:
                if keys[pygame.K_DOWN]:
                    self.y += self.vel

        # player2 movement controls if it's an instance of Player class
        elif self.x == 35:
            if self.y > 0:
                if keys[pygame.K_w]:
                    self.y -= self.vel
            if self.y < 500:
                if keys[pygame.K_s]:
                    self.y += self.vel

    def reset(self):
        self.y = 190

    def area_color_to_black(self):
        """Changes area_color attr to black if it has been changed"""
        if self.area_color != (0, 0, 0):
            if current_time() - self.time_area_color_changed >= 0.2: # new area_color must display for at least 0.2s
                self.area_color = (0, 0, 0)


class Computer:
    """Computer player Class"""
    x = 35
    y = 190 # Best position to be on the y-axis if it wants to reach any incoming ball 
    width = 15
    height = 120
    vel = 10
    score = 0
    random_range = None # range on the paddle's body where we want the ball to collide within
    can_move = False
    collision_point_y = None # Only position where ball can collide with paddle on the y-axis
    return_to_best_pos = False 
    area_color = (0, 0, 0) # Background color of Computer player's half of the screen
    time_area_color_changed = 0

    @classmethod
    def draw(cls):
        """Renders paddle"""
        pygame.draw.rect(win, white, (cls.x, cls.y, cls.width, cls.height))

    @classmethod
    def move(cls):
        """Moves paddle"""
        if cls.return_to_best_pos:
            if cls.y < 190:
                cls.y += cls.vel
            elif cls.y > 190:
                cls.y -= cls.vel
            else:
                cls.return_to_best_pos = False # Computer is in best position

        if not (cls.can_move and cls.collision_point_y):
            return
        if not cls.random_range:
            cls.random_range = random.choice(((0, 40),(41, 80),(81, 120)))

        if not((cls.y+cls.random_range[0])<=cls.collision_point_y and (cls.y+cls.random_range[1])>=cls.collision_point_y):
            # Computer.collision_point_y is not within the range of Computer.random_range
            if cls.collision_point_y < (cls.y+cls.random_range[0]):
                if cls.y > 0:
                    cls.y -= cls.vel
            elif cls.collision_point_y > (cls.y+cls.random_range[1]):
                if cls.y + cls.height < 500:
                    cls.y += cls.vel
        else:
            cls.can_move = False
        
    @classmethod      
    def reset(cls):
        """Resets attributes that may have changed back to default"""
        cls.y = 190
        cls.random_range = None
        cls.can_move = True
        cls.collision_point_y = None

    @classmethod
    def area_color_to_black(cls):
        """Changes area_color attr to black if it has been changed"""
        if cls.area_color != (0, 0, 0):
            if current_time() - cls.time_area_color_changed >= 0.2: # new area_color must display for at least 0.2s
                cls.area_color = (0, 0, 0)
       

class Ball:
    """Ball Class"""
    x = 720
    y = 250
    radius = 10
    vel_x = 0
    vel_y = 0

    @classmethod
    def draw(cls):
        """Renders Ball that will be played on screen"""
        pygame.draw.circle(win, (100, 255, 255), (cls.x, cls.y), cls.radius)

    @classmethod
    def move(cls):
        """Moves Ball"""
        cls.x += cls.vel_x
        cls.y += cls.vel_y
            
    @classmethod
    def collision_with_walls_movement(cls):
        """Detects Ball's Collisions with walls"""
        if cls.y - cls.radius == 0:
            # Ball collided with top horizontal wall
            pygame.mixer.Sound("bounce.mp3").play()
            cls.vel_y = 15

        elif cls.y + cls.radius == 500:
            # Ball collided with bottom horizontal wall
            pygame.mixer.Sound("bounce.mp3").play()
            cls.vel_y = -15
            
        if cls.vel_x < 0:
            if cls.x <= 255:
                Computer.can_move = True # This is one of the reasons why Computer player can lose

        if cls.x + cls.radius <= 0:
            update_score(player1)
        elif cls.x + cls.radius >= 780:
            update_score(player2)
                
    @classmethod
    def check_collision_with(cls, player, new_vel):
        """Detects Ball's Collisions with players' paddles"""
        if (cls.y >= player.y and cls.y <= player.y+40): # If Ball hits the top section of the paddle
            cls.vel_y = -15
        elif (cls.y >= player.y+41 and cls.y <= player.y+80): # If Ball hits the middle section of the paddle
            cls.vel_y = 0
        elif (cls.y >= player.y+81 and cls.y <= player.y+120): # If Ball hits the bottom section of the paddle
            cls.vel_y = 15
        else:
            return
        cls.vel_x = new_vel
        pygame.mixer.Sound("paddle_hits.mp3").play()

        if player2 != Computer:
            return

        if player == player1:
            # Compute Computer.collision_point_y
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
            Computer.return_to_best_pos = random.choice([True, False]) # Random decision to return to best position
            Computer.random_range = None


class GameState():
    """Class that manages the game states"""
    menu_x = 180 # Game menu highlight box's x-coordinate
    menu_y = 300 # Game menu highlight box's y-coordinate
    start = False
    player_to_serve = None
    time_started = 0 # Time Computer player lost a ball

    @classmethod
    def display_game_menu(cls):
        """Displays Game menu UI"""
        win.fill((0, 0, 0))
        win.blit(title_font.render("PING PONG", True, white), (150, 50))
        win.blit(options_font.render("VS Computer", True, white), (200, 310))
        win.blit(options_font.render("MULTIPLAYER", True, white), (400, 310))
        pygame.draw.rect(win, white, (cls.menu_x, cls.menu_y, 180, 50), 2) # Displays highlight box

    @classmethod
    def highlight_option(cls, move_right):
        """Moves highlight box in Game menu UI"""
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
        """Selects an Option and returns a player object"""
        cls.start = True
        cls.player_to_serve = player1
        if cls.menu_x == 180:
            # Option to play against Computer was chosen
            return Computer
        if cls.menu_x == 380:
            # Multiplayer option was chosen
            return Player(35)

    @classmethod
    def update_serving_player(cls):
        """Serves the ball and performs actions that should occur when a player serves"""
        cls.player_to_serve.area_color = (0, 50, 0)
        cls.player_to_serve.time_area_color_changed = current_time()
        cls.player_to_serve = None # serves the ball


player1 = Player(730) # This will always be player one no matter the mode of play
player2 = None # To be determined by the mode of play e.g multiplayer
run = True

def update_score(player):
    """Updates the Score of a player if it scores and sets up for the next serve"""
    player.score += 1

    if player == player1:
        GameState.player_to_serve = player2
        player2.area_color = (70, 0, 0)
        player2.time_area_color_changed = current_time()
    else:
        GameState.player_to_serve = player1
        player1.area_color = (70, 0, 0)
        player1.time_area_color_changed = current_time()

    if GameState.player_to_serve == player2 and player2 == Computer:
        GameState.time_started = current_time()

    Ball.vel_x = 0
    Ball.vel_y = 0
    player1.reset()
    player2.reset()

def serve_if_player_to_serve():
    """Controls the serving mechanism if there's a player to serve"""
    if GameState.player_to_serve == player1:
        Ball.x = 720
        Ball.y = 250
        if keys[pygame.K_SPACE] and (Ball.y >= player1.y and Ball.y <= player1.y+120):
            # Space was pressed and ball is within player's paddle range
            GameState.update_serving_player()

    elif GameState.player_to_serve == player2:
        Ball.x = 60
        Ball.y = 250
        if GameState.player_to_serve == Computer:
            Computer.collision_point_y = Ball.y
            if Computer.can_move == False: 
                # Computer.collision_point_y is in the proper range
                GameState.update_serving_player()
        elif keys[pygame.K_SPACE] and (Ball.y >= player2.y and Ball.y <= player2.y+120):
            # Space was pressed and ball is within player's paddle range
            GameState.update_serving_player()

def game_diplay():
    """Displays Game play UI"""
    win.fill((0, 0, 0))

    player2.area_color_to_black() # Incase area color has been changed
    pygame.draw.rect(win, player2.area_color, (0, 0, 398, 500))
    win.blit(score_font.render(str(player2.score), True, white), (310, 5))

    player1.area_color_to_black() # Incase area color has been changed
    pygame.draw.rect(win, player1.area_color, (403, 0, 393, 500))
    win.blit(score_font.render(str(player1.score), True, white), (450, 5))

    for num in range(5, 495, 55):
        pygame.draw.rect(win, white, (398, num, 5, 50))

    player1.draw()
    player2.draw()
    Ball.draw()

def movements_and_collisions():
    """Controls the movements and collisions during gameplay"""
    player1.move()
    if GameState.player_to_serve == Computer:
        if (current_time() - GameState.time_started) >= 0.6: # Adds a delay of at least 0.6s before Computer serves
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

while run:
    pygame.time.delay(12)
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
        serve_if_player_to_serve()
        game_diplay()
        movements_and_collisions()
   
    pygame.display.update()
pygame.quit()