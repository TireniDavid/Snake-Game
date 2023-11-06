import pygame
from pygame.locals import *
import time
import random
from pygame import mixer, image

SIZE = 40

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.fruit = pygame.image.load("resources/apple.jpg").convert()
        self.x = SIZE * 12
        self.y = SIZE * 12

    def draw(self):
        self.parent_screen.blit(self.fruit, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 24) * SIZE
        self.y = random.randint(0, 14) * SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        mixer.init()
        self.play_background_music("bg_music_1")
        self.surface = pygame.display.set_mode((1000, 600))
        self.render_background("background")
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.speed_x = 0.25

    def is_collision(self, x2, y2, x1, y1):
        if x2 <= x1 < x2 + SIZE:
            if y2 <= y1 < y2 + SIZE:
                return True

        return False

    def collision_itself(self):
        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                self.ending_sound()

                raise "Game_replay"

    def collision_wall(self):
        #side y
        for i in range(-1, 16, 16):
             for j in range(0, 26*SIZE, SIZE):
                 if self.is_collision(self.snake.x[0], self.snake.y[0], j, i * SIZE):
                     self.play_sound("crash")
                     self.ending_sound()
                     raise "Game_replay"

        #side x
        for i in range(-1, 26, 26):
            for j in range(0, 16* SIZE, SIZE):
                if self.is_collision(self.snake.x[0], self.snake.y[0], i * SIZE, j):
                    self.play_sound("crash")
                    self.ending_sound()
                    raise "Game_replay"



    def play(self):
        self.render_background("background")
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("eat")
            self.snake.increase_length()
            self.apple.move()

        self.collision_itself()
        self.collision_wall()

    def display_score(self):
        font = pygame.font.SysFont('arial', 40, True)
        score = font.render(f"Score: {self.snake.length - 1}", True, (255, 255, 255))
        self.surface.blit(score, (800, 10))

    def display_game_over(self):
        font = pygame.font.SysFont('arial', 100, True)
        game_over = font.render(f"Game Over!", True, (255, 255, 255))
        self.surface.blit(game_over, (300, 200))
        font = pygame.font.SysFont('arial', 20, True)
        replay = font.render(f"Press 'Enter' to replay", True, (255, 255, 255))
        self.surface.blit(replay, (400, 330))
        pygame.display.flip()

    def play_background_music(self, back_music):
        mixer.music.load(f"resources/{back_music}.mp3")
        mixer.music.play(-1)

    def play_sound(self, sound):
        sound_type = mixer.Sound(f"resources/{sound}.mp3")
        sound_type.play()
    def ending_sound(self):
        time.sleep(0.5)
        self.play_sound("gameover")
    def render_background(self, bg):
        bg_image = image.load(f"resources/{bg}.jpg")
        self.surface.blit(bg_image, (0, 0))

    def reset(self):

        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)




    def increase_speed(self):
        self.speed_x -= 0.03
    def reduce_speed(self):
        self.speed_x += 0.03


    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False
                        self.play_background_music("bg_music_1")

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_EQUALS:
                            self.increase_speed()
                        if event.key == K_MINUS:
                            self.reduce_speed()

                elif event.type == QUIT:
                    running = False


            if self.increase_speed():
                time.sleep(self.speed_x)
            if self.reduce_speed():
                time.sleep(self.speed_x)
            else:
                time.sleep(self.speed_x)


            try:
                if not pause:
                    self.play()

            except:
                self.display_game_over()
                pause = True
                mixer.music.stop()
                self.reset()




if __name__ == "__main__":
    game = Game()
    game.run()
