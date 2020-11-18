#!/usr/bin/python3
import random, time

random.seed(time.time())

GOAL_VALUE = 2048
TILE_SIZE = 4

is_change = True

tiles = []
# empty tiles
et = []

def init():
    for i in range(0, TILE_SIZE):
        tiles.append([1] * TILE_SIZE)
        for j in range(0, TILE_SIZE):
            et.append((i, j))

def generate():
    global is_change
    if is_change:
        is_change = False
        idx = random.randrange(0,len(et))
        idx1, idx2 = et.pop(idx)
        tiles[idx1][idx2] = tiles[idx1][idx2] << 1

def up():
    global is_change
    for i in range(0, TILE_SIZE):
        for j in range(0, TILE_SIZE):
            if tiles[i][j] > 1:
                # tiles combine
                s = i + 1
                while (s < TILE_SIZE):
                    if tiles[s][j] == 1:
                        s = s + 1
                        continue
                    if tiles[i][j] == tiles[s][j]:
                        tiles[i][j] = tiles[i][j] << 1
                        tiles[s][j] = 1
                        is_change = True
                        et.append((s,j))
                    break
                # tiles move
                s = i
                while s > 0 and tiles[s-1][j] == 1:
                    s = s - 1
                if s != i:
                    tiles[i][j], tiles[s][j] = tiles[s][j], tiles[i][j]
                    is_change = True
                    et.append((i,j))
                    et.remove((s,j))

def down():
    global is_change
    for i in range(TILE_SIZE-1, -1, -1):
        for j in range(0, TILE_SIZE):
            if tiles[i][j] > 1: 
                # tiles combine
                s = i - 1
                while s >= 0:
                    if tiles[s][j] == 1:
                        s = s - 1
                        continue
                    if tiles[i][j] == tiles[s][j]:
                        tiles[i][j] = tiles[i][j] << 1
                        tiles[s][j] = 1
                        is_change = True
                        et.append((s,j))
                    break
                # tiles move
                s = i
                while s < TILE_SIZE-1 and tiles[s+1][j] == 1:
                    s = s + 1
                if s != i:
                    tiles[i][j], tiles[s][j] = tiles[s][j], tiles[i][j]
                    is_change = True
                    et.append((i,j))
                    et.remove((s,j))

def left():
    global is_change
    for i in range(0, TILE_SIZE):
        for j in range(0, TILE_SIZE):
            if tiles[j][i] > 1: 
                # tiles combine
                s = i + 1
                while s < TILE_SIZE:
                    if tiles[j][s] == 1:
                        s = s + 1
                        continue
                    if tiles[j][i] == tiles[j][s]:
                        tiles[j][i] = tiles[j][i] << 1
                        tiles[j][s] = 1
                        is_change = True
                        et.append((j,s))
                    break
                # tiles move
                s = i 
                while s > 0 and tiles[j][s-1] == 1:
                    s = s - 1
                if s != i:
                    tiles[j][s], tiles[j][i] = tiles[j][i], tiles[j][s]
                    is_change = True
                    et.append((j,i))
                    et.remove((j,s))

def right():
    global is_change
    for i in range(TILE_SIZE-1, -1, -1):
        for j in range(0, TILE_SIZE):
            if tiles[j][i] > 1:
                # tiles combine
                s = i - 1
                while s >= 0:
                    if tiles[j][s] == 1:
                        s = s - 1
                        continue
                    if tiles[j][i] == tiles[j][s]:
                        tiles[j][i] = tiles[j][i] << 1
                        tiles[j][s] = 1
                        is_change = True
                        et.append((j,s))
                    break
                # tiles move
                s = i 
                while s < TILE_SIZE-1 and tiles[j][s+1] == 1:
                    s = s + 1
                if s != i:
                    tiles[j][s], tiles[j][i] = tiles[j][i], tiles[j][s]
                    is_change = True
                    et.append((j,i))
                    et.remove((j,s))

actions = {
    'w': lambda: up(),
    's': lambda: down(),
    'a': lambda: left(),
    'd': lambda: right(),
}

def win_check():
    for i in range(0, TILE_SIZE):
        for j in range(0, TILE_SIZE):
            if tiles[i][j] == GOAL_VALUE:
                return True
    return False

def lose_check():
    # still have empty tiles
    if len(et) != 0:
        return False
    # check right and down if value is the same
    for i in range(0, TILE_SIZE-1):
        for j in range(0, TILE_SIZE-1):
            if tiles[i][j] == tiles[i+1][j] or tiles[i][j] == tiles[i][j+1]:
                return False
    return True

def show_tiles():
    for i in range(0,TILE_SIZE):
        print("[", end="")
        for j in range(0,TILE_SIZE):
            if tiles[i][j] == 1:
                print("    ", end = "")
            else:
                print("%4d" % tiles[i][j], end="")
            if j != TILE_SIZE-1:
                print(", ", end="")
        print("]")

if __name__ == '__main__':
    init()
    while True:
        generate()
        show_tiles()

        act = input("Up(w) Down(s) Left(a) Right(d): ")
        while (act not in actions):
            act = input("Up(w) Down(s) Left(a) Right(d): ")

        actions[act]()
        
        if win_check():
            print("You win~")
            show_tiles()
            break

        if lose_check():
            print("You lose~")
            break

