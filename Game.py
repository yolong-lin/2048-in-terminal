#!/usr/bin/python3
import curses, random, time
from curses import wrapper

random.seed(time.time())

class Tile:
    WIDTH  = 8
    HEIGHT = 3

    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.val = 1

    def position(self, y, x):
        self.y = y
        self.x = x

    def reset(self):
        self.val = 1

    def shift(self):
        self.val = self.val << 1

    def getij(self):
        return (self.i, self.j)

    def refresh(self, stdcsr):
        if self.val != 1:
            stdcsr.addstr(self.y, self.x + self.WIDTH // 2 - 4 // 2, "%4d" % self.val)
        else:
            # Clear the previous number
            stdcsr.addstr(self.y, self.x + self.WIDTH // 2 - 4 // 2, " " * 4)

    def swap(self, tile):
        self.val, tile.val = tile.val, self.val

    def __eq__(self, other):
        if isinstance(other, int):
            return self.val == other
        if isinstance(other, Tile):
            return self.val == other.val

    def __ne__(self, other):
        if isinstance(other, int):
            return self.val != other
        if isinstance(other, Tile):
            return self.val != other.val

    def __lt__(self, other):
        if isinstance(other, int):
            return self.val < other
        if isinstance(other, Tile):
            return self.val < other.val

    def __le__(self, other):
        if isinstance(other, int):
            return self.val <= other
        if isinstance(other, Tile):
            return self.val <= other.val

    def __gt__(self, other):
        if isinstance(other, int):
            return self.val > other
        if isinstance(other, Tile):
            return self.val > other.val

    def __ge__(self, other):
        if isinstance(other, int):
            return self.val >= other
        if isinstance(other, Tile):
            return self.val >= other.val


class Game:
    def __init__(self):
        self.GOAL_VALUE = 2048
        self.TILE_SIZE = 4

        self.width = Tile.WIDTH * self.TILE_SIZE + self.TILE_SIZE + 1
        self.height = Tile.HEIGHT * self.TILE_SIZE + self.TILE_SIZE + 1

        self.tiles = []
        self.empty_tiles = []
        self.is_change = True

        for i in range(0, self.TILE_SIZE):
            row = []
            for j in range (0, self.TILE_SIZE):
                tile = Tile(i, j)
                row.append(tile)
                self.empty_tiles.append(tile)
            self.tiles.append(row)

    def start(self):
        return wrapper(self.__start)

    def __start(self, stdcsr):
        curses.curs_set(0)
        self.stdcsr = stdcsr
        self.__draw()

        while 1:
            self.__generate()
            self.__refresh()
            
            if self.__lose_check():
                text = "You Lose"
                stdcsr.addstr(self.y - 2, self.x + self.width // 2 - len(text) // 2, text)
                stdcsr.getch()
                return False

            act_flag = True
            while act_flag:
                act = stdcsr.getch()
                if act == curses.KEY_UP:
                    self.__up()
                    act_flag = False
                elif act == curses.KEY_DOWN:
                    self.__down()
                    act_flag = False
                elif act == curses.KEY_LEFT:
                    self.__left()
                    act_flag = False
                elif act == curses.KEY_RIGHT:
                    self.__right()
                    act_flag = False
                elif act == curses.KEY_RESIZE:
                    self.__draw()
                elif act == ord('q'):
                    return
                else:
                    stdcsr.addstr(0, 0, str(act))
                    pass
            
            if self.__win_check():
                text = "You Win"
                self.__refresh()
                stdcsr.addstr(self.y - 2, self.x + self.width // 2 - len(text) // 2, text)
                stdcsr.getch()
                return True

    def __generate(self):
        if self.is_change:
            self.is_change = False
            i = random.randrange(0, len(self.empty_tiles))
            i, j = self.empty_tiles.pop(i).getij()
            self.tiles[i][j].shift()

    def __draw(self):
        """Resize and Refresh"""
        self.stdcsr.clear()
        self.y, self.x = self.stdcsr.getmaxyx()
        self.y = self.y // 2 - self.height // 2
        self.x = self.x // 2 - self.width // 2
        
        for i in range(self.TILE_SIZE):
            if i == 0:
                vborder = "+"
                hborder = "|"
            vborder = vborder + "-" * Tile.WIDTH + "+"
            hborder = hborder + " " * Tile.WIDTH + "|"

        for i in range(0, self.height):
            if i % (Tile.HEIGHT + 1) == 0:
                self.stdcsr.addstr(self.y + i, self.x, vborder)
            else:
                self.stdcsr.addstr(self.y + i, self.x, hborder)

        ty = self.y
        for i in range(0, self.TILE_SIZE):
            if i == 0:
                ty = ty + 1 + Tile.HEIGHT // 2
            else:
                ty = ty + Tile.HEIGHT + 1
            tx = self.x
            for j in range(0, self.TILE_SIZE):
                tx = tx + 1
                self.tiles[i][j].position(ty, tx)
                self.tiles[i][j].refresh(self.stdcsr)
                tx = tx + Tile.WIDTH
        

    def __refresh(self):
        for i in range(0, self.TILE_SIZE):
            for j in range(0, self.TILE_SIZE):
                self.tiles[i][j].refresh(self.stdcsr)

    def __lose_check(self):
        if len(self.empty_tiles) != 0:
            return False
        for i in range(0, self.TILE_SIZE):
            for j in range(0, self.TILE_SIZE):
                if ( i + 1 < self.TILE_SIZE and self.tiles[i][j] == self.tiles[i+1][j] or 
                     j + 1 < self.TILE_SIZE and self.tiles[i][j] == self.tiles[i][j+1] ):
                    return False
        return True

    def __win_check(self):
        for i in range(0, self.TILE_SIZE):
            for j in range(0, self.TILE_SIZE):
                if self.tiles[i][j] == self.GOAL_VALUE:
                    return True
        return False

    def __up(self):
        for i in range(0, self.TILE_SIZE):
            for j in range(0, self.TILE_SIZE):
                if self.tiles[i][j] > 1:
                    # tiles combine
                    s = i + 1
                    while s < self.TILE_SIZE:
                        if self.tiles[s][j] == 1:
                            s = s + 1
                            continue
                        if self.tiles[i][j] == self.tiles[s][j]:
                            self.tiles[i][j].shift()
                            self.tiles[s][j].reset()
                            self.is_change = True
                            self.empty_tiles.append(self.tiles[s][j])
                        break
                    # tiles move
                    s = i
                    while s > 0 and self.tiles[s-1][j] == 1:
                        s = s - 1
                    if s != i:
                        self.tiles[i][j].swap(self.tiles[s][j])
                        self.is_change = True
                        self.empty_tiles.append(self.tiles[i][j])
                        self.empty_tiles.remove(self.tiles[s][j])

    def __down(self):
        for i in range(self.TILE_SIZE-1, -1, -1):
            for j in range(0, self.TILE_SIZE):
                if self.tiles[i][j] > 1:
                    # tile combine
                    s = i - 1
                    while s >= 0:
                        if self.tiles[s][j] == 1:
                            s = s - 1
                            continue
                        if self.tiles[i][j] == self.tiles[s][j]:
                            self.tiles[i][j].shift()
                            self.tiles[s][j].reset()
                            self.is_change = True
                            self.empty_tiles.append(self.tiles[s][j])
                        break
                    # tile move
                    s = i
                    while s < self.TILE_SIZE-1 and self.tiles[s+1][j] == 1:
                        s = s + 1
                    if s != i:
                        self.tiles[i][j].swap(self.tiles[s][j])
                        self.is_change = True
                        self.empty_tiles.append(self.tiles[i][j])
                        self.empty_tiles.remove(self.tiles[s][j])

    def __left(self):
        for i in range(0, self.TILE_SIZE):
            for j in range(0, self.TILE_SIZE):
                if self.tiles[j][i] > 1: 
                    # tiles combine
                    s = i + 1
                    while s < self.TILE_SIZE:
                        if self.tiles[j][s] == 1:
                            s = s + 1
                            continue
                        if self.tiles[j][i] == self.tiles[j][s]:
                            self.tiles[j][i].shift()
                            self.tiles[j][s].reset()
                            self.is_change = True
                            self.empty_tiles.append(self.tiles[j][s])
                        break
                    # tiles move
                    s = i
                    while s > 0 and self.tiles[j][s-1] == 1:
                        s = s - 1
                    if s != i:
                        self.tiles[j][i].swap(self.tiles[j][s])
                        self.is_change = True
                        self.empty_tiles.append(self.tiles[j][i])
                        self.empty_tiles.remove(self.tiles[j][s])

    def __right(self):
        for i in range(self.TILE_SIZE-1, -1, -1):
            for j in range(0, self.TILE_SIZE):
                if self.tiles[j][i] > 1:
                    # tiles combine
                    s = i - 1
                    while s >= 0:
                        if self.tiles[j][s] == 1:
                            s = s - 1
                            continue
                        if self.tiles[j][i] == self.tiles[j][s]:
                            self.tiles[j][i].shift()
                            self.tiles[j][s].reset()
                            self.is_change = True
                            self.empty_tiles.append(self.tiles[j][s])
                        break
                    # tiles move
                    s = i 
                    while s < self.TILE_SIZE-1 and self.tiles[j][s+1] == 1:
                        s = s + 1
                    if s != i:
                        self.tiles[j][i].swap(self.tiles[j][s])
                        self.is_change = True
                        self.empty_tiles.append(self.tiles[j][i])
                        self.empty_tiles.remove(self.tiles[j][s])

if __name__ == '__main__':
    Game().start()

