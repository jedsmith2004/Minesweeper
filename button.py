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


class OptionBox():

    def __init__(self, x, y, w, h, col, highlight_col, font, option_list, selected=0):
        self.col = col
        self.highlight_col = highlight_col
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.option_list = option_list
        self.selected = selected
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surf):
        pygame.draw.rect(surf, self.highlight_col if self.menu_active else self.col, self.rect)
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2)
        msg = self.font.render(self.option_list[self.selected], 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height
                pygame.draw.rect(surf, self.highlight_col if i == self.active_option else self.col, rect)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center=rect.center))
            outer_rect = (
            self.rect.x, self.rect.y + self.rect.height, self.rect.width, self.rect.height * len(self.option_list))
            pygame.draw.rect(surf, (0, 0, 0), outer_rect, 2)

    def update(self, events):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)

        self.active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.selected = self.active_option
                    self.draw_menu = False
                    return self.active_option
        return -1