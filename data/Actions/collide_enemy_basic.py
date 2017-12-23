import pygame
from pygame.locals import *
import os

def collision(me, collider, settings, game, damage):
    if collider.name == 'Player':
        collider.take_damage(damage)
    if me.rect.collidepoint(collider.rect.midbottom):
        col_side = 'bottom'
        while me.rect.colliderect(collider.rect):
            collider.rect.y -= me.rect.h
            collider.rect.x -= me.rect.w
    elif me.rect.collidepoint(collider.rect.midtop):
        col_side = 'top'
        while me.rect.colliderect(collider.rect):
            collider.rect.y += me.rect.h
    elif me.rect.collidepoint(collider.rect.midleft):
        col_side = 'left'
        while me.rect.colliderect(collider.rect):
            collider.rect.x += me.rect.w
    elif me.rect.collidepoint(collider.rect.midright):
        col_side = 'right'
        while me.rect.colliderect(collider.rect):
            collider.rect.x -= me.rect.w
