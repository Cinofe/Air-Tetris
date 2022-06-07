import pygame as pg
from screeninfo import get_monitors as gm

class Notice:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Tetris')
        self.__si = gm()
        self.__sh, self.__sw = self.__si[0].height, self.__si[0].width
        self.__hw, self.__hh = self.__sw//2,self.__sh//2
        # self.screen = pg.display.set_mode([self.__sw, self.__sh],pg.FULLSCREEN)
        self.screen = pg.display.set_mode([500,500])

        self.title = "필    독"
        self.explanation = [
            "플레이 방법",
            "오른손 사용 필수",
            "손가락을 모두 붙인 상태에서",
            "손바닥이 정면을 보게하여",
            "손끝을 위로 향하게 하면",
            "블럭이 회전",
            "손등이 정면을 보게하여",
            "손끝을 아래로 향하게 하면",
            "블럭이 즉시 바닥으로 내려감",
            "손바닥이 정면을 보게하여",
            "손끝을 오른쪽으로 향하게 하면",
            "블럭이 오른쪽으로 이동",
            "손등이 정면을 보게하여",
            "손끝이 왼쪽을 향하게 하면",
            "블럭이 왼쪽으로 이동",
            "모두 읽었다면 초록 버튼 누르기"
        ]
    def update(self):
        self.screen.fill((0,0,0))
        self.draw_text()
        pg.display.update()

    def draw_text(self):
        self.screen.blit(pg.font.SysFont('malgungothic',80).render(self.title, True, (255,255,255)),(100,100))

    def run(self):
        while(True):
            self.update()


if __name__== "__main__":
    notice=Notice()
    notice.run()
