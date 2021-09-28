import math
import pygame


class Button():
    def __init__(self, pos=(0,0), shape='rect', col=(180,180,180), hoverCol=(140,140,140),clickedCol=(0,0,0),
                 radius=None, width=25, height=20, text=None, icon=None, border=False, borderCol=(180,180,180),
                 borderWidth=2, clickEvent=None, adjustments=(0.0, 0.0),textSize=10):
        self.pos = pos
        self.shape = shape
        self.originalCol, self.col = col, col
        self.hoverCol = hoverCol
        self.clickedCol = clickedCol
        if radius == None: self.radius = max(width,height)
        else: self.radius = radius
        self.width = width
        self.height = height
        self.hoverBool = False
        self.clickedBool = False
        self.icon = icon
        self.text = text
        self.border = border
        self.borderCol = borderCol
        self.borderWidth = borderWidth
        self.clickEvent = clickEvent
        self.adjustments = adjustments
        self.textSize = textSize

    def draw(self,win):
        if self.shape == 'rect':
            if self.border: pygame.draw.rect(win,self.borderCol,(self.pos[0]-self.borderWidth,
                self.pos[1]-self.borderWidth,self.width + self.borderWidth*2,self.height + self.borderWidth*2))
            pygame.draw.rect(win,self.col,(self.pos[0],self.pos[1],self.width,self.height))
            if self.icon != None:
                icon = pygame.transform.scale(pygame.image.load(self.icon).convert(),(self.width, self.height))
                if self.hoverBool:
                    icon.fill(
                    (round(self.hoverCol[0] * 0.25), round(self.hoverCol[1] * 0.25),round(self.hoverCol[2] * 0.25)),
                    special_flags=pygame.BLEND_SUB)
                win.blit(icon,(self.pos[0], self.pos[1], self.width, self.height))
            elif self.text != None:
                font = pygame.font.SysFont("",self.radius//self.textSize)
                text = font.render(self.text,True,(75,75,75))
                win.blit(text,(self.pos[0]+self.width*self.adjustments[0],self.pos[1]+self.height*self.adjustments[1]))
        elif self.shape == 'square':
            if self.border: pygame.draw.rect(win, self.borderCol, (self.pos[0]-self.borderWidth,
                self.pos[1]-self.borderWidth, self.radius + self.borderWidth*2, self.radius + self.borderWidth*2))
            pygame.draw.rect(win, self.col, (self.pos[0], self.pos[1], self.radius, self.radius))
            if self.icon != None:
                icon = pygame.transform.scale(pygame.image.load(self.icon).convert(), (self.radius, self.radius))
                if self.hoverBool:
                    icon.fill(
                            (round(self.hoverCol[0]*0.25),round(self.hoverCol[1]*0.25),round(self.hoverCol[2]*0.25)),
                            special_flags=pygame.BLEND_SUB)
                win.blit(icon,(self.pos[0], self.pos[1]))
            elif self.text != None:
                font = pygame.font.SysFont("",self.radius)
                text = font.render(self.text,True,(0,0,0))
                win.blit(text,(self.pos[0]-self.radius/1.15,self.pos[1]-self.radius/3.3))
        elif self.shape == 'circle':
            if self.border: pygame.draw.circle(win,self.borderCol,self.pos,self.radius+self.borderWidth)
            pygame.draw.circle(win,self.col,self.pos,self.radius)
            if self.icon != None:
                icon = pygame.image.load(self.icon).convert()
                win.blit(icon,(self.pos[0]-self.radius, self.pos[1]-self.radius, self.radius,self.radius))
            elif self.text != None:
                font = pygame.font.SysFont("",self.radius)
                text = font.render(self.text,True,(0,0,0))
                win.blit(text,(self.pos[0]-self.radius/1.15,self.pos[1]-self.radius/3.3))

    def hover(self, mousePos):
        if math.hypot(mousePos[0]-self.pos[0], mousePos[1]-self.pos[1]) < self.radius \
                and self.shape == 'circle': self.hoverBool = True
        elif mousePos[0] > self.pos[0] and mousePos[1] > self.pos[1] and self.shape == 'rect' \
                and mousePos[0] < self.pos[0] + self.width \
                and mousePos[1] < self.pos[1] + self.height: self.hoverBool = True
        elif mousePos[0] > self.pos[0] and mousePos[1] > self.pos[1] and self.shape == 'square' \
                and mousePos[0] < self.pos[0] + self.radius \
                and mousePos[1] < self.pos[1] + self.radius: self.hoverBool = True
        else: self.hoverBool = False
        if self.hoverBool: self.col = self.hoverCol
        else: self.col = self.originalCol

    def clicked(self, mousePos):
        if math.hypot(mousePos[0]-self.pos[0], mousePos[1]-self.pos[1]) < self.radius \
                and self.shape == 'circle': self.clickedBool = True
        elif mousePos[0] > self.pos[0] and mousePos[1] > self.pos[1]and self.shape == 'rect' \
                and mousePos[0] < self.pos[0] + self.width \
                and mousePos[1] < self.pos[1] + self.height: self.clickedBool = True
        elif mousePos[0] > self.pos[0] and mousePos[1] > self.pos[1] and self.shape == 'square' \
                and mousePos[0] < self.pos[0] + self.radius \
                and mousePos[1] < self.pos[1] + self.radius: self.clickedBool = True
        else: self.clickedBool = False
        if self.clickedBool:
            self.col = self.clickedCol
            return eval(self.clickEvent+'()')
        else: self.col = self.originalCol