import pygame as pg, time as t, cv2, numpy as np
from threading import Thread as th
from socket import *
from Game import Game
from menu import Menu
##------------------------------------------------------------------------------------------------##
## 메인 클래스
##------------------------------------------------------------------------------------------------##
done = False

def start_Game():
    global done
    while(not done):
        m_start = t.time()
        u_start = t.time()
        move_time = 2
        up_block_time = 10
        M = Menu()
        value = M.run()
        if value == False:
            done = True
            break
        elif value == 1:
            move_time = 1.5
            up_block_time = 10
        elif value == 2:
            move_time = 1.25
            up_block_time = 8
        elif value == 3:
            move_time = 1
            up_block_time = 6
        G = Game()

        retry = False
        while(not retry):
            if t.time() - m_start >= move_time:
                G.Move_Down()
                m_start = t.time()
            if t.time() - u_start >= up_block_time:
                G.Line_Plus()
                u_start = t.time()
            if G.GAME_OVER():
                del G
                retry = True
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
## client 스트리밍
##------------------------------------------------------------------------------------------------##
def Streaming():
    global done
    try :
        ClientSock = socket(AF_INET, SOCK_STREAM)
        ClientSock.connect(('210.125.31.101', 8080))
    except Exception:
        print("Connection Error")
    cap = cv2.VideoCapture(0)

    while(not done):
        _, frame = cap.read()
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),90]
        _, encode_frame = cv2.imencode('.jpg',frame, encode_param)
        data = np.array(encode_frame)
        ClientSock.send(str(len(data)).ljust(16).encode('utf-8'))
        ClientSock.send(data)
        cv2.waitKey(10)
    
    ClientSock.close()

def main():
    client_th = th(target=Streaming)
    game_th = th(target=start_Game)

    client_th.start()
    game_th.start()

    client_th.join()
    game_th.join()
    
    
if __name__ == "__main__":
    main()