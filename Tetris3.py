import pygame as pg, time as t, cv2, numpy as np
from threading import Thread as th
from socket import *
from Game import Game
from menu import Menu
##------------------------------------------------------------------------------------------------##
## 메인 클래스
##------------------------------------------------------------------------------------------------##
class Main:
    def __init__(self):
        self.done = False
        self.retry = False
        self.masterKey = 0
        self.retur_value = self.masterKey #None

        self.getBs_Sock = socket(AF_INET, SOCK_STREAM)
        self.Streaming_Sock = socket(AF_INET, SOCK_STREAM)

        # try :    
        #     self.getBs_Sock.connect(('210.125.31.101', 10001))
        #     self.Streaming_Sock.connect(('210.125.31.101', 10002))
        # except Exception as e:
        self.getBs_Sock.connect(('192.168.181.155', 10001))
        self.Streaming_Sock.connect(('192.168.181.155', 10002))
            # print(f"Connection Error : {e}")
        self.Best_Score = 0

    def start_Game(self):

        while(not self.done):
            m_start = t.time()
            u_start = t.time()
            move_time = 2
            up_block_time = 10
            M = Menu()
            value = M.run()
            if value == False:
                self.done = True
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
            G = Game(self.Best_Score)

            while(not self.retry):
                if t.time() - m_start >= move_time:
                    G.Move_Down()
                    m_start = t.time()
                if t.time() - u_start >= up_block_time:
                    G.Line_Plus()
                    u_start = t.time()
                if G.GAME_OVER():
                    del G
                    self.retry = True
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.done = True
                        self.retry = True
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            self.done = True
                            self.retry = True
                        if self.retur_value == None:
                            continue
                        if event.key == pg.K_UP or self.retur_value == 0:
                            G.Turnning()
                        if event.key == pg.K_DOWN or self.retur_value == 0:
                            G.Move_Down()
                        if event.key == pg.K_LEFT or self.retur_value == 0:
                            G.Move_Left()
                        if event.key == pg.K_RIGHT or self.retur_value == 0:
                            G.Move_Right()
                        if event.key == pg.K_SPACE or self.retur_value == 0:
                            G.instant_down()
                        if event.key == pg.K_r:
                            del G
                            self.retry = True
    ##------------------------------------------------------------------------------------------------##
    ## client 스트리밍
    ##------------------------------------------------------------------------------------------------##
    def Streaming(self):
        try:
            self.Streaming_Sock.sendall('2'.encode('utf-8'))
            if self.Streaming_Sock.recv(1024).decode('utf-8') == '200':
                cap = cv2.VideoCapture(0)
                while(not self.done):
                    _, frame = cap.read()
                    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),90]
                    _, encode_frame = cv2.imencode('.jpg',frame, encode_param)
                    data = np.array(encode_frame)
                    self.Streaming_Sock.send(str(len(data)).ljust(16).encode('utf-8'))
                    self.Streaming_Sock.send(data)
                    cv2.waitKey(10)
        except Exception as e:
            print(f'Connection Error : Streaming_Sock({e})')
            self.done = True
        self.Streaming_Sock.close()

    def Get_Bs(self):
        try:
            self.getBs_Sock.sendall('1'.encode('utf-8'))
            self.Best_Score = int(self.getBs_Sock.recv(1024).decode('utf-8'))
        except Exception as e:
            print(f'Connection Error : getBs_Sock({e})')
        self.getBs_Sock.close()
        
    def run(self):
        # 프로그램의 시작 지점
        self.Get_Bs()
        client_th = th(target=self.Streaming)
        game_th = th(target=self.start_Game)

        client_th.start()
        game_th.start()

        client_th.join()
        game_th.join()
    
    
if __name__ == "__main__":
    main = Main()
    main.run()