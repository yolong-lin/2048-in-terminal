#!/usr/bin/python3
import curses, random, time
from curses import wrapper

random.seed(time.time())

class Tile:
    WIDTH  = 8
    HEIGHT = 3

    def __init__(self, game, i, j):
        self.game = game
        self.i = i
        self.j = j
        self.val = 1

    def position(self, y, x):
        self.y = y
        self.x = x

    def reset(self):
        self.game.empty_tiles.append(self)
        self.val = 1

    def shift(self):
        self.val = self.val << 1
        self.game.is_change = True

    def getij(self):
        return (self.i, self.j)

    def refresh(self):
        if self.val != 1:
            self.game.stdcsr.addstr(self.y, self.x + self.WIDTH // 2 - 4 // 2, "%4d" % self.val)
        else:
            # Clear the previous number
            self.game.stdcsr.addstr(self.y, self.x + self.WIDTH // 2 - 4 // 2, " " * 4)

    def swap(self, other):
        if self.val == other.val:
            return
        self.val, other.val = other.val, self.val
        self.game.is_change = True
        if self.val == 1:
            self.game.empty_tiles.append(self)
            self.game.empty_tiles.remove(other)
        else:
            self.game.empty_tiles.append(other)
            self.game.empty_tiles.remove(self)

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
                tile = Tile(self, i, j)
                row.append(tile)
                self.empty_tiles.append(tile)
            self.tiles.append(row)

    def start(self):
        return wrapper(self.__start)

    def __start(self, stdcsr):
        curses.curs_set(0)
        self.stdcsr = stdcsr
        self.__draw()

        self.__generate()
        self.is_change = True
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
        if self.is_change and len(self.empty_tiles) > 0:
            i = random.randrange(0, len(self.empty_tiles))
            i, j = self.empty_tiles.pop(i).getij()
            for _ in range(random.randrange(1, 3)):
                self.tiles[i][j].shift()
            self.is_change = False

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
                self.tiles[i][j].refresh()
                tx = tx + Tile.WIDTH

    def __refresh(self):
        for i in range(0, self.TILE_SIZE):
            for j in range(0, self.TILE_SIZE):
                self.tiles[i][j].refresh()

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
        for i in range(self.TILE_SIZE):
            base = 0
            for j in range(self.TILE_SIZE):
                if j == 0:
                    k = j if self.tiles[j][i] == 1 else j + 1
                elif self.tiles[j][i] != 1:
                    if k != 0 and self.tiles[k-1][i] == self.tiles[j][i] and k > base:
                        self.tiles[k-1][i].shift()
                        self.tiles[j][i].reset()
                        base = k
                    else:
                        self.tiles[k][i].swap(self.tiles[j][i])
                        k = k + 1

    def __down(self):
        for i in range(self.TILE_SIZE):
            base = self.TILE_SIZE - 1
            for j in range(self.TILE_SIZE-1, -1, -1):
                if j == self.TILE_SIZE-1:
                    k = j if self.tiles[j][i] == 1 else j - 1
                elif self.tiles[j][i] != 1:
                    if k != self.TILE_SIZE - 1 and self.tiles[k+1][i] == self.tiles[j][i] and k < base:
                        self.tiles[k+1][i].shift()
                        self.tiles[j][i].reset()
                        base = k
                    else:
                        self.tiles[k][i].swap(self.tiles[j][i])
                        k = k - 1

    def __left(self):
        for i in range(self.TILE_SIZE):
            base = 0
            for j in range(self.TILE_SIZE):
                if j == 0:
                    k = j if self.tiles[i][j] == 1 else j + 1
                elif self.tiles[i][j] != 1:
                    if k != 0 and self.tiles[i][k-1] == self.tiles[i][j] and k > base:
                        self.tiles[i][k-1].shift()
                        self.tiles[i][j].reset()
                        base = k
                    else:
                        self.tiles[i][k].swap(self.tiles[i][j])
                        k = k + 1

    def __right(self):
        for i in range(self.TILE_SIZE):
            base = self.TILE_SIZE - 1
            for j in range(self.TILE_SIZE-1, -1, -1):
                if j == self.TILE_SIZE-1:
                    k = j if self.tiles[i][j] == 1 else j - 1
                elif self.tiles[i][j] != 1:
                    if k != self.TILE_SIZE - 1 and self.tiles[i][k+1] == self.tiles[i][j] and k < base:
                        self.tiles[i][k+1].shift()
                        self.tiles[i][j].reset()
                        base = k
                    else:
                        self.tiles[i][k].swap(self.tiles[i][j])
                        k = k - 1

if __name__ == '__main__':
    Game().start()

