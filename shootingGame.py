import pygame
from pygame.locals import *
import random
from time import sleep
import os

#색상
BLACK = (0,0,0)
WHITE = (255, 255, 255)
YELLOW  = (250, 250, 50)
RED  = (250, 50,50)

FPS = 60

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 640

class Fighter(pygame.sprite.Sprite):
    def __init__(self):
        super(Fighter, self).__init__()
        load_image = pygame.image.load('images/shooting/figter.png')
        self.image = pygame.transform.scale(load_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = int(WINDOW_WIDTH/2)
        self.rect.y = WINDOW_HEIGHT - self.rect.height
        self.dx = 0
        self.dy = 0


    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # 죄우 벽
        if self.rect.x < 0 or self.rect.x + self.rect.width > WINDOW_WIDTH:
            self.rect.x -= self.dx

        #위아래
        if self.rect.y < 0 or self.rect.y + self.rect.height > WINDOW_HEIGHT:
            self.rect.y -= self.dy

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    #충돌 났을 시
    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite

class Missile(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Missile, self).__init__()
        load_image = pygame.image.load('images/shooting/missile.png')
        self.image = pygame.transform.scale(load_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y + self.rect.height < 0:
            self.kill()

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite

class Rock(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Rock, self).__init__()

        # path = 'images/shooting/'
        # os.chdir(path)
        # files = os.listdir(path)

        rock_images = ['images/shooting/rock01.png', 'images/shooting/rock02.png', 'images/shooting/rock03.png',
                       'images/shooting/rock04.png', 'images/shooting/rock05.png', 'images/shooting/rock06.png']

        # for file in files:
        #     if 'rock*.png' in file:
        #         # f = cv2.imread(file)
        #         rock_images.append(file)


        self.image = pygame.image.load(random.choice(rock_images))
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.x = ypos
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def out_of_screen(self):
        if self.rect.y > WINDOW_HEIGHT:
            return True


def draw_text(text, font, surface, x, y, main_color):
    text_obj = font.render(text, True, main_color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj, text_rect)

def occur_explosion(surface, x, y):
    explosion_loac_image = pygame.image.load('images/shooting/explosion.png')
    explosion_image = pygame.transform.scale(explosion_loac_image, (50, 50))
    explosion_rect = explosion_image.get_rect()
    explosion_rect.x = x
    explosion_rect.y = y
    surface.blit(explosion_image, explosion_rect)

    #폭팔 발생 소리


def game_loop():
    default_font = pygame.font.Font('images/shooting/D2Coding.ttc', 28)
    background_image = pygame.image.load('images/shooting/spaceBackground.png')
    # 게임 오버 사운드

    fps_clock = pygame.time.Clock()

    fighter = Fighter()
    missiles = pygame.sprite.Group()
    rocks = pygame.sprite.Group()

    occur_prob = 40
    shot_count = 0
    count_missed = 0

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if __name__ == '__main__':
                    if event.key == pygame.K_LEFT:
                        fighter.dx -= 5
                    elif event.key == pygame.K_RIGHT:
                        fighter.dx += 5
                    elif event.key == pygame.K_UP:
                        fighter.dy -= 5
                    elif event.key == pygame.K_DOWN:
                        fighter.dy += 5
                    elif event.key == pygame.K_SPACE:
                        missile = Missile(fighter.rect.centerx, fighter.rect.centery, 10)
                        # missile.launch()
                        missiles.add(missile)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        fighter.dx = 0
                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        fighter.dy = 0

            screen.blit(background_image, background_image.get_rect())

            occur_of_rocks = 1 + int(shot_count / 300)
            min_rock_speed = 1 + int(shot_count / 200)
            max_rock_speed = 1 + int(shot_count / 100)

            if random.randint(1, occur_prob) == 1:
                for i in range(occur_of_rocks):
                    speed = random.randint(min_rock_speed, max_rock_speed)
                    rock = Rock(random.randint(0, WINDOW_WIDTH - 30), 0, speed)
                    rocks.add(rock)

            draw_text('파괴한 운석: {}'.format(shot_count), default_font,screen, 100, 20, YELLOW)
            draw_text('놓친 운석: {}'.format(shot_count), default_font, screen,400, 20, RED)

            for missile in missiles:
                rock = missile.collide(rocks)
                if rock:
                    missile.kill()
                    rock.kill()
                    occur_explosion(screen, rock.rect.x, rock.rect.y)
                    shot_count += 1

            for rock in rocks:
                if rock.out_of_screen():
                    rock.kill()
                    count_missed += 1

            rocks.update()
            rocks.draw(screen)
            missiles.update()
            missiles.draw(screen)
            fighter.update()
            fighter.draw(screen)
            pygame.display.flip()

            # 비행기가 운석과 부딪혔을 때, 놓친개 3개이상이다
            if fighter.collide(rocks) or count_missed >= 3:
                # pygame.mixer
                # 게임 노래 끝
                occur_explosion(screen, fighter.rect.x, fighter.rect.y)
                pygame.display.update()
                # gameover_sound.play()  # 게임 오벌 소리
                sleep(1)
                dont = True

            fps_clock.tick(FPS)

    return 'game_menu'

def game_menu():
    start_load_image = pygame.image.load('images/shooting/spaceBackground.png')
    start_image = pygame.transform.scale(start_load_image, (40, 40))
    screen.blit(start_image, [0,0])
    draw_x = int(WINDOW_WIDTH / 2)
    draw_y = int(WINDOW_HEIGHT / 4)
    font_70 = pygame.font.Font('images/shooting/D2Coding.ttc', 70)
    font_40 = pygame.font.Font('images/shooting/D2Coding.ttc', 40)

    draw_text('지구를 지켜라', font_70, screen, draw_x, draw_y, YELLOW)
    draw_text('엔터 키를 누르면', font_40, screen, draw_x, draw_y + 200, WHITE)
    draw_text('게임이 시작됩니다.', font_40, screen, draw_x, draw_y + 250, WHITE)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return 'play'
            elif event.key == QUIT:
                return 'quit'


    return 'game_menu'

def main():
    global screen

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("SHOOTING GAME")

    action = 'game_menu'
    while action != 'quit':
        if action == 'game_menu':
            action = game_menu()
        elif action == 'play':
            action = game_loop()

    pygame.quit()

if __name__ == "__main__":
    main()





