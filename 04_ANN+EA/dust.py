import pygame
class Dust:
    def __init__(self, dust_point ):
        self.dust_point = dust_point
        self.initial_position = # dust point posizioni in range 

def draw_dust(self, screen, is_cleaned):
    color = (0,255,255)
    if is_cleaned:
        color = (90,90,90)
    for dust in self.dust_point:
        pygame.draw.point(screen, color, self.round_Y(wall[0]), self.round_Y(wall[1]), 4)
