import pygame as pg, time as t, cv2, numpy as np, sys, pickle as pk
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
        self.value = -1

        self.Get = '1'
        self.Set = '2'
        self.stream = '3'
        self.motion = '4'
        self.host = '210.125.31.101'
        # self.host = '192.168.0.6'
        self.port = 10000
        self.Sock = socket(AF_INET, SOCK_STREAM)
        self.Sock.connect((self.host, self.port))
        self.StreamSock = None
        self.motion_value = 0
        self.prev_motion = 0
        self.motion = {0:'READY',1:'LEFT',2:'RIGHT',3:'TURN',4:'DOWN',-1:'Detect Fail'}
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
            if str(e) == '[Errno 32] Broken pipe':
                self.Error('send Error : ', e)
                sys.exit()
            else : 
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
        self.Best_Score = int(self.recvData(int(length)).decode('utf-8'))
    ##--------------------------------------------------------------------------------------------##
    ##  Best_Score 전송 하는 함수
    ##--------------------------------------------------------------------------------------------##
    def Set_Bs(self):
        self.sendData(self.Sock, self.encoded(self.Set))
        self.sendData(self.Sock, self.encoded(self.Best_Score))
    ##--------------------------------------------------------------------------------------------##
    ##  Server로부터 motion정보를 받아오는 함수
    ##--------------------------------------------------------------------------------------------##
    def Get_motion(self):
        hand_box = []
        try:
            length = self.recvData(16).decode('utf-8')
        except Exception as e:
            self.Error('No Data Error : ', e)
            self.retry = True
            self.done = True
        self.motion_value = int(self.recvData(int(length)).decode('utf-8'))

        length = self.recvData(16).decode('utf-8')
        req = self.recvData(int(length)).decode('utf-8')
        if req == '4':
            for _ in range(4):
                length = self.recvData(16).decode('utf-8')
                hand_box.append(self.recvData(int(length)).decode('utf-8'))

            x,y,w,h = list(map(int, hand_box))
            if w < 320 or h < 240:
                x -= 80
                y -= 60
                w += 160
                h += 120
            xw = x + w
            yh = y + h
            if x < 0 :
                x = 0
            if y < 0 :
                y = 0
            if xw > 640:
                xw = 640
            if yh > 480:
                yh = 480
            cv2.imshow('',self.frame[y:yh,x:xw])
            cv2.moveWindow('',500,0)
            cv2.waitKey(1)
        else:
            cv2.destroyWindow('')

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

        cap = cv2.VideoCapture(cv2.CAP_V4L2)
        stime = t.time()

        while(not self.done):
            if self.value == False:
                sys.exit()
            ret, self.frame = cap.read()
            
            if (ret is True) and ((t.time() - stime) > 1//60):
                stime = t.time()
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),90]
                _, b_frame = cv2.imencode('.jpg',self.frame,encode_param)
                b_frame = np.array(b_frame) 
                self.sendData(self.StreamSock, b_frame)
                cv2.waitKey(1)
    ##--------------------------------------------------------------------------------------------##
    ##  Tetris 실행 함수
    ##--------------------------------------------------------------------------------------------##
    def start_Game(self):
        while(not self.done):
            self.retry = False
            # 타이머 설정
            d_stime = t.time()
            u_stime = t.time()
            mo_stime = t.time()

            down_delay = 2
            up_block_delay = 10
            mo_delay = 1.5


            M = Menu()
            self.value = M.run()
            if self.value == False:
                sys.exit()
            elif self.value == 1:
                down_delay = 2
                up_block_delay = 20
            elif self.value == 2:
                down_delay = 1.7
                up_block_delay = 15
            elif self.value == 3:
                down_delay = 1.4
                up_block_delay = 10

            G = Game(self.Best_Score)
            while(not self.retry):
                if t.time() - d_stime >= down_delay:
                    G.Move_Down()
                    d_stime = t.time()
                # if t.time() - u_start >= up_block_time:
                #     G.Line_Plus()
                #     u_start = t.time()
                if G.GAME_OVER():
                    if self.Best_Score < G.Score:
                        self.Best_Score = G.Score
                        self.Set_Bs()
                    del G
                    self.retry = True
                    break
                ## 모션으로 조정
                self.Get_motion()
                # Left, Right는 처음 입력 받고 다음에서 같은 데이터가 오면 0.7초 대기 후, 
                # 0.2초마다 Move_Left 실행
                # Turn, Instatn는 딱 한번만 입력 받기
                # 이전 데이터와 겹치지 않을 때는 즉시 반영
                G.set_motion(self.motion.get(self.motion_value))

                if self.prev_motion == 1 and self.motion_value == 1:
                    if t.time() - mo_stime > mo_delay:
                        G.Move_Left()
                        mo_delay = 0.5
                        mo_stime = t.time()
                elif self.prev_motion == 2 and self.motion_value == 2:
                    if t.time() - mo_stime > mo_delay:
                        G.Move_Right()
                        mo_delay = 0.5
                        mo_stime = t.time()
                elif self.prev_motion == 3 or self.prev_motion == 4:
                    if self.motion_value == 3 or self.motion_value == 4:
                        continue
                else:
                    if self.motion_value == 1:
                        G.Move_Left()
                    elif self.motion_value == 2:
                        G.Move_Right()
                    elif self.motion_value == 3:
                        G.Turnning()
                    elif self.motion_value == 4:
                        G.instant_down()
                    mo_delay = 0.7
                self.prev_motion = self.motion_value
                
                ## 키입력 조정
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.done = True
                        self.retry = True
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            # self.done = True
                            self.retry = True
                        if event.key == pg.K_q :
                            self.retry = True
                            self.done = True
                            return
                        # if event.key == pg.K_UP or self.motion_value == 1:
                        #     G.Turnning()
                        # if event.key == pg.K_DOWN or self.motion_value == 2:
                        #     G.Move_Down()
                        # if event.key == pg.K_LEFT or self.motion_value == 3:
                        #     G.Move_Left()
                        # if event.key == pg.K_RIGHT or self.motion_value == 4:
                        #     G.Move_Right()
                        # if event.key == pg.K_SPACE or self.motion_value == 5:
                        #     G.instant_down()
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