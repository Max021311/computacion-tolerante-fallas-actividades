import pygame
import sys
import random
import pickle

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

WIDTH, HEIGHT = 600, 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

snake = [(100, 100), (90, 100), (80, 100)]
direction = (10, 0)
fruit = (random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10)
score = 0

def draw_snake():
    for segmento in snake:
        pygame.draw.rect(window, GREEN, pygame.Rect(segmento[0], segmento[1], 10, 10))

def draw_fruit():
    pygame.draw.rect(window, WHITE, pygame.Rect(fruit[0], fruit[1], 10, 10))

def game():
    global direction, score, fruit

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 10):
                    direction = (0, -10)
                elif event.key == pygame.K_DOWN and direction != (0, -10):
                    direction = (0, 10)
                elif event.key == pygame.K_LEFT and direction != (10, 0):
                    direction = (-10, 0)
                elif event.key == pygame.K_RIGHT and direction != (-10, 0):
                    direction = (10, 0)
                elif event.key == pygame.K_s:
                    save_checkpoint()
                elif event.key == pygame.K_l:
                    load_checkpoint()


        # Mover la serpiente
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, head)
        print(head[0], head[1])

        # Comprobar si la serpiente ha colisionado con la fruta
        if head == fruit:
            score += 1
            fruit = (random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10)
        elif head[0] > WIDTH or head[0] < 0 or head[1] > HEIGHT or head[1] < 0 or head in snake[1:]:
            print("¡Has perdido!")
            print(f"Puntuación final: {score}")
            pygame.quit()
            sys.exit()
        else:
            snake.pop()

        # Dibujar en la pantalla
        window.fill(BLACK)
        draw_snake()
        draw_fruit()
        pygame.display.flip()
        pygame.time.Clock().tick(15)

def save_checkpoint():
    try:
        with open('checkpoint.pkl', 'wb') as file:
            data = { 'score': score, 'snake': snake, 'direction': direction, 'fruit': fruit}
            pickle.dump(data, file)
        print("Checkpoint guardada con éxito.")
    except Exception as e:
        print(f"Error al guardar el checkpoint: {e}")

def load_checkpoint():
    try:
        with open('checkpoint.pkl', 'rb') as file:
            global score, snake, direction, fruit
            data = pickle.load(file)
            score = data['score']
            snake = data['snake']
            direction = data['direction']
            fruit = data['fruit']
    except FileNotFoundError:
        print("No hay una partida guardada.")
    except Exception as e:
        print(f"Error al cargar la partida: {e}")

# Iniciar el juego
game()
