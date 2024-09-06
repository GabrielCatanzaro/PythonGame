import pygame
import random
import sys
import time

# Configurações iniciais
pygame.init()
mainClock = pygame.time.Clock()
WINDOWWIDTH = 800
WINDOWHEIGHT = 800
GRIDWIDTH = 20  # Número de colunas do labirinto
GRIDHEIGHT = 20  # Número de linhas do labirinto
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Labirinto e Pontuação')

# Cores
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Variáveis de movimento
moveLeft = False
moveRight = False
moveUp = False
moveDown = False
MOVESPEED = 6
score = 0
growth_count = 0
MAX_GROWTH_COUNT = 10
start_time = time.time()
CELLSIZE_X = WINDOWWIDTH // GRIDWIDTH
CELLSIZE_Y = WINDOWHEIGHT // GRIDHEIGHT

# Função para criar e desenhar o labirinto
def create_labyrinth():
    # Labirinto baseado em matriz
    labyrinth = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1],
        [0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
    ]
    return [labyrinth]

# Função para desenhar o labirinto na tela
def draw_labyrinth(labyrinths):
    # Calcula o tamanho das células
    cell_size_x = WINDOWWIDTH // len(labyrinths[0][0])
    cell_size_y = WINDOWHEIGHT // len(labyrinths[0])

    # Desenha o labirinto
    for idx, labyrinth in enumerate(labyrinths):
        start_x = (WINDOWWIDTH // 2) * (idx % 2)
        start_y = (WINDOWHEIGHT // 2) * (idx // 2)

        for row in range(len(labyrinth)):
            for col in range(len(labyrinth[row])):
                if labyrinth[row][col] == 1:
                    pygame.draw.rect(windowSurface, BLACK,
                                     pygame.Rect(start_x + col * cell_size_x,
                                                 start_y + row * cell_size_y,
                                                 cell_size_x, cell_size_y))
                elif labyrinth[row][col] == 0:
                    pygame.draw.rect(windowSurface, WHITE,
                                     pygame.Rect(start_x + col * cell_size_x,
                                                 start_y + row * cell_size_y,
                                                 cell_size_x, cell_size_y))

# Inicialização dos elementos
labyrinths = create_labyrinth()
FOODSIZE = 10
player = pygame.Rect(380, 380, 20, 20)  # Posição inicial fixa para o jogador
foods = []

# Função para gerar comida
def generate_food():
    while True:
        new_food = pygame.Rect(random.randint(0, GRIDWIDTH - 1) * CELLSIZE_X,
                               random.randint(0, GRIDHEIGHT - 1) * CELLSIZE_Y, FOODSIZE, FOODSIZE)
        row = new_food.y // CELLSIZE_Y
        col = new_food.x // CELLSIZE_X
        if labyrinths[0][row][col] == 0:
            foods.append(new_food)
            break

# Gera 20 comidas inicialmente
for _ in range(20):
    generate_food()

exit_rect = pygame.Rect(WINDOWWIDTH - 50, WINDOWHEIGHT // 2 - 25, 50, 50)  # Saída do labirinto

# Inicialização da variável foodCounter
foodCounter = 0
NEWFOOD = 100  # Intervalo para gerar nova comida (em iterações do loop principal)

# Loop principal do jogo
running = True
while running:
    # Processamento de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                moveRight = False
                moveLeft = True
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                moveLeft = False
                moveRight = True
            if event.key in (pygame.K_UP, pygame.K_w):
                moveDown = False
                moveUp = True
            if event.key in (pygame.K_DOWN, pygame.K_s):
                moveUp = False
                moveDown = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key in (pygame.K_LEFT, pygame.K_a):
                moveLeft = False
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                moveRight = False
            if event.key in (pygame.K_UP, pygame.K_w):
                moveUp = False
            if event.key in (pygame.K_DOWN, pygame.K_s):
                moveDown = False
            if event.key == pygame.K_x:
                player.topleft = (50, 50)  # Reinicia o jogador para a posição inicial
        if event.type == pygame.MOUSEBUTTONUP:
            foods.append(pygame.Rect(event.pos[0], event.pos[1], FOODSIZE, FOODSIZE))

    if moveDown:
        next_rect = player.copy()
        next_rect.top += MOVESPEED
        if all(labyrinths[0][row][col] == 0 for row in range(len(labyrinths[0])) for col in
               range(len(labyrinths[0][0]))
               if next_rect.colliderect(pygame.Rect(col * CELLSIZE_X, row * CELLSIZE_Y, CELLSIZE_X, CELLSIZE_Y))):
            player.top += MOVESPEED
    if moveUp:
        next_rect = player.copy()
        next_rect.top -= MOVESPEED
        if all(labyrinths[0][row][col] == 0 for row in range(len(labyrinths[0])) for col in
               range(len(labyrinths[0][0]))
               if next_rect.colliderect(pygame.Rect(col * CELLSIZE_X, row * CELLSIZE_Y, CELLSIZE_X, CELLSIZE_Y))):
            player.top -= MOVESPEED
    if moveLeft:
        next_rect = player.copy()
        next_rect.left -= MOVESPEED
        if all(labyrinths[0][row][col] == 0 for row in range(len(labyrinths[0])) for col in
               range(len(labyrinths[0][0]))
               if next_rect.colliderect(pygame.Rect(col * CELLSIZE_X, row * CELLSIZE_Y, CELLSIZE_X, CELLSIZE_Y))):
            player.left -= MOVESPEED
    if moveRight:
        next_rect = player.copy()
        next_rect.left += MOVESPEED
        if all(labyrinths[0][row][col] == 0 for row in range(len(labyrinths[0])) for col in
               range(len(labyrinths[0][0]))
               if next_rect.colliderect(pygame.Rect(col * CELLSIZE_X, row * CELLSIZE_Y, CELLSIZE_X, CELLSIZE_Y))):
            player.left += MOVESPEED

    # Verificação de envolvimento (wrap around)
    if player.left > WINDOWWIDTH:
        player.left = 0
    elif player.right < 0:
        player.left = WINDOWWIDTH - player.width
    if player.top > WINDOWHEIGHT:
        player.top = 0
    elif player.bottom < 0:
        player.top = WINDOWHEIGHT - player.height

    # Desenha o fundo
    windowSurface.fill(WHITE)

    # Desenha os labirintos
    draw_labyrinth(labyrinths)

    # Desenha o jogador
    pygame.draw.rect(windowSurface, RED, player)

    # Atualiza foodCounter
    foodCounter += 1
    pheight = 0
    # Verifica colisão com comida
    for food in foods:
        if player.colliderect(food):
            foods.remove(food)
            score += 1
            # Aumenta o tamanho do jogador em 1%
            if growth_count < MAX_GROWTH_COUNT:
                player.inflate_ip (player.width * 0.05, player.height * 0.05)
                growth_count += 1

    # Verifica colisão com comida e gera nova comida se necessário
    if foodCounter >= NEWFOOD:
        foodCounter = 0
        generate_food()

    # Desenha comidas na tela
    for food in foods:
        pygame.draw.rect(windowSurface, GREEN, food)

    # Desenha a saída
    pygame.draw.rect(windowSurface, BLUE, exit_rect)

    # Verifica se o jogador chegou na saída
    if player.colliderect(exit_rect):
        end_time = time.time()
        time_taken = end_time - start_time
        windowSurface.fill(WHITE)
        font = pygame.font.SysFont(None, 48)
        text_surf = font.render(f'Parabéns! Tempo: {time_taken:.2f} s, Pontuação: {score}', True, BLACK)
        text_rect = text_surf.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2))
        windowSurface.blit(text_surf, text_rect)
        pygame.display.update()
        pygame.time.wait(5000)
        pygame.quit()
        sys.exit()

    # Exibe pontuação
    font = pygame.font.SysFont(None, 36)
    score_surf = font.render(f'Score: {score}', True, GREEN)
    windowSurface.blit(score_surf, (10, 10))

    # Atualiza a tela
    pygame.display.update()
    mainClock.tick(40)

    # Exibe a pontuação no terminal
    print(f'Score: {score}')