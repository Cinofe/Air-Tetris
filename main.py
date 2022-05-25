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
        self.Best_Score = 0

        self.Get = '1'
        self.Set = '2'
        self.stream = '3'
        self.host = '210.125.31.101'
        self.port = 10000
        self.Sock = socket(AF_INET, SOCK_STREAM)
        self.Sock.connect((self.host, self.port))
        self.StreamSock = None
        self.return_value = 0
    ##--------------------------------------------------------------------------------------------##
    ##  Error 출력 함수
    ##--------------------------------------------------------------------------------------------##
    def Error(self, str, error):
        print(f'{str}{error}')
    ##--------------------------------------------------------------------------------------------##
    ##  server로 data 전송 하는 함수
    ##--------------------------------------------------------------------------------------------##
    def sendData(self, conn, data):
        try:
            conn.send(str(len(data)).ljust(16).encode('utf-8'))
            conn.send(data)
        except Exception as e:
            self.Error('send Error : ', e)
    ##--------------------------------------------------------------------------------------------##
    ##  server로 data 받는 함수
    ##--------------------------------------------------------------------------------------------##
    def recvData(self,count):
        try:
            buf = b''
            while count:
                newbuf = self.Sock.recv(count)
                if not newbuf:
                    return None
                buf += newbuf
                count -= len(newbuf)
            return buf
        except Exception as e:
            self.Error('recv Error : ', e)
    ##--------------------------------------------------------------------------------------------##
    ##  data Encoding 하는 함수
    ##--------------------------------------------------------------------------------------------##
    def encoded(self, data):
        return str(data).encode('utf-8')
    ##--------------------------------------------------------------------------------------------##
    ##  Best_Score 요청 하는 함수
    ##--------------------------------------------------------------------------------------------##
    def Get_Bs(self):
        self.sendData(self.Sock, self.encoded(self.Get))
        length = self.recvData(16).decode('utf-8')
        self.Best_Score = self.recvData(int(length)).decode('utf-8')
    ##--------------------------------------------------------------------------------------------##
    ##  Best_Score 전송 하는 함수
    ##--------------------------------------------------------------------------------------------##
    def Set_Bs(self):
        self.sendData(self.Sock, self.encoded(self.Set))
        self.sendData(self.Sock, self.encoded(self.Best_Score))
    ##--------------------------------------------------------------------------------------------##
    ##  server와 Streaming 연결 하는 함수
    ##--------------------------------------------------------------------------------------------##
    def Streaming(self):
        self.sendData(self.Sock, self.encoded(self.stream))
        length = self.recvData(16).decode('utf-8')
        port = self.recvData(int(length)).decode('utf-8')

        try:
            self.StreamSock = socket(AF_INET, SOCK_STREAM)
            self.StreamSock.connect((self.host,int(port)))
        except Exception as e:
            self.Error('stream Connect Error : ', e)

        cap = cv2.VideoCapture(0)
        while(not self.done):
            _, frame = cap.read()

            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),90]
            _, b_frame = cv2.imencode('.jpg',frame,encode_param)
            b_frame = np.array(b_frame)
            self.sendData(self.StreamSock, b_frame)
            cv2.waitKey(10)
    ##--------------------------------------------------------------------------------------------##
    ##  Tetris 실행 함수
    ##--------------------------------------------------------------------------------------------##
    def start_Game(self):
        while(not self.done):
            self.retry = False
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
                # if t.time() - m_start >= move_time:
                #     G.Move_Down()
                #     m_start = t.time()
                # if t.time() - u_start >= up_block_time:
                #     G.Line_Plus()
                #     u_start = t.time()
                if G.GAME_OVER():
                    if self.Best_Score < G.Score:
                        self.Best_Score = G.Score
                        self.Set_Bs()
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
                        if self.return_value == None:
                            continue
                        if event.key == pg.K_UP or self.return_value == 1:
                            G.Turnning()
                        if event.key == pg.K_DOWN or self.return_value == 2:
                            G.Move_Down()
                        if event.key == pg.K_LEFT or self.return_value == 3:
                            G.Move_Left()
                        if event.key == pg.K_RIGHT or self.return_value == 4:
                            G.Move_Right()
                        if event.key == pg.K_SPACE or self.return_value == 5:
                            G.instant_down()
                        if event.key == pg.K_r:
                            del G
                            self.retry = True
    ##--------------------------------------------------------------------------------------------##
    ##  프로그램 시작
    ##--------------------------------------------------------------------------------------------##
    def run(self):
        print('running')
        self.Get_Bs()
        t1 = th(target=self.Streaming)
        t1.daemon = True
        t1.start()

        t2 = th(target=self.start_Game)
        t2.daemon = True
        t2.start()

        t1.join()
        t2.join()

if __name__ == "__main__":
    main = Main()
    main.run()