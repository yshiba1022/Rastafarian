import pyxel
import time
import sys
import random

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

N_OF_STAGE = 8

BLUE_BALL = (1,0)
RED_BALL = (0,1)
GREEN_BALL = (1,1)
YELLOW_BALL = (0,2)

BLUE_BALL_OUT = (1,3)
RED_BALL_OUT = (0,3)
GREEN_BALL_OUT = (1,4)
YELLOW_BALL_OUT = (0,4)

SCREEN_TITLE  = 0
SCREEN_START  = 1
SCREEN_PAZZLE = 2
SCREEN_CLEAR  = 3
SCREEN_IMPOSSIBLE   = 4
SCREEN_ALL_CLEAR  = 5
SCREEN_SELECT = 6

scene = SCREEN_TITLE
stage = 0
timing = 0

# 主人公の Cherry の設定 
class Cherry:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = RIGHT
        self.pre_time = time.time()
        self.step = 0

class App:

    
    def __init__(self):
        pyxel.init(64, 64)

        pyxel.load("test.pyxres")

        self.cherry = Cherry(1, 1)
        pyxel.run(self.update, self.draw)

    # 進行方向に進むスペースがあるか
    # あれば True，なければ False
    def isSpaseToMove(self, xdiff, ydiff):
        global stage
        x = self.cherry.x + xdiff + 8*stage
        y = self.cherry.y + ydiff
        if (0,0)==pyxel.tilemap(1).pget(x, y):
            return True
        else:
            return False

    def Tell_impossible(self):
        global scene
        self.draw()
        time.sleep(0.5)
        scene = SCREEN_IMPOSSIBLE

    def RollStone(self, x, y, xdiff, ydiff):
        global stage
        global scene
        
        x  = x + xdiff
        y  = y + ydiff
        x2 = x + xdiff
        y2 = y + ydiff
        
        c = pyxel.tilemap(1).pget(x+8*stage, y)
        tile = pyxel.tilemap(1).pget(x2+8*stage, y2)
        if tile == (0,0):
            pyxel.tilemap(1).pset(x+8*stage,  y, (0,0))
            pyxel.tilemap(1).pset(x2+8*stage,y2, c)
            self.RollStone(x, y, xdiff, ydiff)
        elif tile == (1,2):
            if c == RED_BALL:
                pyxel.tilemap(1).pset(x+8*stage,  y, (0,0))
                pyxel.tilemap(1).pset(x2+8*stage,y2, RED_BALL_OUT)
                self.Tell_impossible()
            elif c == BLUE_BALL:
                pyxel.tilemap(1).pset(x+8*stage,  y, (0,0))
                pyxel.tilemap(1).pset(x2+8*stage,y2, BLUE_BALL_OUT)

            elif c == YELLOW_BALL:
                pyxel.tilemap(1).pset(x+8*stage,  y, (0,0))
                pyxel.tilemap(1).pset(x2+8*stage,y2, YELLOW_BALL_OUT)
                self.Tell_impossible()

            elif c == GREEN_BALL:
                pyxel.tilemap(1).pset(x+8*stage,  y, (0,0))
                pyxel.tilemap(1).pset(x2+8*stage,y2, GREEN_BALL_OUT)
                self.Tell_impossible()

    # キャラクタが画面内にいるか判定
    def is_in_field(self, xdiff, ydiff):
        x = self.cherry.x + xdiff
        y = self.cherry.y + ydiff
        return (x > 0 and x < 7 and y > 0 and y < 7)

    # ボールが緑，黄色，赤の順番に並んでいるか
    # 黄色が2番目であれば，順序は問わない
    def is_clear(self):
        global stage

        yellow_ball_position = (-1,-1)
        # まず黄色の位置がどこか調べる
        for x in range(0,8):
            for y in range(0,8):
                tile = pyxel.tilemap(1).pget(x + 8*stage, y)
                if tile == YELLOW_BALL:
                    yellow_ball_position = (x + 8*stage, y)
                    break
                
        print(yellow_ball_position)
        #print(stage)
        
        x =  yellow_ball_position[0]
        y =  yellow_ball_position[1]
        
        #次に黄色の上下に赤か緑があるか調べる
        above  = pyxel.tilemap(1).pget(x, y-1)
        under  = pyxel.tilemap(1).pget(x, y+1)
        if ((above == RED_BALL and under == GREEN_BALL) or (above == GREEN_BALL and under == RED_BALL)):
            return True

        #次に黄色の左右に赤か緑があるか調べる
        left   = pyxel.tilemap(1).pget(x -1, y)
        right  = pyxel.tilemap(1).pget(x +1, y)
        if ((left == RED_BALL and right == GREEN_BALL) or (left == GREEN_BALL and right == RED_BALL)):
            return True

        return False

        
    def update(self):
        global scene
        global stage
        global timing

        if scene == SCREEN_TITLE:
            if pyxel.btnp(pyxel.KEY_SPACE):
                scene = SCREEN_START
                stage = 0
            elif pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_LEFT): 
                scene = SCREEN_SELECT
                
        elif scene == SCREEN_SELECT:
            if pyxel.btnp(pyxel.KEY_RIGHT):
                if stage < N_OF_STAGE:
                    stage = stage + 1
            elif pyxel.btnp(pyxel.KEY_LEFT):
                if stage > 0:
                    stage = stage - 1
            elif pyxel.btnp(pyxel.KEY_SPACE):
                scene = SCREEN_START
                             
        elif scene == SCREEN_START:
            time.sleep(1.5)
            self.cherry = Cherry(1, 1)
            scene = SCREEN_PAZZLE
                
        elif scene == SCREEN_CLEAR:
            time.sleep(1.5)
            if stage > N_OF_STAGE:
                scene = SCREEN_ALL_CLEAR
            else:
                scene = SCREEN_START
            
        elif scene == SCREEN_ALL_CLEAR:
            if random.random() < .2:
                timing = random.randint(0,3)
                
            if pyxel.btnp(pyxel.KEY_R):
                pyxel.load("test.pyxres")
                scene = SCREEN_TITLE
            elif pyxel.btnp(pyxel.KEY_Q):
                sys.exit()
                
        elif scene ==  SCREEN_IMPOSSIBLE:
            if pyxel.btnp(pyxel.KEY_R):
                pyxel.load("test.pyxres")
                scene = SCREEN_START
            elif pyxel.btnp(pyxel.KEY_Q):
                sys.exit()
        
        elif scene == SCREEN_PAZZLE:

            # クリアしているかどうか調べる
            if self.is_clear():
                time.sleep(.5)
                scene = SCREEN_CLEAR
                stage = stage + 1

            if (time.time() - self.cherry.pre_time > 0.5):
                self.cherry.pre_time = time.time()
                if (self.cherry.step == 1):
                    self.cherry.step = 0
                else:
                    self.cherry.step = 1
                
            # リプレイ
            if pyxel.btnp(pyxel.KEY_R):
                pyxel.load("test.pyxres")
                scene = SCREEN_START
                
            if pyxel.btnp(pyxel.KEY_UP):
                if self.is_in_field(0, -1):
                    if self.isSpaseToMove(0, -1) == True:
                        self.cherry.y = self.cherry.y - 1
                        self.cherry.direction = UP
                    else:
                        self.RollStone(self.cherry.x, self.cherry.y, 0, -1)
            
            if pyxel.btnp(pyxel.KEY_DOWN):
                if self.is_in_field(0, 1):
                    if self.isSpaseToMove(0, 1) == True:
                        self.cherry.y = self.cherry.y + 1
                        self.cherry.direction = DOWN
                    else:
                        self.RollStone(self.cherry.x, self.cherry.y, 0, 1)
                
            if pyxel.btnp(pyxel.KEY_RIGHT):
                if self.is_in_field(1, 0):
                    if self.isSpaseToMove(1, 0) == True:
                        self.cherry.x = self.cherry.x + 1
                        self.cherry.direction = RIGHT 
                    else:
                        self.RollStone(self.cherry.x, self.cherry.y, 1, 0)
                
            if pyxel.btnp(pyxel.KEY_LEFT):
                if self.is_in_field(-1, 0):
                    if self.isSpaseToMove(-1, 0) == True:
                        self.cherry.x = self.cherry.x - 1
                        self.cherry.direction = LEFT
                    else:
                        self.RollStone(self.cherry.x, self.cherry.y, -1, 0)

    def draw(self):
        global scene
        global stage
        
        if scene == SCREEN_TITLE:
            pyxel.bltm(0, 0, 0, 0, 0, 64, 64)
            pyxel.text(8, 16, "Rastafarian!", 7)
        elif scene == SCREEN_SELECT:
            pyxel.bltm(0, 0, 1, 64*stage, 0, 64, 64)
            pyxel.text(8, 8*7, "STAGE", 7)
            pyxel.text(8 + 8*5, 8*7, str(stage), 7)
        elif scene == SCREEN_START:
            pyxel.bltm(0, 0, 0, 0, 0, 64, 64)
            pyxel.text(8, 16, "STAGE", 7)
            pyxel.text(8+8*4, 16, str(stage), 7)
        elif scene == SCREEN_CLEAR:
            #pyxel.bltm(0, 0, 0, 0, 0, 64, 64)
            pyxel.text(16, 16, "CLEAR!", 7)
        elif scene == SCREEN_IMPOSSIBLE:
            pyxel.text(8, 16, "Impossible...", 7)
        elif scene == SCREEN_ALL_CLEAR:
            pyxel.bltm(0, 0, 0, timing*8*8, 8*2*8, 64, 64)
            pyxel.text(16, 16, "ALL Clear!", 7)
        else:
            pyxel.cls(0)

            # マップを書く
            pyxel.bltm(0, 0, 1, 64*stage, 0, 64, 64)
            
            t = self.cherry.step
            v = self.cherry.direction
            if v == RIGHT:
                pyxel.blt(self.cherry.x*8, self.cherry.y*8, 0, t*8, 24, 8, 8, 2)
            elif v == LEFT:
                pyxel.blt(self.cherry.x*8, self.cherry.y*8, 0, t*8, 0, 8, 8, 2)
            elif v == DOWN:
                pyxel.blt(self.cherry.x*8, self.cherry.y*8, 0, t*8, 8, 8, 8, 2)
            else:
                pyxel.blt(self.cherry.x*8, self.cherry.y*8, 0, t*8, 16, 8, 8, 2)
            

App()
