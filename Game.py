#!/usr/bin/python3
import random
import time

random.seed(time.time())

class Game:

    def __init__(self):
        self.GOAL_VALUE = 2048
        self.TILE_SIZE = 4
        self.ACTIONS = {
            'w': lambda: self.__up(),
            's': lambda: self.__down(),
            'a': lambda: self.__left(),
            'd': lambda: self.__right(),
        }

        self.__init()

    def start(self):
        while True:
            self.__generate()
            self.__show_tiles()

            if self.__lose_check():
                return False

            act = input()
            while act not in self.ACTIONS:
                act = input()

            self.ACTIONS[act]()

            if self.__win_check():
                self.__show_tiles()
                return True

    def __init(self):
        self.tiles = []
        self.empty_tiles = []
        self.is_change = True

        for i in range(0, self.TILE_SIZE):
            self.tiles.append([1] * self.TILE_SIZE)
            for j in range (0, self.TILE_SIZE):
                self.empty_tiles.append((i, j))

    def __generate(self):
        if self.is_change:
            self.is_change = False
            i = random.randrange(0, len(self.empty_tiles))
            i1, i2 = self.empty_tiles.pop(i)
            self.tiles[i1][i2] = self.tiles[i1][i2] << 1

    def __show_tiles(self):
        for i in range(0, self.TILE_SIZE):
            print("[", end = "")
            for j in range(0, self.TILE_SIZE):
                if self.tiles[i][j] == 1:
                    print("    ", end = "")
                else:
                    print("%4d" % self.tiles[i][j], end = "")
                if j != self.TILE_SIZE-1:
                    print(", ", end = "")
            print("]")
            
    def __win_check(self):
        for i in range(0, self.TILE_SIZE):
            for j in range(0, self.TILE_SIZE):
                if self.tiles[i][j] == self.GOAL_VALUE:
                    return True
        return False

    def __lose_check(self):
        # still have empty tiles
        if len(self.empty_tiles) != 0:
            return False
        for i in range(0, self.TILE_SIZE):
            for j in range(0, self.TILE_SIZE):
                if i + 1 < self.TILE_SIZE and self.tiles[i][j] == self.tiles[i+1][j] or j + 1 < self.TILE_SIZE and self.tiles[i][j] == self.tiles[i][j+1]:
                    return False
        return True

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
                            self.tiles[i][j] = self.tiles[i][j] << 1
                            self.tiles[s][j] = 1
                            self.is_change = True
                            self.empty_tiles.append((s,j))
                        break
                    # tiles move
                    s = i
                    while s > 0 and self.tiles[s-1][j] == 1:
                        s = s - 1
                    if s != i:
                        self.tiles[i][j], self.tiles[s][j] = self.tiles[s][j], self.tiles[i][j]
                        self.is_change = True
                        self.empty_tiles.append((i,j))
                        self.empty_tiles.remove((s,j))

    def __down(self):
        for i in range(self.TILE_SIZE-1, -1, -1):
            for j in range(0, self.TILE_SIZE):
                if self.tiles[i][j] > 1: 
                    # tiles combine
                    s = i - 1
                    while s >= 0:
                        if self.tiles[s][j] == 1:
                            s = s - 1
                            continue
                        if self.tiles[i][j] == self.tiles[s][j]:
                            self.tiles[i][j] = self.tiles[i][j] << 1
                            self.tiles[s][j] = 1
                            self.is_change = True
                            self.empty_tiles.append((s,j))
                        break
                    # tiles move
                    s = i
                    while s < self.TILE_SIZE-1 and self.tiles[s+1][j] == 1:
                        s = s + 1
                    if s != i:
                        self.tiles[i][j], self.tiles[s][j] = self.tiles[s][j], self.tiles[i][j]
                        self.is_change = True
                        self.empty_tiles.append((i,j))
                        self.empty_tiles.remove((s,j))

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
                            self.tiles[j][i] = self.tiles[j][i] << 1
                            self.tiles[j][s] = 1
                            self.is_change = True
                            self.empty_tiles.append((j,s))
                        break
                    # tiles move
                    s = i 
                    while s > 0 and self.tiles[j][s-1] == 1:
                        s = s - 1
                    if s != i:
                        self.tiles[j][s], self.tiles[j][i] = self.tiles[j][i], self.tiles[j][s]
                        self.is_change = True
                        self.empty_tiles.append((j,i))
                        self.empty_tiles.remove((j,s))

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
                            self.tiles[j][i] = self.tiles[j][i] << 1
                            self.tiles[j][s] = 1
                            self.is_change = True
                            self.empty_tiles.append((j,s))
                        break
                    # tiles move
                    s = i 
                    while s < self.TILE_SIZE-1 and self.tiles[j][s+1] == 1:
                        s = s + 1
                    if s != i:
                        self.tiles[j][s], self.tiles[j][i] = self.tiles[j][i], self.tiles[j][s]
                        self.is_change = True
                        self.empty_tiles.append((j,i))
                        self.empty_tiles.remove((j,s))

if __name__ == '__main__':
    result = Game().start()
    print("You %s" % ("win" if result else "lose"))

