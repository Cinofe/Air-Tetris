import pygame as pg
from screeninfo import get_monitors as gm
##-------------------------------------------------------------------------------------------------##
## 메뉴 UI 클래스
##-------------------------------------------------------------------------------------------------##
class Menu:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Tetris')
        self.__si = gm()
        self.__sh, self.__sw = self.__si[0].height, self.__si[0].width
        self.__hw, self.__hh = self.__sw//2,self.__sh//2
        print(self.__hw, self.__hh)
        self.screen = pg.display.set_mode([self.__sw, self.__sh],pg.FULLSCREEN)
        self.level = 1
        self.selected = 1
        self.fontSize = 200
        self.Levels = {1:'EASY',2:'NORMAL',3:'HARD'}
        self.font = pg.font.Font(None, self.fontSize)

        self.levelText = self.font.render(self.Levels.get(self.level), True, (255,255,255))
        self.playText = self.font.render("PLAY", True, (255,255,255))
        self.quitText = self.font.render("QUIT", True, (255,255,255))

        self.rect_levelBox = pg.Rect((self.__hw-160,self.__hh-220,315,70))
        self.rect_playBox = pg.Rect((self.__hw-160,self.__hh-87,315,70))
        self.rect_quitBox = pg.Rect((self.__hw-160,self.__hh+55,315,70))

        self.selections = [(self.rect_levelBox, self.levelText),
                            (self.rect_playBox, self.playText),
                            (self.rect_quitBox, self.quitText)]
        self.update()
    ##---------------------------------------------------------------------------------------------##
    ## 종료
    ##---------------------------------------------------------------------------------------------##
    def exit(self):
        self.doen = True
    ##---------------------------------------------------------------------------------------------##
    ## 화면 업데이트
    ##---------------------------------------------------------------------------------------------##
    def update(self):
        self.selections = [(self.rect_levelBox, self.levelText),
                            (self.rect_playBox, self.playText),
                            (self.rect_quitBox, self.quitText)]
        self.screen.fill((0,0,0))
        self.change_selection()
        # 난이도 조절시에만 화살표 표시
        if self.selected == 0:
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
        left_polygon = ((xstartPos - 35, box.centery - 5),
                        (xstartPos - 15, ystartPos + 10),
                        (xstartPos - 15, yendPos - 20))
        # 오른쪽 삼각형 좌표 ((선택지 x 끝값 + 35, 선택지 y 중간값 + 5),
        # (선택지 x 끝값 + 15, 선택지 y 시작값 + 10),
        # (선택지 x 끝값 + 15, 선택지 y 끝값 - 20))
        right_polygon = ((xendPos + 35, box.centery - 5),
                        (xendPos + 15, ystartPos + 10),
                        (xendPos +15, yendPos - 20))
        
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
        levelPos = (self.rect_levelBox.centerx - self.levelText.get_width()//2, 
                    self.rect_levelBox.centery - self.levelText.get_height()//2)
        playPos = (self.rect_playBox.centerx - self.playText.get_width()//2,
                    self.rect_playBox.centery - self.playText.get_height()//2)
        quitPos = (self.rect_quitBox.centerx - self.quitText.get_width()//2,
                    self.rect_quitBox.centery - self.quitText.get_height()//2)
        self.screen.blit(self.levelText, levelPos)
        self.screen.blit(self.playText, playPos)
        self.screen.blit(self.quitText, quitPos)

    ##---------------------------------------------------------------------------------------------##
    ## 선택지 이동 그리기
    ##---------------------------------------------------------------------------------------------##
    def change_selection(self):
        self.levelText = self.font.render(self.Levels.get(self.level), True, (255,255,255))
        box, text = self.selections[self.selected]
        selectionPos = ((box.centerx - text.get_width()//2)-5,
                        (box.centery - text.get_height()//2)-5,
                        text.get_width()+10, text.get_height()+3)
        pg.draw.rect(self.screen, (255,255,255),selectionPos,2)

    ##---------------------------------------------------------------------------------------------##
    ## 메뉴 화면 실행
    ##---------------------------------------------------------------------------------------------##
    def run(self):
        while(True):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False
                if event.type == pg.KEYDOWN:
                    # if event.key == pg.K_ESCAPE:
                    #     return False
                    if event.key == pg.K_q:
                        return False
                    if event.key == pg.K_UP:
                        if self.selected == 0:
                            self.selected = 1
                        else:
                            self.selected -= 1
                        self.update()
                    if event.key == pg.K_DOWN:
                        if self.selected == 1:
                            self.selected = 0
                        else :
                            self.selected += 1
                        self.update()
                    if event.key == pg.K_LEFT:
                        if self.selected == 0:
                            if self.level > 1:
                                self.level -= 1
                        self.update()
                    if event.key == pg.K_RIGHT:
                        if self.selected == 0:
                            if self.level < 3:
                                self.level += 1
                        self.update()
                    if event.key == pg.K_RETURN:
                        if self.selected == 1:
                            return self.level
                        elif self.selected == 2:
                            return False
            self.update()

if __name__ == '__main__':
    menu = Menu()
    value = menu.run()