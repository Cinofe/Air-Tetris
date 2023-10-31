import pygame as pg

## 게임 플레이 방법을 위한 간략한 설명
class Notice:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Tetris')

        self.__screenWidth, self.__scrrenHeight = 600, 760
        self.__screenWidthHalf, self.__screenHeightHalf = self.__screenWidth//2,self.__scrrenHeight//2

        self.screen = pg.display.set_mode([self.__screenWidth, self.__scrrenHeight])

        self.title = "필    독"
        self.explanations = [
            "플레이 방법 : ",
            "- 오른손 사용 필수",
            "- 오른쪽 이동 : 손바닥이 정면을 보게하여 손끝이 오른쪽",
            "- 왼쪽   이동 : 손등이 정면을 보게하여 손끝이 왼쪽",
            "- 블럭   회전 : 손바닥이 정면을 보게하여 손끝이 위로",
            "- 블럭 내리기 : 손등이 정면을 보게하여 손끝이 아래로",
            "- 메뉴   제어 : 키보드 방향키와 스페이스키를 눌러 조정",
            "- 모두 읽었다면 스페이스키를 눌러 게임 시작"
        ]
    
    def update(self):
        self.screen.fill((0,0,0))
        self.draw_text()
        pg.display.update()

    def draw_text(self):
        self.screen.blit(pg.font.SysFont('malgungothic',75).render(self.title, True, (255,255,255)),(self.__screenWidthHalf-130, 15))
        for i, explanation in enumerate(self.explanations):
            self.screen.blit(pg.font.SysFont('malgungothic',18).render(explanation, True, (255,255,255)),(self.__screenWidthHalf-240, 150+(50*(i+1))))

    def run(self):
        done = False
        while(not done):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        done = True
                    if event.key == pg.K_SPACE:
                        done = True
            self.update()