import pygame, random, time, button

pygame.init()
pygame.font.init()

OFFSET = 50
WIDTH = 900
HEIGHT = WIDTH + OFFSET
win = pygame.display.set_mode((WIDTH, HEIGHT))

MODS = [
    [-1,-1],
    [-1,0],
    [-1,1],
    [0,-1],
    [0,0],
    [0,1],
    [1,-1],
    [1,0],
    [1,1]
]


class Grid:
    def __init__(self, diff):
        self.diff = diff
        if diff == 0:
            self.size = 10, 10
            self.bombs = 10
        elif diff == 1:
            self.size = 18, 18
            self.bombs = 40
        else:
            self.size = 25, 25
            self.bombs = 99
        self.bombs_list = []

        self.offset = OFFSET

        self.grid = [[Square(i, j, "dark" if (i + j) % 2 else "light") for j in range(self.size[1])] for i in
                     range(self.size[0])]
        self.cube_width, self.cube_height = WIDTH // self.size[0], WIDTH // self.size[1]

    def assign_bombs(self, firstPos):
        for bomb in range(self.bombs):
            square = random.randint(0, self.size[0] - 1), random.randint(0, self.size[1] - 1)
            invalid = True
            while invalid:
                if self.grid[square[0]][square[1]].value == -1 or abs(self.grid[square[0]][square[1]].x - firstPos[0]) < 2\
                    or abs(self.grid[square[0]][square[1]].y - firstPos[1]) < 2:
                    square = random.randint(0, self.size[0] - 1), random.randint(0, self.size[1] - 1)
                else:
                    neighbours = 0
                    for neighbour in MODS:
                        p1 = square[0] + neighbour[0]
                        p2 = square[1] + neighbour[1]
                        if 0 <= p1 <= self.size[0] - 1 and 0 <= p2 <= self.size[1] - 1:
                            if self.grid[p1][p2].value == -1: neighbours += 1
                    if neighbours > 3: invalid = True
                    else: invalid = False
            else:
                self.grid[square[0]][square[1]].value = -1
                self.bombs_list.append(self.grid[square[0]][square[1]])

        for bomb in self.bombs_list:
            for neighbour in MODS:
                p1 = bomb.x + neighbour[0]
                p2 = bomb.y + neighbour[1]
                if 0 <= p1 <= self.size[0] - 1 and 0 <= p2 <= self.size[1] - 1:
                    if self.grid[p1][p2].value is None: self.grid[p1][p2].value = "1"
                    elif self.grid[p1][p2].value != -1: self.grid[p1][p2].value = str(int(self.grid[p1][p2].value) + 1)

    def draw(self):
        for j in range(self.size[1]):
            for i in range(self.size[0]):
                square = self.grid[i][j]
                cur = square.x * self.cube_width, square.y * self.cube_height + self.offset
                if not square.revealed:
                    pygame.draw.rect(win, square.col, (cur[0], cur[1], self.cube_width, self.cube_height))
                else:
                    half_cube_x = self.cube_width // 2
                    half_cube_y = self.cube_height // 2
                    pygame.draw.rect(win, square.revealed_col, (cur[0], cur[1], self.cube_width, self.cube_height))
                    if square.value == -1:
                        pygame.draw.rect(win, square.bomb_col, (cur[0], cur[1], self.cube_width, self.cube_height))
                        pygame.draw.circle(win, (40, 40, 40),
                                           (cur[0] + half_cube_x, cur[1] + half_cube_y),
                                           min(self.cube_width // 4, self.cube_height // 4))
                    elif square.value is not None:
                        font = pygame.font.SysFont("", round(self.cube_width*1.5))
                        if int(square.value) % 3 == 1 or int(square.value) == 1: col = (0,0,255-(int(square.value) // 3)*100)
                        elif int(square.value) % 3 == 2: col = (0,255-(int(square.value) // 3)*100,0)
                        else: col = (255-(int(square.value) // 3)*100,0,0)
                        text = font.render(str(square.value), False, col)
                        win.blit(text, (cur[0]+self.cube_width*0.23, cur[1]+self.cube_height*0.05))


class Square:
    def __init__(self, x, y, col):
        self.x = x
        self.y = y
        self.value = None
        if col == "dark":
            self.hidden_col = (252, 186, 3)
            self.revealed_col = (201, 201, 201)
            self.revealed_highlight_col = (255, 255, 255)
            self.hidden_highlight_col = (255, 200, 30)
        else:
            self.hidden_col = (235, 172, 47)
            self.revealed_col = (156, 156, 156)
            self.revealed_highlight_col = (180, 180, 180)
            self.hidden_highlight_col = (255, 190, 70)
        self.col = self.hidden_col
        self.revealed = False
        self.bomb_col = (random.randint(50, 254), random.randint(50, 254), random.randint(50, 254))


def game_win(grid):
    for i in range(grid.size[0]):
        for j in range(grid.size[1]):
            if grid.grid[i][j].value == -1: grid.grid[i][j].col = (0,0,0)
            grid.draw()
            pygame.display.update()
    time.sleep(0.5)
    for i in range(grid.size[0]):
        for j in range(grid.size[1]):
            grid.grid[j][i].col = (255,255,255)
            time.sleep(0.01)
            grid.draw()
            pygame.display.update()
    for i in range(grid.size[0]):
        for j in range(grid.size[1]):
            grid.grid[j][i].col = (0,0,0)
            time.sleep(0.01)
            grid.draw()
            pygame.display.update()

def check_win(grid):
    win = True
    for i in range(grid.size[0]):
        for j in range(grid.size[1]):
            if grid.grid[i][j].value != -1 and not grid.grid[i][j].revealed: win = False

    if win:
        print("hi")
        game_win(grid)
        return True



def game_over(grid, first):
    bombs = []
    for i in range(grid.size[0]):
        for j in range(grid.size[1]):
            if grid.grid[i][j].value == -1: bombs.append((i, j))

    grid.grid[first[0]][first[1]].revealed = True
    grid.draw()
    pygame.display.update()

    random.shuffle(bombs)
    for bomb in bombs:
        time.sleep(random.randint(1, 10) / 200)
        grid.grid[bomb[0]][bomb[1]].revealed = True
        grid.draw()
        pygame.display.update()


def clear_area(grid,pos):
    for neighbour in MODS:
        p1 = pos[0] + neighbour[0]
        p2 = pos[1] + neighbour[1]
        if 0 <= p1 <= grid.size[0] - 1 and 0 <= p2 <= grid.size[1] - 1:
            if grid.grid[p1][p2].value is None and not grid.grid[p1][p2].revealed:
                grid.grid[p1][p2].revealed = True
                clear_area(grid,(p1,p2))
            elif grid.grid[p1][p2].value is not None and grid.grid[pos[0]][pos[1]].value is None and not grid.grid[p1][p2].revealed and grid.grid[p1][p2].value != -1:
                grid.grid[p1][p2].revealed = True
        else: pass
    return


def hovering(grid, prev):
    mouseX, mouseY = pygame.mouse.get_pos()
    squareX, squareY = mouseX // grid.cube_width, (mouseY - grid.offset) // grid.cube_height
    if mouseY > grid.offset:
        if prev is not None:
            if not prev.revealed:
                prev.col = prev.hidden_col
            else:
                prev.col = prev.revealed_col
        if not grid.grid[squareX][squareY].revealed:
            grid.grid[squareX][squareY].col = grid.grid[squareX][squareY].hidden_highlight_col
        else:
            grid.grid[squareX][squareY].col = grid.grid[squareX][squareY].revealed_highlight_col
    return grid.grid[squareX][squareY]


def clicked(grid):
    mouseX, mouseY = pygame.mouse.get_pos()
    squareX, squareY = mouseX // grid.cube_width, (mouseY - grid.offset) // grid.cube_height
    if not grid.grid[squareX][squareY].revealed:
        if grid.grid[squareX][squareY].value == -1:
            game_over(grid, (squareX, squareY))
            return False
        else:
            grid.grid[squareX][squareY].revealed = True
    else:
        pass
    return True


def redraw_window(grid,list1):
    win.fill((0, 0, 255))
    grid.draw()
    list1.draw(win)


def main():
    clock = pygame.time.Clock()
    d = 0
    grid = Grid(d)

    list1 = button.OptionBox(
        40, 5, 160, 40, (150, 150, 150), (100, 200, 255), pygame.font.SysFont("", 30),
        ["option 1", "2nd option", "another option"])

    prev = None
    first_click = True
    run = True
    while run:
        clock.tick(60)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: pygame.quit()
                elif event.key == pygame.K_r:
                    grid = Grid(d)
                    first_click = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                squareX, squareY = mouseX // grid.cube_width, (mouseY - grid.offset) // grid.cube_height
                if
                    if mouseY > grid.offset:
                        if first_click: grid.assign_bombs((squareX,squareY))

                        if first_click or grid.grid[squareX][squareY].value is None: clear_area(grid,(squareX,squareY))
                        if not clicked(grid): run = False
                        first_click = False

        list1.update(events)
        if check_win(grid): run = False
        prev = hovering(grid, prev)

        redraw_window(grid,list1)
        pygame.display.update()


if __name__ == "__main__":
    while True:
        main()
