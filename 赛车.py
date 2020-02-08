import pygame
from pygame.locals import *
import sys
import time
import random
WINDOW_WIDTH=600
WINDOW_HEIGHT=800
#期望FPS值
DEFAULT_FPS=60
#每次循环耗时
DEFAULT_DELAY=1.0/DEFAULT_FPS-0.002
#碰撞函数
def collide(r1,r2):
    #判断碰撞
    if r1.x>r2.x+r2.width:
        return False
    if r1.x+r1.width<r2.x:
        return False
    if r1.y > r2.y + r2.height:
        return False
    if r1.y + r1.height < r2.y:
        return False
    return True
#爆炸物定义
class Bomb:
    def __init__(self,window,x,y):
        self.window=window
        for i in range(1,14):
            self.imges=[]
            self.imges.append(pygame.image.load("img/image {}.png".format(i)))

        self.index=0
        self.img=self.imges[self.index]
        self.width=self.img.get_width()
        self.height=self.img.get_height()
        self.x=x
        self.y=y

        self.is_destroyed=False

    def display(self):
        if self.index>=len(self.imges):
            self.is_destroyed = True
            return
        self.img=self.imges[self.index]
        self.width=self.img.get_width()
        self.height=self.img.get_height()
        self.window.blit(self.img,(self.x,self.y))
        self.index+=1
        sound=pygame.mixer.Sound("snd/爆炸.wav")
        sound.play()

#定义陌生车辆
class StrangerCar:
    def __init__(self,window):
        self.window=window
        self.reset()
    #移动陌生车辆
    def move(self):
        self.y+=5
        if self.y>WINDOW_HEIGHT:
            self.reset()

    def display(self):
        self.window.blit(self.img,(self.x,self.y))
    def reset(self):
        self.img=pygame.image.load("img/car{}.png".format(random.randint(2,6)))
        #宽和高
        self.width=self.img.get_width()
        self.height=self.img.get_height()
        #位置
        self.x=random.choice((22, 177, 332,487))
        self.y = random.randint(-self.height*5,-self.height)
class PlayerCar:
    #属性
    def __init__(self,window):
        self.window=window
        self.img=pygame.image.load("img/car1.png")
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x=177
        self.y=500
    def display(self):
        self.window.blit(self.img,(self.x,self.y))
    def move_up(self):
        self.y-=10
        if self.y<0:
            self.y=0
    def move_down(self):
        self.y+=10
        if self.y>WINDOW_HEIGHT-self.height:
            self.y=WINDOW_HEIGHT-self.height
    def move_left(self):
        self.x-=155
        if self.x<22:
            self.x=22
    def move_right(self):
        self.x+=155
        if self.x>487:
            self.x=487
if __name__ == '__main__':
    # 初始化游戏框架
    pygame.init()
    #设置窗体大小
    window=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    #设置窗体title
    pygame.display.set_caption("黑马 飙车")
    #设置窗体图标
    pygame.display.set_icon(pygame.image.load("img/car1.png"))
    #真实的FPS
    fps=0
    #加载字体
    font=pygame.font.Font("font/happy.ttf",24)
    font_finish = pygame.font.Font("font/happy.ttf", 48)
    finish_txt=font_finish.render("游戏结束", True, (0, 0, 0))
    ft_width=finish_txt.get_width()
    ft_height=finish_txt.get_height()
    ft_x=(WINDOW_WIDTH-ft_width)/2
    ft_y = (WINDOW_HEIGHT - ft_height) / 2
    #加载我方车辆
    player=PlayerCar(window)
    #加载陌生车辆
    strangers=[]
    for i in range(4):
        strangers.append(StrangerCar(window))
    #爆炸物
    bombs=[]
    #播放背景音效
    pygame.mixer_music.load("snd/背景音效.wav")
    pygame.mixer_music.play(-1)
    #游戏结束
    is_over=False

    while True:
        # 加载背景图片
        imge = pygame.image.load("img/马路1.jpg")
        # 将背景图放到窗体上
        window.blit(imge, (0, 0))

        for bomb in bombs:
            bomb.display()
        # 刷新窗体
        pygame.display.flip()
        if is_over:
            window.blit(finish_txt, (ft_x, ft_y))
        if not is_over:

            #显示我方汽车
            player.display()
            #显示陌生汽车
            for stranger in strangers:
                stranger.display()
                stranger.move()
            #判断是否发生碰撞
            #陌生汽车矩形
            # stranger_rect=pygame.Rect(stranger.x,stranger.y,stranger.width,stranger.height)
            #我方汽车矩形
            player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
            for stranger in strangers:
                stranger_rect = pygame.Rect(stranger.x, stranger.y, stranger.width, stranger.height)
                if collide(player_rect,stranger_rect):
                    #我方飞机阵亡
                    bombs.append(Bomb(window,player.x-50,player.y))
                    #游戏暂停
                    is_over=True

        # 刷新窗体
        pygame.display.flip()
        #开始时间
        start=time.time()
        #窗体关闭事件
        events=pygame.event.get()
        for event in events:
            if event.type==QUIT:
                #窗体关闭
                pygame.quit()
                sys.exit(0)
            if event.type==KEYDOWN:
                if event.key==K_UP:
                    #汽车向上移动
                    player.move_up()
                if event.key==K_DOWN:
                    #汽车向下移动
                    player.move_down()
                if event.key==K_LEFT:
                    # 汽车向左移动
                    player.move_left()
                if event.key==K_RIGHT:
                    # 汽车向右移动
                    player.move_right()
                if event.key==K_1:
                    pygame.mixer_music.play(-1)
                if event.key==K_2:
                    pygame.mixer_music.stop()
                if event.key==K_RETURN and is_over:
                    #重置状态
                    for stranger in strangers:
                        stranger.reset()
                    is_over=False
        #长按事件
        keys=pygame.key.get_pressed()
        if keys[K_UP]:
            player.move_up()
        if keys[K_DOWN]:
            player.move_down()
        #结束时间
        end=time.time()
        #逻辑耗时
        cost=end-start
        if cost<DEFAULT_DELAY:
            sleep=DEFAULT_DELAY-cost
        else:
            sleep=0
        #睡眠
        time.sleep(sleep)
        end = time.time()
        fps=1.0/(end-start)