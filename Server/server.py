from Recognization import Recognization
from threading import Thread as thd
from socket import *
import _thread as th, cv2, numpy as np, time as ti, pickle as pk
##------------------------------------------------------------------------------------------------##
## 서버 클래스
##------------------------------------------------------------------------------------------------##
class Server:
    def __init__(self):
        self.Best_Score = 0
        self.StreamPort = 10001
        self.host = '0.0.0.0'
        self.port = 10000

        self.Recog = Recognization()
        self.motion_result = 0
        self.frame = None
        self.show_frame = None
        self.hand_box = []
        self.motion = {0:'ready',1:'left',2:'right',3:'turn',4:'instant'}

        self.Sock = socket(AF_INET, SOCK_STREAM)
        self.Sock.bind((self.host, self.port))
        self.StreamSock = socket(AF_INET, SOCK_STREAM)
        self.StreamSock.bind((self.host, self.StreamPort))
        self.conn = None

        self.file = np.genfromtxt('./Server/dataSet.txt', delimiter=',')
        self.angleFile = self.file[:,:-1]
        self.labelFile = self.file[:,-1]
        self.angle = self.angleFile.astype(np.float32)
        self.label = self.labelFile.astype(np.float32)
        self.knn = cv2.ml.KNearest_create()
        self.knn.train(self.angle,cv2.ml.ROW_SAMPLE,self.label)
        
    ##--------------------------------------------------------------------------------------------##
    ## Error 출력 함수
    ##--------------------------------------------------------------------------------------------##
    def Error(self, str, e):
        print(f'{str}{e}')
    ##--------------------------------------------------------------------------------------------##
    ## data 불러오는 함수
    ##--------------------------------------------------------------------------------------------##
    def loadData(self):
        try:
            with open(r'./data.txt','r') as f:
                self.Best_Score = int(f.readline())
        except Exception as e:
            self.Error('Load Error : ', e)
            self.saveData()
            self.loadData()
    ##--------------------------------------------------------------------------------------------##
    ## data 저장 함수
    ##--------------------------------------------------------------------------------------------##
    def saveData(self):
        try:
            with open(r'./data.txt','w') as f:
                f.write(str(self.Best_Score))
        except Exception as e:
            self.Error('Save Error : ', e)
    ##--------------------------------------------------------------------------------------------##
    ## Client로 부터 데이터 받는 함수
    ##--------------------------------------------------------------------------------------------##
    def recvData(self, conn, count):
        try :
            data = b''
            while count:
                newbuf = conn.recv(count)
                if not newbuf:
                    return None
                data += newbuf
                count -= len(newbuf)
            return data
        except Exception as e:
            self.Error('recv Error : ', e)
    ##--------------------------------------------------------------------------------------------##
    ## Client로 데이터 보내는 함수
    ##--------------------------------------------------------------------------------------------##
    def sendData(self, conn, data):
        try:
            conn.send(str(len(data)).ljust(16).encode('utf-8'))
            conn.send(str(data).encode('utf-8'))
        except Exception as e:
            self.Error('send Error : ', e)
    ##--------------------------------------------------------------------------------------------##
    ## 인식한 손의 좌표 정보를 토대로 모션을 인식하여 반환 하는 함수
    ##--------------------------------------------------------------------------------------------##
    def Get_handMotion(self, landmark):
        self.motion_result = 0
        f_name = str(th.get_native_id())
        h, w, _ = self.frame.shape
        x, y = [], []
        index = -1
        self.hand_box = []
        for res in landmark:
            for i in range(21):
                lx, ly = round(res.landmark[i].x * w), round(res.landmark[i].y * h)
                x.append(lx)
                y.append(ly)
            
            self.hand_box = [min(x)-20, min(y)-20,
                            abs(max(x)-min(x))+40,
                            abs(max(y)-min(y))+40]
            if any(self.hand_box):
                cv2.rectangle(self.frame,self.hand_box, (0,0,0),2)

            joint = np.zeros((21,2))
            for j, lm in enumerate(res.landmark):
                # 각 좌표의 중심 좌표를 0이 아닌 0.5를 기준으로 잡고 벡터 구하기
                joint[j] = [lm.x - 0.5, 0.5 - lm.y]
            # 엄지 좌표를 제외한 각 좌표의 벡터 시작점, 끝점 지정
            v1 = joint[[0, 5, 6, 7, 0, 9,10,11, 0,13,14,15, 0,17,18,19],:]
            v2 = joint[[5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20],:]
            # 각 좌표 상의 벡터 계산
            v = v2 - v1
            # 벡터의 크기 도출
            v = v / np.linalg.norm(v, axis=1)[:,np.newaxis]

            # 각 좌표 벡터의 x,y 의 곱 계산
            result = [round(i * (j+0.2),6) for i,j in v]

            data = np.array([result],dtype=np.float32)
            _, result, _, _ = self.knn.findNearest(data,3)
            index = int(result[0][0])

            if index in self.motion.keys():
                cv2.putText(self.frame, self.motion[index].upper(),
                        (int(res.landmark[0].x * self.frame.shape[1] -10),
                        int(res.landmark[0].y * self.frame.shape[0] + 40)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,0), 3)
    
        return index
    ##--------------------------------------------------------------------------------------------##
    ## Client로부터 스트리밍 데이터 받는 함수
    ##--------------------------------------------------------------------------------------------##    
    def Stream(self):
        stime = ti.time()
        try:
            print('stream connect wait...')
            self.StreamSock.listen(1)
            S_conn, addr = self.StreamSock.accept()
            print(f'connect : {str(addr[0])}')
        except Exception as e:
            self.Error('Stream Connect Error : ', e)

        f_stime = ti.time()

        while(True):
            f_name = str(th.get_native_id())
            try:
                try:
                    length = self.recvData(S_conn,16).decode('utf-8')
                except Exception as e:
                    self.Error('Stream No data Error : ',e)
                    return

                data = self.recvData(S_conn, int(length))
                data = np.frombuffer(data, dtype='uint8')
                self.frame = cv2.imdecode(data,1)
                self.frame = cv2.flip(self.frame,0)
                self.frame, landmark = self.Recog.processing(self.frame)

                fps = 1//(ti.time() - f_stime)
                f_stime = ti.time()
                cv2.putText(self.frame, str(fps),(20,40),0,1,(0,0,255),2)

                if any(landmark):
                    index = self.Get_handMotion(landmark)
                    ## 서버에서는 그냥 데이터를 주고, 클라이언트에서 조절
                    self.motion_result = index
                else:
                    self.motion_result = -1
                if ti.time() - stime > 0.1:
                    self.sendData(self.conn, str(self.motion_result))
                    stime = ti.time()
                
                cv2.imshow(f_name,self.frame)
                cv2.moveWindow(f_name, 500, 250)
                cv2.waitKey(1)
            except Exception:
                return      
    ##--------------------------------------------------------------------------------------------##
    ## Client가 요청을 구부하는 함수
    ##--------------------------------------------------------------------------------------------##
    def request(self, conn, req):  
        print(f'req : {req}',end='')
        if req == '1': # Get
            print('(get)')
            self.loadData()
            self.sendData(conn, str(self.Best_Score))
        elif req == '2': # Set
            print('(set)')
            length = self.recvData(conn,16).decode('utf-8')
            self.Best_Score = self.recvData(conn,int(length)).decode('utf-8')
            self.saveData()
        elif req == '3': # Streaming
            print('(stream)')
            self.sendData(conn, str(self.StreamPort))
            th.start_new_thread(self.Stream)
    ##--------------------------------------------------------------------------------------------##
    ## 메인 서버 루틴
    ##--------------------------------------------------------------------------------------------##   
    def run(self):
        print('waiting...')
        self.__init__()
        try:
            self.Sock.listen(1)
            self.conn, addr = self.Sock.accept()
            print(f'Connect : {str(addr[0])}')
        except Exception as e:
            self.Error('Connect Error : ', e)
        
        while(True):
            try:
                length = self.recvData(self.conn,16).decode('utf-8')
            except Exception as e:
                self.Error('No data Error : ',e)
                return
            if length != '0':
                req = self.recvData(self.conn, int(length)).decode('utf-8')
                self.request(self.conn, req)


if __name__ == '__main__':
    server = Server()
    print('open')
    while(True):
        t = thd(target = server.run)
        t.start()
        t.join()
