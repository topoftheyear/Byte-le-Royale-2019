import math

import pygame

class HealthBar(pygame.sprite.Sprite):

    def __init__(self, x, y, w, h, unit_id, unit=False):
        super().__init__()
        self.unit_id = unit_id

        self.max_health = 0
        self.current_health = 0

        self.unit_hp_bar = unit

        if self.unit_hp_bar:
            self.max_focus = 0
            self.current_focus = 0

            self.max_will = 0
            self.current_will = 0

        self.font_obj = pygame.font.Font('game/visualizer/assets/joystix/joystix monospace.ttf', 12)

        self.rect = pygame.Rect(x, y, w, h)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)

    def update(self, units):

        unit = self.get_unit(units)

        if unit is None: # couldn't find a valid unit
            return

        updates = False

        # Update health
        if unit.health is not self.max_health:
            self.max_health = unit.health
            updates = True

        if unit.current_health is not self.current_health:
            self.current_health = unit.current_health
            updates = True

        if self.unit_hp_bar:

            # Update Focus
            if unit.focus is not self.max_focus:
                self.max_focus = unit.focus
                updates = True

            if unit.current_focus is not self.current_focus:
                self.current_focus = unit.current_focus
                updates = True

            # Update Focus
            if unit.will is not self.max_will:
                self.max_will = unit.will
                updates = True

            if unit.current_will is not self.current_will:
                self.current_will = unit.current_will
                updates = True

        if updates:

            # render text
            self.text_surf = self.font_obj.render('HP:{0}'.format(
                str(self.current_health).rjust(6, "0")), True, pygame.Color("#2a2b2b"))

            text_rect = self.text_surf.get_rect()

            #Choose where to draw the amount of HP left
            text_rect.topleft = (4, 3)
            self.image.fill(pygame.Color("#DEDEDE"), (0, 1, 300, 20))
            self.image.blit(self.text_surf, text_rect)

            #Draw health bars
            self.image.fill(pygame.Color("#FFFFFF"),(96, 2, 202, 18))
            self.image.fill(pygame.Color("#FF0000"),(97, 3, 200, 16))
            self.image.fill(pygame.Color("#33BF00"),(97, 3, math.floor((self.current_health/float(self.max_health))*200), 16))

            if self.unit_hp_bar:

                self.image.fill(pygame.Color("#DEDEDE"), (95, 20, 300, 20))

                # draw focus bar
                text_surf = self.font_obj.render('F:', True, pygame.Color("#2a2b2b"))
                text_surf_rect = text_surf.get_rect()
                text_surf_rect.topleft = (100, 20)
                self.image.blit(text_surf, text_surf_rect)

                self.image.fill(pygame.Color("#BDB0FF"), (120, 20, 75, 16))
                self.image.fill(pygame.Color("#4F2BFF"), (120, 20, math.floor((self.current_focus/float(self.max_focus))*75), 16))

                # draw will bar
                text_surf = self.font_obj.render('W:', True, pygame.Color("#2a2b2b"))
                text_surf_rect = text_surf.get_rect()
                text_surf_rect.topleft = (200, 20)
                self.image.blit(text_surf, text_surf_rect)

                self.image.fill(pygame.Color("#FFBF75"), (222, 20, 75, 16))
                self.image.fill(pygame.Color("#FF8800"), (222, 20, math.floor((self.current_will/float(self.max_will))*75), 16))

    def get_unit(self, units):
        for unit in units:
            if unit.id == self.unit_id:
                return unit
        return None
