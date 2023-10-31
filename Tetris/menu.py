import pygame as pg, time as t
# import RPi.GPIO as GPIO
from screeninfo import get_monitors as gm
from notice import Notice
##-------------------------------------------------------------------------------------------------##
## 메뉴 UI 클래스
##-------------------------------------------------------------------------------------------------##
class Menu:
    def __init__(self):
        # N = Notice()
        # N.run()
        pg.init()
        pg.display.set_caption('Tetris')

        # self.__up = 27
        # self.__down = 22
        # self.__center = 17
        # self.__left = 23
        # self.__right = 24

        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(self.__up,GPIO.IN)
        # GPIO.setup(self.__down,GPIO.IN)
        # GPIO.setup(self.__center,GPIO.IN)
        # GPIO.setup(self.__left,GPIO.IN)
        # GPIO.setup(self.__right,GPIO.IN)
        
        ## 모니터 정보 획득
        # self.__screenInfo = gm()
        ## 화면 정보 입력
        # self.__scrrenHeight, self.__screenWidth = self.__screenInfo[0].height, self.__screenInfo[0].width
        self.__scrrenHeight, self.__screenWidth = 600, 760
        self.__screenWidthHalf, self.__screenHeightHalf = self.__screenWidth//2,self.__scrrenHeight//2
        ## 전체 화면 모드
        # self.screen = pg.display.set_mode([self.__screenWidth, self.__scrrenHeight])
        self.screen = pg.display.set_mode([self.__scrrenHeight, self.__screenWidth])
        
        self.level = 1
        self.selected = 2
        self.playType = False
        self.fontSize = 75
        self.Levels = {1:'EASY',2:'NORMAL',3:'HARD'}
        self.Types = {False:'KeyBoard',True:'Motion'}
        self.font = pg.font.SysFont('malgungothic', self.fontSize)

        self.typeText = self.font.render(self.Types.get(self.playType), True, (255,255,255))
        self.levelText = self.font.render(self.Levels.get(self.level), True, (255,255,255))
        self.playText = self.font.render("PLAY", True, (255,255,255))
        self.quitText = self.font.render("QUIT", True, (255,255,255))

        self.rect_typeBox = pg.Rect((self.__screenWidthHalf-240, self.__screenHeightHalf-180, 315, 70))
        self.rect_levelBox = pg.Rect((self.__screenWidthHalf-240,self.__screenHeightHalf-40, 315,70))
        self.rect_playBox = pg.Rect((self.__screenWidthHalf-240,self.__screenHeightHalf+73, 315,70))
        self.rect_quitBox = pg.Rect((self.__screenWidthHalf-240,self.__screenHeightHalf+215, 315,70))

        self.selections = [(self.rect_typeBox, self.typeText),
                            (self.rect_levelBox, self.levelText),
                            (self.rect_playBox, self.playText),
                            (self.rect_quitBox, self.quitText)]
        self.update()
    ##---------------------------------------------------------------------------------------------##
    ## 화면 업데이트
    ##---------------------------------------------------------------------------------------------##
    def update(self):
        self.selections = [(self.rect_typeBox, self.typeText),
                            (self.rect_levelBox, self.levelText),
                            (self.rect_playBox, self.playText),
                            (self.rect_quitBox, self.quitText)]
        self.screen.fill((0,0,0))
        self.change_selection()
        # 난이도 조절시에만 화살표 표시
        if self.selected in [0, 1]:
            self.draw_arrow()
        self.draw_text()
        pg.display.flip()
    ##---------------------------------------------------------------------------------------------##
    ## 난이도 선택칸 화살표 그리기
    ##---------------------------------------------------------------------------------------------##
    def draw_arrow(self):
        box, text = self.selections[self.selected]
        xstartPos = box.centerx - text.get_width()//2
        ystartPos = box.centery - text.get_height()//2
        xendPos = xstartPos + text.get_width()
        yendPos = ystartPos + text.get_height()
        # 왼쪽 삼각형 좌표 ((선택지 x 시작값 - 35, 선택지 y 중간값 - 5),
        # (선택지 x 시작값 - 15, 선택지 y 시작값 + 10),
        # (선택지 x 시작값 - 15, 선택지 y 끝값 - 20))
        left_polygon = ((xstartPos - 50, box.centery),
                        (xstartPos - 15, ystartPos + 15),
                        (xstartPos - 15, yendPos - 10))
        # 오른쪽 삼각형 좌표 ((선택지 x 끝값 + 35, 선택지 y 중간값 + 5),
        # (선택지 x 끝값 + 15, 선택지 y 시작값 + 10),
        # (선택지 x 끝값 + 15, 선택지 y 끝값 - 20))
        right_polygon = ((xendPos +50, box.centery),
                        (xendPos + 15, ystartPos + 15),
                        (xendPos +15, yendPos - 10))
        
        if self.selected == 0:
            if not self.playType:
                pg.draw.polygon(self.screen, (255,255,255),right_polygon)
            elif self.playType:
                pg.draw.polygon(self.screen, (255,255,255),left_polygon)
        elif self.selected == 1:
            if self.level == 1:
                pg.draw.polygon(self.screen, (255,255,255),right_polygon)
            elif self.level == 2:
                pg.draw.polygon(self.screen, (255,255,255),left_polygon)
                pg.draw.polygon(self.screen, (255,255,255),right_polygon)
            elif self.level == 3:
                pg.draw.polygon(self.screen, (255,255,255),left_polygon)
    ##---------------------------------------------------------------------------------------------##
    ## Text 그리기
    ##---------------------------------------------------------------------------------------------##
    def draw_text(self):
        typePos = (self.rect_typeBox.centerx - self.typeText.get_width()//2,
                    self.rect_typeBox.centery - self.typeText.get_height()//2)
        levelPos = (self.rect_levelBox.centerx - self.levelText.get_width()//2, 
                    self.rect_levelBox.centery - self.levelText.get_height()//2)
        playPos = (self.rect_playBox.centerx - self.playText.get_width()//2,
                    self.rect_playBox.centery - self.playText.get_height()//2)
        quitPos = (self.rect_quitBox.centerx - self.quitText.get_width()//2,
                    self.rect_quitBox.centery - self.quitText.get_height()//2)
        self.screen.blit(self.typeText, typePos)
        self.screen.blit(self.levelText, levelPos)
        self.screen.blit(self.playText, playPos)
        self.screen.blit(self.quitText, quitPos)

    ##---------------------------------------------------------------------------------------------##
    ## 선택지 이동 그리기
    ##---------------------------------------------------------------------------------------------##
    def change_selection(self):
        self.levelText = self.font.render(self.Levels.get(self.level), True, (255,255,255))
        self.typeText = self.font.render(self.Types.get(self.playType), True, (255,255,255))
        box, text = self.selections[self.selected]
        selectionPos = ((box.centerx - text.get_width()//2)-5,
                        (box.centery - text.get_height()//2),
                        text.get_width()+10, text.get_height()+8)
        pg.draw.rect(self.screen, (255,255,255),selectionPos,2)

    ##---------------------------------------------------------------------------------------------##
    ## 메뉴 화면 실행
    ##---------------------------------------------------------------------------------------------##
    def run(self):
        pushed = 0
        while(True):
            # t.sleep(0.1)
            # if not(GPIO.input(self.__up)) and not(GPIO.input(self.__left)) and not(GPIO.input(self.__right)):
            #     return False
            # if not(GPIO.input(self.__up)) and pushed == 0:
            #     pushed = 1
            #     if self.selected == 0:
            #         self.selected = 1
            #     else:
            #         self.selected -= 1
            #     self.update()
            # elif not(GPIO.input(self.__down)) and pushed == 0:
            #     pushed = 1
            #     if self.selected == 1:
            #         self.selected = 0
            #     else :
            #         self.selected += 1
            #     self.update()
            # elif not(GPIO.input(self.__left)) and pushed == 0:
            #     pushed = 1
            #     if self.selected == 0:
            #         if self.level > 1:
            #             self.level -= 1
            #     self.update()
            # elif not(GPIO.input(self.__right)) and pushed == 0:
            #     pushed = 1
            #     if self.selected == 0:
            #         if self.level < 3:
            #             self.level += 1
            #     self.update()
            # elif not(GPIO.input(self.__center)) and pushed == 0:
            #     pushed = 1
            #     if self.selected == 1:
            #         return self.level
            #     elif self.selected == 2:
            #         return False
            # else:
            #     pushed = 0
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        return False
                    ## 위쪽키 입력 : 
                    if event.key == pg.K_UP:
                        if self.selected == 0:
                            self.selected = 3
                        else:
                            self.selected -= 1
                    if event.key == pg.K_DOWN:
                        if self.selected == 3:
                            self.selected = 0
                        else :
                            self.selected += 1
                    if event.key == pg.K_LEFT:
                        if self.selected == 0:
                            if self.playType:
                                self.playType = not self.playType
                        if self.selected == 1:
                            if self.level > 1:
                                self.level -= 1
                    if event.key == pg.K_RIGHT:
                        if self.selected == 0:
                            if not self.playType:
                                self.playType = not self.playType
                        if self.selected == 1:
                            if self.level < 3:
                                self.level += 1
                    if event.key == pg.K_SPACE:
                        if self.selected == 2:
                            return self.level, self.playType
                        elif self.selected == 3:
                            return False, False
            self.update()

if __name__ == '__main__':
    menu = Menu()
    value, t = menu.run()
    print(value, t)