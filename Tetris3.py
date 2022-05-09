import pygame as pg, time as t
from Game import Game
##------------------------------------------------------------------------------------------------##
## 게임 시작 함수
##------------------------------------------------------------------------------------------------##
def start_Game():
    done = False
    start = t.time()
    while(not done):
        print('run game')
        G = Game()
        retry = False
        while(not retry):
            print('running game')
            # if t.time() - start >= 1:
            #     G.Move_Down()
            #     start = t.time()
            if G.GAME_OVER():
                print('gameover')
                del G
                retry = True
                done = True
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                    retry = True
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        done = True
                        retry = True
                    if event.key == pg.K_UP:
                        G.Turnning()
                    if event.key == pg.K_DOWN:
                        G.Move_Down()
                    if event.key == pg.K_LEFT:
                        G.Move_Left()
                    if event.key == pg.K_RIGHT:
                        G.Move_Right()
                    if event.key == pg.K_SPACE:
                        G.instant_down()
                    if event.key == pg.K_r:
                        del G
                        retry = True
##------------------------------------------------------------------------------------------------##
## 메인 함수
##------------------------------------------------------------------------------------------------##
def main():
    start_Game()
    
if __name__ == "__main__":
    main()