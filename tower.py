import pygame
import os
import math
from enemy import Enemy, EnemyGroup
TOWER_IMAGE = pygame.image.load(os.path.join("images", "rapid_test.png"))


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def collide(self, enemy):
        """
        Q2.2)check whether the enemy is in the circle (attack range), if the enemy is in range return True
        :param enemy: Enemy() object
        :return: Bool
        """
        en_x, en_y = enemy.get_pos()
        x, y = self.center

        if((en_x - x)**2) + ((en_y-y)**2) < (self.radius**2):
            return True
        return False
        """
        Hint:
        x1, y1 = enemy.get_pos()
        ...
        """


    def draw_transparent(self, win):
        """
        Q1) draw the tower effect range, which is a transparent circle.
        :param win: window surface
        :return: None
        """
        # create a transparent surface area = 2R*2R
        transparent_surface = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        # define transparency: 0~255, 0 is fully transparent
        transparency = 125
        # draw the circle on the transparent surface
        #                                       (r, g, b, transparency), (x, y)of the surface, not the win, radius)
        pygame.draw.circle(transparent_surface, (169,169,169, transparency), (self.radius,self.radius), self.radius )
        x, y = self.center
        #                            make sure that the circle is in the center
        win.blit(transparent_surface,(x-self.radius, y-self.radius))

        """
        other sol.
        to print the transparent surface on the whole screen
        no need to change the centers of different surfaces
        """

class Tower:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(TOWER_IMAGE, (70, 70))  # image of the tower
        self.rect = self.image.get_rect()#(x,y,width,hieght)
        self.rect.center = (x, y)  # center of the tower
        self.range = 150  # tower attack range
        self.damage = 2   # tower damage
        self.range_circle = Circle(self.rect.center, self.range)  # attack range circle (class Circle())
        self.cd_count = 0  # used in self.is_cool_down()
        self.cd_max_count = 60  # used in self.is_cool_down()
        self.is_selected = True # the state of whether the tower is selected
        self.type = "tower"

    def is_cool_down(self):
        """
        Q2.1) Return whether the tower is cooling down
        (1) Use a counter to computer whether the tower is cooling down (( self.cd_count
        :return: Bool
        """
        if self.cd_count< self.cd_max_count:
            self.cd_count += 1
            return False
        else:
            # initialize to wait for another 120 frames
            self.cd_count = 0
            return True

     """
          Hint:
          let counter be 0
          if the counter < max counter then
              set counter to counter + 1
          else 
              counter return to zero
          end if
            """



    def attack(self, enemy_group):
        # 先到 enenmy.py 讀 class enemygroup method get 裡的資料([enemy(), enemy(),...])
        # 再傳回給 tower.py 中 circle class 中的collide method，他需要enemy這個函數去判斷位置
        for en in enemy_group.get():
            if self.is_cool_down() == True and Circle(self.rect.center, self.range).collide(en) == True:
                en.get_hurt(self.damage)
                break
        # break和continue的差別？？continue還會再讀一次，break直接離開迴圈
        """
        Q2.3) Attack the enemy.
        (1) check the the tower is cool down ((self.is_cool_down()
        (2) if the enemy is in attack range, then enemy get hurt. ((Circle.collide(), enemy.get_hurt()
        :param enemy_group: EnemyGroup()
        :return: None
        """



    def is_clicked(self, x, y):
        """
        Bonus) Return whether the tower is clicked
        (1) If the mouse position is on the tower image, return True
        :param x: mouse pos x
        :param y: mouse pos y
        :return: Bool
        """
        #參考main裡collide_base來的
        tw_x, tw_y = self.rect.center
        width, height = self.rect.w, self.rect.h
        if tw_x - width // 2 < x < tw_x + width // 2 and tw_y - height // 2 < y < tw_y + height // 2:
            return True
        return False



    def get_selected(self, is_selected):
        """
        Bonus) Change the attribute self.is_selected
        :param is_selected: Bool
        :return: None
        """
        self.is_selected = is_selected

    def draw(self, win):
        """
        Draw the tower and the range circle
        :param win:
        :return:
        """
        # draw range circle
        if self.is_selected:
            self.range_circle.draw_transparent(win)
        # draw tower
        win.blit(self.image, self.rect)


class TowerGroup:
    def __init__(self):
        self.constructed_tower = [Tower(250, 380), Tower(420, 400), Tower(600, 400)]

    def get(self):
        return self.constructed_tower

