import pygame
from grid import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREY = (192, 192, 192)
SIZE = 20
GAP = 2
DIM = 30
MIN_P = 0.2


"""def grid_list(grid):
    small_grid = []
    for i in range(grid.dim):
        for j in range(grid.dim):
            small_grid.append(grid.get_cell(i, j))
    result = []
    for i in range(len(small_grid)):
        if small_grid[i].isCovered is True and small_grid[i].isFlag is False:
            result.append(11)
        elif small_grid[i].isFlag:
            result.append(9)
        elif small_grid[i].isCovered is False and small_grid[i].isMine is True:
            result.append(12)
        else:
            result.append(small_grid[i].numOfMines)
    return result


def draw_initial_grid(result, dim):
    pygame.init()
    width = SIZE * dim + (dim + 1) * GAP
    height = SIZE * dim + (dim + 1) * GAP
    surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption("MineSweeper")
    exit_flag = True
    while exit_flag:
        surface.fill(BLACK)
        for i in range(dim):
            for j in range(dim):
                if result[i * dim + j] == 11:
                    pygame.draw.rect(surface, GREY, [(GAP + SIZE) * j + GAP, (GAP + SIZE) * i + GAP, SIZE, SIZE])

                elif result[i * dim + j] == 9:
                    pygame.draw.rect(surface, RED, [(GAP + SIZE) * j + GAP, (GAP + SIZE) * i + GAP, SIZE, SIZE])

                elif result[i * dim + j] == 10:
                    pygame.draw.rect(surface, WHITE, [(GAP + SIZE) * j + GAP, (GAP + SIZE) * i + GAP, SIZE, SIZE])
                    number = pygame.font.SysFont('宋体', 20)
                    number_surface = number.render('F', True, BLACK)
                    number_rect = number_surface.get_rect()
                    number_rect.center = ((GAP + SIZE) * j + GAP + SIZE / 2, (GAP + SIZE) * i + GAP + SIZE / 2)
                    surface.blit(number_surface, number_rect)

                elif result[i * dim + j] == 0:
                    pygame.draw.rect(surface, WHITE, [(GAP + SIZE) * j + GAP, (GAP + SIZE) * i + GAP, SIZE, SIZE])

                elif result[i * dim + j] == 12:
                    pygame.draw.rect(surface, BLACK, [(GAP + SIZE) * j + GAP, (GAP + SIZE) * i + GAP, SIZE, SIZE])

                else:
                    pygame.draw.rect(surface, WHITE, [(GAP + SIZE) * j + GAP, (GAP + SIZE) * i + GAP, SIZE, SIZE])
                    number = pygame.font.SysFont('宋体', 20)
                    number_surface = number.render(str(result[i * dim + j]), True, BLACK)
                    number_rect = number_surface.get_rect()
                    number_rect.center = ((GAP + SIZE) * j + GAP + SIZE / 2, (GAP + SIZE) * i + GAP + SIZE / 2)
                    surface.blit(number_surface, number_rect)

        pygame.display.flip()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit_flag = False
"""

if __name__ == '__main__':
    # test_grid = create_grid(DIM, MIN_P)
    test_grid = Grid(DIM, 400)
    for ii in range(0, DIM):
        for jj in range(0, DIM):
            print(test_grid.uncover_grid(ii, jj), end=" ")
        print()
    # test_grid = grid_list(test_grid)
    # draw_initial_grid(test_grid, DIM)
