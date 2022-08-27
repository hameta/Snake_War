# импортируем модули
import pygame
import sys
import time
import random


# инициализируем pygame
pygame.init()


# создаём окно
width = 790
height = 510
clear_color = (27, 27, 27,)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake')
icon = pygame.image.load('/Users/hameta/Programs/Python/Images/Snake_icon.png')
pygame.display.set_icon(icon)


# класс Snake
class Snake():
    # поля
    tails = None
    direction = 1

    # методы
    def __init__(self, x, y):
        self.tails = []
        for i in range(3):
            self.tails.append([x-i*10, y])

    def direct(self, event):
        if event.type == pygame.KEYDOWN:
            if self.direction % 2 == 0:
                if event.key == pygame.K_RIGHT:
                    self.direction = 1
                elif event.key == pygame.K_LEFT:
                    self.direction = 3
            elif self.direction % 2 != 0:
                if event.key == pygame.K_DOWN:
                    self.direction = 2
                elif event.key == pygame.K_UP:
                    self.direction = 4

    def move(self, speed, food):
        if self.direction == 1:
            self.tails.insert(0, [self.tails[0][0]+speed,
            self.tails[0][1]])
        elif self.direction == 2:
            self.tails.insert(0, [self.tails[0][0],
            self.tails[0][1]+speed])
        elif self.direction == 3:
            self.tails.insert(0, [self.tails[0][0]-speed,
            self.tails[0][1]])
        elif self.direction == 4:
            self.tails.insert(0, [self.tails[0][0],
            self.tails[0][1]-speed])
        if not self.eat(food):
            self.tails.pop()

        # телепорт
        if self.tails[0][0] == width:
            self.tails[0][0] = 0
        elif self.tails[0][1] == height:
            self.tails[0][1] = 0
        elif self.tails[0][0] < 0:
            self.tails[0][0] = width - 10
        elif self.tails[0][1] < 0:
            self.tails[0][1] = height - 10

    def draw(self, head_color, tail_color):
        for index, tail in enumerate(self.tails):
            x = tail[0]
            y = tail[1]
            if index == 0:
                continue
            else:
                pygame.draw.rect(screen, tail_color, [x, y, 10, 10])
        pygame.draw.rect(screen, head_color, [self.tails[0][0], self.tails[0][1], 10, 10])

    def eat(self, food):
        if [food.x, food.y] == self.tails[0]:
            return True
        else:
            return False

    def tailcut(self):
        if self.tails[0] in self.tails[1:]:
            cut = self.tails[1:].index(self.tails[0])
            for rem in range(cut+1, len(self.tails)-1):
                del self.tails[cut+1]

# класс Snakebot
class Snakebot(Snake):
    # поля
    part_long = 0


    # методы
    def direct(self, food, min, max):
        def turn_x():
            if self.direction % 2 == 0:
                if food.x > self.tails[0][0]:
                    self.direction = 1
                elif food.x < self.tails[0][0]:
                    self.direction = 3
        def turn_y():
            if self.direction % 2 != 0:
                if food.y > self.tails[0][1]:
                    self.direction = 2
                elif food.y < self.tails[0][1]:
                    self.direction = 4
        if self.tails[0][0] - food.x > 50 or \
        self.tails[0][1] - food.y > 50 or \
        self.tails[0][0] - food.x < -40 or \
        self.tails[0][1] - food.y < -40:
            if self.part_long == 0:
                self.part_long = random.randint(min, max)
                if random.randint(0, 1) == 0:
                    if abs(self.tails[0][0] - food.x) > \
                    abs(self.tails[0][1] - food.y):
                        x_or_y = 0
                    elif abs(self.tails[0][0] - food.x) < \
                    abs(self.tails[0][1] - food.y):
                        x_or_y = 1
                    else:
                        x_or_y = -1
                else:
                    x_or_y = random.randint(0, 1)
                if x_or_y == 0:
                    turn_x()
                elif x_or_y == 1:
                    turn_y()
            self.part_long -= 1
        else:
            if self.tails[0][0] == food.x:
                turn_y()
            elif self.tails[0][1] == food.y:
                turn_x()
                

# класс Food
class Food():
    # поля
    x = 0
    y = 0

    # методы
    def locate(self, generator, *extras):
        while generator:
            self.x = random.randint(0, (width-10)/10) * 10
            self.y = random.randint(0, (height-10)/10) * 10
            for extra in extras:
                if [self.x, self.y] in extra:
                    break
            else:
                generator = False

    def draw(self, color):
        pygame.draw.rect(screen, color, [self.x, self.y, 10, 10])


# инициализация объектов
snake = Snake(width/2+15, height/2-25)
snakebot = Snakebot(width/2-15, height/2-25)
apple = Food()


# первое появление яблока
apple.locate(True, snake.tails)


# игровой цикл
while True:


    # итерация событий
    for event in pygame.event.get():

        # закрытие окна
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        # направление змейки
        snake.direct(event)

    
    # направление бота
    snakebot.direct(apple, 1, 5)


    # движение змеек
    snake.move(10, apple)
    snakebot.move(10, apple)

    
    # обрезаем хвост при столкновении
    snake.tailcut()
    snakebot.tailcut()
    

    # появление яблока
    eatten = snake.eat(apple) or snakebot.eat(apple)
    apple.locate(eatten, snake.tails, snakebot.tails)


    # отрисовка
    apple.draw((200, 0, 0,))
    snakebot.draw((0, 255, 255,), (0, 200, 200,))
    snake.draw((0, 255, 0,), (0, 200, 0,))


    # очистка обновление экрана
    pygame.display.update()
    screen.fill(clear_color)


    # задержка
    time.sleep(0.06)
