from Recognization import Recognization
from Game import Game
from menu import Menu
import pygame as pg, time as t, cv2, numpy as np, sys

class Main:
    # 변수 초기화
    def __init__(self):
        # 게임 환경 관련 변수 
        self.done = False
        self.retry = False
        self.playType = False
        self.Options = { False : [False, False], 1 : [2, 25], 2 : [1.7, 20], 3: [1.4, 15]}

        # 타이머 설정
        self.downBlockStartTime = t.time() # 내려오는 블럭 생성 시작점 기록
        self.upBlcokStartTime = t.time() # 올라오는 블럭 생성 시작점 기록
        self.motionMoveTimer = t.time() # 모션으로 움직이는 블럭 시작점 기록
 
        # 기본 Delay 설정
        self.downBlockDelay = 2
        self.upBlockDelay = 10
        self.motionDelay = 1.5
    
        # 최고 점수
        self.BestScore = 0

        # 메뉴 보기
        self.showMenu()
        
        # 선택한 난이도에 따른 Delay 설정
        self.downBlockDelay, self.upBlockDelay = self.Options.get(self.selectedOption)

        # 모션 사용시 변수 선언
        if self.playType:
            # 카메라 객체 생성
            self.cap = cv2.VideoCapture(0)
            self.frame = None

            # KNN 모델 생성 및 데이터 불러오기
            self.dataFile = np.genfromtxt('../dataSet.txt', delimiter=',')
            self.data = self.dataFile[:,:-1].astype(np.float32)
            self.label = self.dataFile[:,-1].astype(np.float32)
            self.knn = cv2.ml.KNearest_create()

            # 불러온 데이터로 학습
            self.knn.train(self.data, cv2.ml.ROW_SAMPLE, self.label)

            # 모션 감지 객체 생성
            self.recog = Recognization()
            
            # 모션 감지 변수
            self.motionValue = -1
            self.prevMotion = -1
            self.motion = {0:'READY',1:'LEFT',2:'RIGHT',3:'TURN',4:'DOWN',-1:'Not Detected'}

    # 메뉴 불러오기
    def showMenu(self):
        self.retry = True
        self.M = Menu()
        self.selectedOption, self.playType = self.M.run()
        # 종료 옵션 선택시 종료
        if not self.selectedOption:
            sys.exit()
    
    # 모션 인식
    def getMotion(self):
        # 카메라에서 데이터 읽어오기
        ret, self.frame = self.cap.read()
        h, w, _ = self.frame.shape
        index = -1
        # 데이터를 읽어올 수 없을 경우 오류 메시지 출력 및 종료
        if not ret:
            print("The camera cna't be detected. Please check the camera connection.")
            sys.exit()

        # 사용자가 가리키는 방향대로 인식하기 위해 좌우 대칭 변경
        self.frame = cv2.flip(self.frame, 1)
        
        # Mediapipe를 통해 인식한 손의 landmark 정보 불러오기
        self.frame, landmarks = self.recog.processing(self.frame)

        # landmark를 통해 K-NN 에 입력될 데이터 생성
        for landmark in landmarks:
            # landmark의 각 좌표 정보는 픽셀 정보가 아니라 0~1로 이루어진 비율값(영상 가운데 위치한 좌표 값, x :0.5, y :0.5) 이므로 높이, 너비를 곱하여 정확한 픽셀 좌표 구하기
            # landmark는 21개의 좌표 정보를 가지고 있음
            # 각 좌표의 중심 좌표 기준을 0이 아니라 0.5를 기준으로 잡고 벡터 계산
            joint = np.array([[lm.x - 0.5, 0.5 - lm.y] for lm in landmark.landmark])

            V1 = joint[[0, 5, 6, 7, 0, 9,10,11, 0,13,14,15, 0,17,18,19],:]
            V2 = joint[[5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20],:]
            # 각 좌표의 벡터 계산
            V = V2 - V1
            # 벡터 크기 도출
            V = V / np.linalg.norm(V, axis=1)[:, np.newaxis]

            result = [round(i * (j+0.2), 6) for i, j in V]
            data = np.array([result], dtype=np.float32)
            _, result, _, _ = self.knn.findNearest(data, 3)
            index = int(result[0][0])
        return index


    def run(self):
        # 게임 시작
        while not self.done:
            G = Game()
            self.retry = False
            # 종료 옵션 선택시 종료
            if not self.selectedOption:
                sys.exit()
            while not self.retry:
                # 일정 시간 마다 생성된 블럭 아래로 내리기
                if t.time() - self.downBlockStartTime >= self.downBlockDelay:
                    G.Move_Down
                    self.downBlockStartTime = t.time()
                
                # 일정 시간 마다 바닥 블럭 위로 올리기
                if t.time() - self.upBlcokStartTime >= self.upBlockDelay:
                    G.Line_Plus()
                    self.upBlcokStartTime = t.time()
                
                # Game Over 시 최고 기록 갱신 및 메뉴화면 표시            
                if G.GAME_OVER():
                    if self.BestScore < G.Score:
                        self.BestScore = G.Score
                    # 새로운 메뉴에서 새로운 게임 옵션 선택 및 설정
                    self.showMenu()
                
                # Motion으로 Game 진행
                if self.playType:
                    self.motionValue = self.getMotion()
                    G.set_motion(self.motion.get(self.motionValue))
                    
                    ## 고쳐야할 부분 동작이 즉시 실행이 안됨. 
                    ## 또, 즉시 실행되면 순간적인 잘못된 인식에서 잘못된 결과가 도출될 수도 있음
                    # 예상 적정 딜레이 0.01 ~ 0.05
                    if self.prevMotion == self.motionValue:
                        # 한 번의 동작으로 여러 이동 연계를 위해 Delay 감소1
                        self.motionDelay = 0.2
                    else:
                        self.motionDelay = 0.7
                    if t.time() - self.motionMoveTimer > self.motionDelay:
                        if self.motionValue == 1:
                            G.Move_Left()
                        elif self.motionValue == 2:
                            G.Move_Right()
                        elif self.motionValue == 3:
                            G.Turnning()
                        elif self.motionValue == 4:
                            G.instant_down()
                        self.motionMoveTimer = t.time()
                        self.prevMotion = self.motionValue

                # Keyboard로 Game 진행
                else :
                    for e in pg.event.get():
                        if e.type == pg.QUIT:
                            self.done = True
                            self.retry = True
                        if e.type == pg.KEYDOWN:
                            # ESC 키 입력 시 메뉴 화면으로 돌아가기
                            if e.key == pg.K_ESCAPE:
                                self.showMenu()
                            # R 키 입력 시 재시작
                            if e.key == pg.K_r:
                                self.retry = True
                            # 위쪽 방향키 : 블럭 회전
                            if e.key == pg.K_UP:
                                G.Turnning()
                            # 아래쪽 방향키 : 블럭 한 칸 내리기
                            if e.key == pg.K_DOWN:
                                G.Move_Down()
                            # 왼쪽, 오른쪽 방향키 : 블럭 좌, 우 이동
                            if e.key == pg.K_LEFT:
                                G.Move_Left()
                            if e.key == pg.K_RIGHT:
                                G.Move_Right()
                            # 스페이스 바 : 블럭 한 번에 내리기
                            if e.key == pg.K_SPACE:
                                G.instant_down()

if __name__ == "__main__":
    main = Main()
    main.run()