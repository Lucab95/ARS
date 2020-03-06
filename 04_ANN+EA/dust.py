import pygame
import numpy as np
class Dust:
    def __init__(self, dust_point, size_screen):
        self.dust_point = dust_point
        self.dusts = self.initialize_dust(dust_point,size_screen)
        # self.initial_position = # dust point posizioni in range

    def draw_dust(self, screen):
        for idx, dust in enumerate(self.dusts):
            # print(dust[1], idx)
            color = (0, 255, 100)
            if dust[1] == True:
                color=(90,90,255)
            pygame.draw.rect(screen,color,( dust[0][0], dust[0][1], 5,5))

    def initialize_dust(self, dust_point,size_screen):
        dusts = []
        line_dust = int(dust_point / 10)
        dust_finish_x = size_screen[0]
        dust_finish_y = size_screen[1]
        dust_init_x = 40
        step_x = int((dust_finish_x - 40) / line_dust)
        step_y = int((dust_finish_y - 40)/line_dust)
        for i in range(line_dust):
            dust_init_y = 40
            x_dust = dust_init_x + i * step_x
            for i in range(line_dust):
                y_dust = dust_init_y + i * step_y
                dusts.append([(x_dust, y_dust),False])
        return dusts


    def reached(self,index):
        # print (self.dusts[75][1])
        # print (index)
        self.dusts[index][1]=True

    def get_dust(self):
        return self.dusts;
