from http.client import CONTINUE
import pygame as pg, random as rd
from Block import Block
from Case import Case
##-------------------------------------------------------------------------------------------------##
## 게임 클래스
##-------------------------------------------------------------------------------------------------##
class Game:
    def __init__(self):
        print('init pygame')
        pg.init()
        pg.key.set_repeat(300,100)
        self.__screen = pg.display.set_mode([535, 645])

        self.__Colors = {
            'BLACK':(0,0,0),
            'WHITE':(255,255,255),
            'RED':(255,21,21),
            'GREEN':(21,255,21),
            'BLUE':(21,51,255),
            'YELLOW':(255,255,21),
            'PURPLE':(153,21,255),
            'SKY':(21,255,255),
            'ORANGE':(255,153,21)
        }
        self.__Blocks = {
            0:{
                0:[[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]],
                1:[[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]],
                2:[[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]],
                3:[[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]]
            },
            1:{
                0:[[0,0,1,0],[0,0,1,0],[0,0,1,0],[0,0,1,0]],
                1:[[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]],
                2:[[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0]],
                3:[[0,0,0,0],[0,0,0,0],[1,1,1,1],[0,0,0,0]]
            },
            2:{
                0:[[0,0,0,0],[0,1,1,0],[0,0,1,1],[0,0,0,0]],
                1:[[0,0,1,0],[0,1,1,0],[0,1,0,0],[0,0,0,0]],
                2:[[0,0,0,0],[0,1,1,0],[0,0,1,1],[0,0,0,0]],
                3:[[0,0,1,0],[0,1,1,0],[0,1,0,0],[0,0,0,0]]
            },
            3:{
                0:[[0,0,0,0],[0,1,1,0],[1,1,0,0],[0,0,0,0]],
                1:[[0,0,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0]],
                2:[[0,0,0,0],[0,1,1,0],[1,1,0,0],[0,0,0,0]],
                3:[[0,0,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0]]
            },
            4:{
                0:[[0,0,0,0],[0,0,1,0],[0,1,1,1],[0,0,0,0]],
                1:[[0,0,0,0],[0,0,1,0],[0,1,1,0],[0,0,1,0]],
                2:[[0,0,0,0],[0,0,0,0],[0,1,1,1],[0,0,1,0]],
                3:[[0,0,0,0],[0,0,1,0],[0,0,1,1],[0,0,1,0]]
            },
            5:{
                0:[[0,0,0,0],[0,1,0,0],[0,1,1,1],[0,0,0,0]],
                1:[[0,0,1,0],[0,0,1,0],[0,1,1,0],[0,0,0,0]],
                2:[[0,0,0,0],[1,1,1,0],[0,0,1,0],[0,0,0,0]],
                3:[[0,0,0,0],[0,1,1,0],[0,1,0,0],[0,1,0,0]]
            },
            6:{
                0:[[0,0,0,0],[0,0,1,0],[1,1,1,0],[0,0,0,0]],
                1:[[0,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,0,0]],
                2:[[0,0,0,0],[0,1,1,1],[0,1,0,0],[0,0,0,0]],
                3:[[0,0,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,0]]
            }
        }
        self.__ColorNames = ["YELLOW","SKY","RED","GREEN","PURPLE","BLUE","ORANGE"]

        self.__prevBlock = []
        self.__prevColor = ()
        self.__Map =[[('0',(0))for _ in range(10)]for _ in range(20)]

        self.__Score = 0
        # self.__BestScore = 0

        self.__createPrevBlock()
        self.__createNewBlock()
        self.__game_over = False
    ##---------------------------------------------------------------------------------------------##
    ## 화면 업데이트
    ##---------------------------------------------------------------------------------------------##
    def __screenUpdate(self):
        self.__screen.fill(self.__Colors.get('BLACK'))
        self.__drawBackground()
        self.__drawMap()
        self.__drawText('Next Block', 20, self.__Colors.get("WHITE"),(400, 184))
        # self.__drawText('Best Score : '+ str(0), 25, self.__Colors.get('WHITE'),(360,240))
        self.__drawText('Score : ' + str(self.__Score), 25, self.__Colors.get('WHITE'),(360,280))
        self.__drawPrevBlock()
        self.__drawNewBlock()
        pg.display.flip()
    ##---------------------------------------------------------------------------------------------##
    ## 미리보기 블럭 생성
    ##---------------------------------------------------------------------------------------------##
    def __createPrevBlock(self):
        choice = rd.randint(0,6)
        self.__prevBlock = self.__Blocks[choice]
        self.__prevColor = self.__Colors.get(self.__ColorNames[choice])
        self.__drawPrevBlock()
    ##---------------------------------------------------------------------------------------------##
    ## 미리보기 블럭 그리기
    ##---------------------------------------------------------------------------------------------##
    def __drawPrevBlock(self):
        for i in range(4):
            for j in range(4):
                if self.__prevBlock[0][i][j] == 1:
                    pg.draw.rect(self.__screen, self.__prevColor,[368+(j*31),53+(i*31),30,30])
    ##---------------------------------------------------------------------------------------------##
    ## 배경화면 그리기
    ##---------------------------------------------------------------------------------------------##
    def __drawBackground(self):
        pg.draw.rect(self.__screen, self.__Colors.get("WHITE"),[10,10,315,625],2)
        pg.draw.rect(self.__screen, self.__Colors.get("WHITE"),[365,50,129,129],2)
    ##---------------------------------------------------------------------------------------------##
    ## 텍스트 그리기
    ##---------------------------------------------------------------------------------------------##
    def __drawText(self, str, size, color, pos):
        self.__screen.blit(pg.font.Font(None, size).render(str,True,color),pos)
    ##---------------------------------------------------------------------------------------------##
    ## 맵 그려주기
    ##---------------------------------------------------------------------------------------------##
    def __drawMap(self):
        for i in range(20):
            for j in range(10):
                if self.__Map[i][j][0] == '1':
                    pg.draw.rect(self.__screen, self.__Map[i][j][1], [13 + (j*31), 13 + (i*31),30,30])
    ##---------------------------------------------------------------------------------------------##
    ## 블럭 만들기
    ##---------------------------------------------------------------------------------------------##
    def __createNewBlock(self):
        self.__B_Case = Case()
        self.__B_Case.setBlock(self.__prevBlock)
        self.__B_Case.setColor(self.__prevColor)
        self.__createPrevBlock()
        self.__screenUpdate()
    ##---------------------------------------------------------------------------------------------##
    ## 블럭 그리기
    ##---------------------------------------------------------------------------------------------##
    def __drawNewBlock(self):
        color = self.__B_Case.getColor()
        for x, y in self.__B_Case.getBlockPos():
            pg.draw.rect(self.__screen, color, [13 + (x*31), 13 + (y*31),30,30])
    ##---------------------------------------------------------------------------------------------##
    ## 블럭 밑으로 이동
    ##---------------------------------------------------------------------------------------------##
    def Move_Down(self):
        if self.__moveCollision(2):
            self.__B_Case.Move_Down()
        else:
            self.__inMap()
            self.__createNewBlock()
        self.__screenUpdate()
    ##---------------------------------------------------------------------------------------------##
    ## 블럭 왼쪽으로 이동
    ##---------------------------------------------------------------------------------------------##
    def Move_Left(self):
        if self.__moveCollision(0):
            self.__B_Case.Move_Left()
        self.__screenUpdate()
    ##---------------------------------------------------------------------------------------------##
    ## 블럭 오른쪽으로 이동
    ##---------------------------------------------------------------------------------------------##
    def Move_Right(self):
        if self.__moveCollision(1):
            self.__B_Case.Move_Right()
        self.__screenUpdate()
    ##---------------------------------------------------------------------------------------------##
    ## 블럭 회전
    ##---------------------------------------------------------------------------------------------##
    def Turnning(self):
        self.__B_Case.Turn()
        self.__Out_map_Check()
        self.__turnCollision()
        self.__screenUpdate()
    ##---------------------------------------------------------------------------------------------##
    ## 블럭 즉시 아래로
    ##---------------------------------------------------------------------------------------------##
    def instant_down(self):
        cnt = 0
        cnts = []
        x, y = self.__B_Case.getPos()
        for bx, by in self.__B_Case.getBlockPos():
            for j in range(by,20):
                if self.__Map[j][bx][0] != '1':
                    cnt += 1
                else :
                    break
            cnts.append(cnt)
            cnt = 0
        self.__B_Case.setPos(x, y+min(cnts)-1)
        self.__screenUpdate()
        self.__inMap()
        self.__createNewBlock()
    ##---------------------------------------------------------------------------------------------##
    ## 이동 충돌 검사 (0 : 좌, 1 : 우, 2 : 하)
    ##---------------------------------------------------------------------------------------------##
    def __moveCollision(self, dir):
        try:
            for x, y in self.__B_Case.getBlockPos():
                # 좌 검사
                if dir == 0:
                    if self.__Map[y][x-1][0] == '1':
                        return False
                # 우 검사
                elif dir == 1:
                    if self.__Map[y][x+1][0] == '1':
                        return False
                # 하 검사
                elif dir == 2:
                    if self.__Map[y+1][x][0] == '1':
                        return False
        except Exception :
            return False
        return True
    ##---------------------------------------------------------------------------------------------##
    ## 회전 충돌 검사
    ##---------------------------------------------------------------------------------------------##
    def __turnCollision(self):
        def collision():
            pos = self.__B_Case.getBlockPos()
            for x, y in pos:
                if self.__Map[y][x][0] == '1':
                    return True
            return False
        def out():
            pos = self.__B_Case.getBlockPos()
            for x, y in pos:
                if x < 0 or x > 9 or y < 0 or y > 19:
                    return True
            return False
        
        cx, cy = self.__B_Case.getPos()

        if (not collision()) and (not out()):
            return
        else:
            self.__B_Case.setPos(cx-1, cy)
            if (not collision()) and (not out()):
                return
            else :
                self.__B_Case.setPos(cx,cy-1)
                if (not collision()) and (not out()):
                    return
                else:
                    self.__B_Case.setPos(cx+1,cy)
                    if (not collision()) and (not out()):
                        return
                    else:
                        self.__B_Case.setPos(cx+1,cy)
                        if (not collision()) and (not out()):
                            return
                        else:
                            self.__B_Case.setPos(cx,cy+1)
                            if (not collision()) and (not out()):
                                return
                            else:
                                self.__B_Case.setPos(cx,cy)
                                self.__B_Case.Re_Turn()
    ##---------------------------------------------------------------------------------------------##
    ## 회전시 맵 밖으로 나갔을때, 맵 안으로 넣어주는 동작
    ##---------------------------------------------------------------------------------------------##
    def __Out_map_Check(self):
        # 케이스 좌표 불러오기
        cx, cy = self.__B_Case.getPos()
        # 블럭 좌표 불러오기
        temp_pos = self.__B_Case.getBlockPos()
        for x, y in temp_pos:
            if x < 0 :
                if self.__moveCollision(1):
                    self.Move_Right()
                else:
                    self.__B_Case.Re_Turn()
            elif x > 9:
                if self.__moveCollision(0):
                    self.Move_Left()
                else:
                    self.__B_Case.Re_Turn()
            elif y < 0:
                if self.__moveCollision(2):
                    self.Move_Down()
                else:
                    self.__B_Case.Re_Turn()
            elif y > 19:
                self.__B_Case.setPos(cx,cy-1)
    ##---------------------------------------------------------------------------------------------##
    ## Map에 블럭 고정
    ##---------------------------------------------------------------------------------------------##
    def __inMap(self):
        for x, y in self.__B_Case.getBlockPos():
            if self.__Map[y][x][0] != '1':
                self.__Map[y][x] = ('1', self.__B_Case.getColor())
        self.__check_line()
        self.__check_over()
    ##--------------------------------------------------------------------------------------------##
    ## 완성된 라인 제거
    ##--------------------------------------------------------------------------------------------##
    def __check_line(self):
        l = 19
        while(l != 0):
            cnt = 0
            for i in range(10):
                if self.__Map[l][i][0] == '1':
                    cnt += 1
            if cnt >= 10:
                for j in range(l,-1,-1):
                    if j == 0:
                        self.__Map[j] = [('0',(0)) for _ in range(10)]
                    else:
                        self.__Map[j] = self.__Map[j-1]
                l += 1
                self.__Score += 10
            elif cnt == 0:
                break
            l -= 1
        self.__screenUpdate()
    ##--------------------------------------------------------------------------------------------##
    ## GAME OVER 체크
    ##--------------------------------------------------------------------------------------------##
    def __check_over(self):
        for i in range(10):
            if self.__Map[0][i][0] == '1':
                self.__game_over = True

    ##--------------------------------------------------------------------------------------------##
    ## Game over 호출
    ##--------------------------------------------------------------------------------------------##
    def GAME_OVER(self):
        return self.__game_over
