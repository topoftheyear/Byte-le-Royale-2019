import random, math

import pygame
import ptext

from game.visualizer.spritesheet_functions import SpriteSheet
from game.common.enums import *


class DamageIconSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_data, x, y):
        super().__init__()

        sprite_sheet = SpriteSheet("game/visualizer/assets/damage_type_icons.png")

        self.h = 32
        self.w = 32

        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3])

        self.image = pygame.transform.scale(self.image, (self.h*2, self.w*2))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class PiercingIconSprite(DamageIconSprite):
    def __init__(self, x, y):
        super().__init__([
            0, DamageType.piercing * 32,
            32, 32
        ], x, y)

class SlashingIconSprite(DamageIconSprite):
    def __init__(self, x, y):
        super().__init__([
            0, DamageType.slashing * 32,
            32, 32
        ], x, y)

class BludgeoningIconSprite(DamageIconSprite):
    def __init__(self, x, y):
        super().__init__([
            0, DamageType.bludgeoning * 32,
            32, 32
        ], x, y)

class PrecisionIconSprite(DamageIconSprite):
    def __init__(self, x, y):
        super().__init__([
            0, DamageType.precision * 32,
            32, 32
        ], x, y)

class FireIconSprite(DamageIconSprite):
    def __init__(self, x, y):
        super().__init__([
            0, DamageType.fire * 32,
            32, 32
        ], x, y)

class ColdIconSprite(DamageIconSprite):
    def __init__(self, x, y):
        super().__init__([
            0, DamageType.cold * 32,
            32, 32
        ], x, y)

class ElectricityIconSprite(DamageIconSprite):
    def __init__(self, x, y):
        super().__init__([
            0, DamageType.electricity * 32,
            32, 32
        ], x, y)

class AcidIconSprite(DamageIconSprite):
    def __init__(self, x, y):
        super().__init__([
            0, DamageType.acid * 32,
            32, 32
        ], x, y)

class SonicIconSprite(DamageIconSprite):
    def __init__(self, x, y):
        super().__init__([
            0, DamageType.sonic * 32,
            32, 32
        ], x, y)

class ForceIconSprite(DamageIconSprite):
    def __init__(self, x, y):
        super().__init__([
            0, DamageType.force * 32,
            32, 32
        ], x, y)


def get_damage_type_icon(damage_type, pos):
    cls = None

    if damage_type is DamageType.piercing:
        cls = PiercingIconSprite
    elif damage_type is DamageType.slashing:
        cls = SlashingIconSprite
    elif damage_type is DamageType.bludgeoning:
        cls = BludgeoningIconSprite
    elif damage_type is DamageType.precision:
        cls = PrecisionIconSprite
    elif damage_type is DamageType.fire:
        cls = FireIconSprite
    elif damage_type is DamageType.cold:
        cls = ColdIconSprite
    elif damage_type is DamageType.electricity:
        cls = ElectricityIconSprite
    elif damage_type is DamageType.acid:
        cls = AcidIconSprite
    elif damage_type is DamageType.sonic:
        cls = SonicIconSprite
    elif damage_type is DamageType.force:
        cls = ForceIconSprite

    if cls is None:
        return None

    return cls(*pos)


class UnitIconSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_data, x, y):
        super().__init__()

        sprite_sheet = SpriteSheet("game/visualizer/assets/unit_class_icons.png")

        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3])

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class KnightIconSprite(UnitIconSprite):
    def __init__(self, x, y):
        UnitIconSprite.__init__(self, [
            0, UnitClass.knight * 32,
            32, 32
        ], x, y)


class BrawlerIconSprite(UnitIconSprite):
    def __init__(self, x, y):
        UnitIconSprite.__init__(self, [
            0, UnitClass.brawler * 32,
            32, 32
        ], x, y)

class PikemanIconSprite(UnitIconSprite):
    def __init__(self, x, y):
        UnitIconSprite.__init__(self, [
            0, UnitClass.pikeman * 32,
            32, 32
        ], x, y)

class RogueIconSprite(UnitIconSprite):
    def __init__(self, x, y):
        UnitIconSprite.__init__(self, [
            0, UnitClass.rogue * 32,
            32, 32
        ], x, y)

class MagusIconSprite(UnitIconSprite):
    def __init__(self, x, y):
        UnitIconSprite.__init__(self, [
            0, UnitClass.magus * 32,
            32, 32
        ], x, y)

class WizardIconSprite(UnitIconSprite):
    def __init__(self, x, y):
        UnitIconSprite.__init__(self, [
            0, UnitClass.wizard * 32,
            32, 32
        ], x, y)

class SorcererIconSprite(UnitIconSprite):
    def __init__(self, x, y):
        UnitIconSprite.__init__(self, [
            0, UnitClass.sorcerer * 32,
            32, 32
        ], x, y)

class AlchemistIconSprite(UnitIconSprite):
    def __init__(self, x, y):
        UnitIconSprite.__init__(self, [
            0, UnitClass.alchemist * 32,
            32, 32
        ], x, y)

class IconBackSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        sprite_sheet = SpriteSheet("game/visualizer/assets/icon_back.png")

        self.image = sprite_sheet.get_image(0, 0, 40, 40)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class MonsterSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_path, frames, x, y, h, w, animation_speed):
        super().__init__()

        self.frames = frames
        self.index = 0
        self.tick_counter = 0
        self.animation_speed = animation_speed

        self.h = h
        self.w = w

        self.sprite_sheet = SpriteSheet(sprite_sheet_path)

        self.image = self.sprite_sheet.get_image(
                                                self.frames[self.index][0],
                                                self.frames[self.index][1],
                                                self.h,
                                                self.w
                                                )

        self.image = pygame.transform.scale(self.image, (self.h*2, self.w*2))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.tick_counter += 1
        if self.tick_counter % self.animation_speed is 0:
            if self.index < len(self.frames)-1:
                self.index += 1
            else:
                self.index = 0
        self.image = self.sprite_sheet.get_image(
                                                self.frames[self.index][0],
                                                self.frames[self.index][1],
                                                self.h,
                                                self.w
                                                )

        self.image = pygame.transform.scale(self.image, (self.h*2, self.w*2))

class BeholderSprite(MonsterSprite):
    def __init__(self, x, y):
        MonsterSprite.__init__(self, "game/visualizer/assets/beholder.png", [
            [0, 0],
            [136, 0],
            [0, 136],
            [136, 136]
        ], x, y, 136, 136, 3)

class SlimeSprite(MonsterSprite):
    def __init__(self, x, y):
        MonsterSprite.__init__(self, "game/visualizer/assets/slime.png", [
            [0, 0],
            [128, 0],
            [256,0],
            [384,0],
            [0, 128],
            [128,128],
            [256,128],
            [384,128],
            [0,256],
            [128,256],
            [256,256],
            [384,256],
            [0,384],
            [128,384],
        ], x, y, 128, 128,2)

class MinotaurSprite(MonsterSprite):
    def __init__(self, x, y):
        MonsterSprite.__init__(self, "game/visualizer/assets/minotaur.png", [
            [0, 0],
            [128, 0],
            [256,0],
            [384,0],
            [0, 128],
            [128,128],
            [256,128],
            [384,128],
            [0,256],
            [128,256],
            [256,256],
            [384,256],
            [0,384],
            [128,384],
            [256,384],
            [384,384]
        ], x, y, 128, 128, 3)

class DragonSprite(MonsterSprite):
    def __init__(self, x, y):
        MonsterSprite.__init__(self, "game/visualizer/assets/dragon.png", [
            [0, 0],
            [128, 0],
            [256,0],
            [384,0],
            [512,0],
            [0, 128],
            [128,128],
            [256,128],
            [384,128],
            [512,128],
            [0,256],
            [128,256],
            [256,256],
            [384,256],
            [512,256],
            [0,384],
            [128,384],
            [256,384],
            [384,384],
            [512,384],
            [0,512],
            [128,512],
            [256,512]
        ], x, y, 128, 128,3)

class WraithSprite(MonsterSprite):
    def __init__(self, x, y):
        MonsterSprite.__init__(self, "game/visualizer/assets/wraith.png", [
            [0, 0],
            [128, 0],
            [256,0],
            [384,0],
            [512,0],
            [0, 128],
            [128,128],
            [256,128],
            [384,128],
            [512,128],
            [0,256],
            [128,256],
            [256,256],
            [384,256],
            [512,256],
            [0,384],
            [128,384],
            [256,384],
            [384,384],
            [512,384],
            [0,512],
            [128,512],
            [256,512],
            [384,512],
            [512,512],
            [0,640],
            [128,640],
            [256,640],
            [384,640],
            [512,640]
        ], x, y, 128, 128,4)

class WispSprite(MonsterSprite):
    def __init__(self, x, y):
        MonsterSprite.__init__(self, "game/visualizer/assets/wisp.png", [
            [0, 0],
            [128, 0],
            [256,0],
            [384,0],
            [512,0],
            [0, 128],
            [128,128],
            [256,128],
            [384,128],
            [512,128],
            [0,256],
            [128,256],
            [256,256],
            [384,256],
            [512,256],
            [0,384],
            [128,384],
            [256,384],
            [384,384],
            [512,384],
            [0,512],
            [128,512],
            [256,512],
            [384,512]
        ], x, y, 128, 128,3)


class VampireSprite(MonsterSprite):
    def __init__(self, x, y):
        MonsterSprite.__init__(self, "game/visualizer/assets/vampire.png", [
            [0,   0], [128,   0], [256,   0], [384,   0], [512,   0], [640,   0],
            [0, 128], [128, 128], [256, 128], [384, 128], [512, 128], [640, 128],
            [0, 256], [128, 256], [256, 256], [384, 256], [512, 256], [640, 256],
            [0, 384], [128, 384], [256, 384], [384, 384], [512, 384], [640, 384],
            [0, 512], [128, 512], [256, 512], [384, 512], [512, 512], [640, 512],
            [0, 512], [128, 512]

        ], x, y, 128, 128, 2)

def get_monster_sprite(monster_type, pos):
    if monster_type is MonsterType.beholder:
        return BeholderSprite(*pos)
    elif monster_type is MonsterType.slime:
        return SlimeSprite(*pos)
    elif monster_type is MonsterType.minotaur:
        return MinotaurSprite(*pos)
    elif monster_type is MonsterType.dragon:
        return DragonSprite(*pos)
    elif monster_type is MonsterType.wraith:
        return WraithSprite(*pos)
    elif monster_type is MonsterType.wisp:
        return WispSprite(*pos)
    elif monster_type is MonsterType.vampire:
        return VampireSprite(*pos)


class BackgroundSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_path, frames, x, y, h, w, animation_speed):
        super().__init__()

        self.frames = frames
        self.index = 0
        self.tick_counter = 0
        self.animation_speed = animation_speed

        self.h = h
        self.w = w

        self.sprite_sheet = SpriteSheet(sprite_sheet_path)

        self.image = self.sprite_sheet.get_image(
                                                self.frames[self.index][0],
                                                self.frames[self.index][1],
                                                self.h,
                                                self.w
                                                )

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.tick_counter += 1
        if self.tick_counter % self.animation_speed is 0:
            if self.index < len(self.frames)-1:
                self.index += 1
            else:
                self.index = 0
        self.image = self.sprite_sheet.get_image(
                                                self.frames[self.index][0],
                                                self.frames[self.index][1],
                                                self.h,
                                                self.w
                                                )

class TownShopSprite(BackgroundSprite):
    def __init__(self):
        BackgroundSprite.__init__(self, "game/visualizer/assets/town_shop.png", [
            [ 0,    0 ],
            [ 1280, 0 ],
            [ 0,    720 ],
            [ 1280, 720 ],
        ], 0, 0, 1280, 720, 3)

class BrownDungeonSprite(BackgroundSprite):
    def __init__(self):
        BackgroundSprite.__init__(self, "game/visualizer/assets/monster_room.png", [
            [ 0, 0 ],
        ], 0, 0, 1280, 720, 1)

class GreyDungeonSprite(BackgroundSprite):
    def __init__(self):
        BackgroundSprite.__init__(self, "game/visualizer/assets/monster_room_1.png", [
            [ 0, 0 ],
        ], 0, 0, 1280, 720, 1)

class OrangeDungeonSprite(BackgroundSprite):
    def __init__(self):
        BackgroundSprite.__init__(self, "game/visualizer/assets/monster_room_2.png", [
            [ 0, 0 ],
        ], 0, 0, 1280, 720, 1)

class GreenDungeonSprite(BackgroundSprite):
    def __init__(self):
        BackgroundSprite.__init__(self, "game/visualizer/assets/monster_room_3.png", [
            [ 0, 0 ],
        ], 0, 0, 1280, 720, 1)

class HillSprite(BackgroundSprite):
    def __init__(self):
        BackgroundSprite.__init__(self, "game/visualizer/assets/hill.png", [
            [ 0, 0 ],
        ], 0, 0, 1280, 720, 1)

loaded_monster_room_sprites = {}

def get_room_sprite():
    cls = random.choice([
        BrownDungeonSprite,
        GreyDungeonSprite,
        OrangeDungeonSprite,
        GreenDungeonSprite
    ])

    if cls not in loaded_monster_room_sprites:
        loaded_monster_room_sprites[cls] = cls()
    return loaded_monster_room_sprites[cls]


class AttackAnimation(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()

        self.frames = [
			[0,0],
			[128, 0],
			[0, 128],
			[128, 128],
            [0, 256],
            [128, 256]

		]
        self.index = 0
        self.tick_counter = 0
        self.animation_speed = 1

        self.h = 128
        self.w = 128

        self.color = color

        self.sprite_sheet = SpriteSheet("game/visualizer/assets/attack.png")

        self.image = self.sprite_sheet.get_image(
                                                self.frames[self.index][0],
                                                self.frames[self.index][1],
                                                self.h,
                                                self.w
                                                )

        pa = pygame.PixelArray(self.image)
        pa.replace(pygame.Color(0, 0, 0, 255), self.color)
        del pa


        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, group):
        self.tick_counter += 1
        if self.tick_counter % self.animation_speed is 0:
            if self.index < len(self.frames)-1:
                self.index += 1
            else:
                del self.image
                group.remove(self)

        self.image = self.sprite_sheet.get_image(
                                                self.frames[self.index][0],
                                                self.frames[self.index][1],
                                                self.h,
                                                self.w
                                                )
        pa = pygame.PixelArray(self.image)
        pa.replace(pygame.Color(255, 255, 255, 255), self.color)
        d = 60
        r = self.color.r if self.color.r-d < 0 else self.color.r-d
        g = self.color.g if self.color.g-d < 0 else self.color.g-d
        b = self.color.b if self.color.b-d < 0 else self.color.b-d
        pa.replace(pygame.Color("#a5a5a5"), pygame.Color ( r, g, b, 255))
        del pa

class MagicAttackAnimation(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.frames = [
            [  0,   0], [128,   0], [256,   0], [384,   0],
            [  0, 128], [128, 128], [256, 128], [384, 128],
            [  0, 256], [128, 256], [256, 256], [384, 256],
            [  0, 384]
        ]

        self.index = 0
        self.tick_counter = 0
        self.animation_speed = 1

        self.h = 128
        self.w = 128


        self.sprite_sheet = SpriteSheet("game/visualizer/assets/explosion_animation.png")

        self.image = self.sprite_sheet.get_image(
            self.frames[self.index][0],
            self.frames[self.index][1],
            self.h,
            self.w
        )

        self.color = pygame.Color(
            color.r,
            color.g,
            color.b,
            255
        )

        d = 60
        self.color_2 = pygame.Color(
            self.color.r if self.color.r-d < 0 else self.color.r-d,
            self.color.g if self.color.g-d < 0 else self.color.g-d,
            self.color.b if self.color.b-d < 0 else self.color.b-d,
            255
        )

        d = 100
        self.color_3 = pygame.Color(
            self.color.r if self.color.r-d < 0 else self.color.r-d,
            self.color.g if self.color.g-d < 0 else self.color.g-d,
            self.color.b if self.color.b-d < 0 else self.color.b-d,
            255
        )

        pa = pygame.PixelArray(self.image)
        pa.replace(pygame.Color("#ffffff"), self.color)
        pa.replace(pygame.Color("#a5a5a5"), self.color_2)
        pa.replace(pygame.Color("#3c3c3c"), self.color_3)
        del pa


        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, group):
        self.tick_counter += 1
        if self.tick_counter % self.animation_speed is 0:
            if self.index < len(self.frames)-1:
                self.index += 1
            else:
                del self.image
                group.remove(self)

        self.image = self.sprite_sheet.get_image(
            self.frames[self.index][0],
            self.frames[self.index][1],
            self.h,
            self.w
        )
        pa = pygame.PixelArray(self.image)
        pa.replace(pygame.Color("#ffffff"), self.color)
        pa.replace(pygame.Color("#a5a5a5"), self.color_2)
        pa.replace(pygame.Color("#3c3c3c"), self.color_3)
        del pa


class UnitSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_path, frames, x, y, h, w, animation_speed):
        super().__init__()

        self.frames = frames
        self.index = 0
        self.tick_counter = 0
        self.animation_speed = animation_speed

        self.h = h
        self.w = w

        self.sprite_sheet = SpriteSheet(sprite_sheet_path)

        self.image = self.sprite_sheet.get_image(
                                                self.frames[self.index][0],
                                                self.frames[self.index][1],
                                                self.h,
                                                self.w
                                                )

        self.image = pygame.transform.scale(self.image, (self.h*2, self.w*2))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.tick_counter += 1
        if self.tick_counter % self.animation_speed is 0:
            if self.index < len(self.frames)-1:
                self.index += 1
            else:
                self.index = 0
        self.image = self.sprite_sheet.get_image(
                                                self.frames[self.index][0],
                                                self.frames[self.index][1],
                                                self.h,
                                                self.w
                                                )

        self.image = pygame.transform.scale(self.image, (math.floor(self.h*1.5), math.floor(self.w*1.5)))

class KnightSprite(UnitSprite):
    def __init__(self, x, y):
            UnitSprite.__init__(
                    self,
                    "game/visualizer/assets/knight.png",
                    [
                        # 8 x 9
                        [0,    0], [128,    0], [256,    0], [384,    0], [512,    0], [640,    0], [768,    0], [896,    0],
                        [0,  128], [128,  128], [256,  128], [384,  128], [512,  128], [640,  128], [768,  128], [896,  128],
                        [0,  256], [128,  256], [256,  256], [384,  256], [512,  256], [640,  256], [768,  256], [896,  256],
                        [0,  384], [128,  384], [256,  384], [384,  384], [512,  384], [640,  384], [768,  384], [896,  384],
                        [0,  512], [128,  512], [256,  512], [384,  512], [512,  512], [640,  512], [768,  512], [896,  512],
                        [0,  640], [128,  640], [256,  640], [384,  640], [512,  640], [640,  640], [768,  640], [896,  640],
                        [0,  768], [128,  768], [256,  768], [384,  768], [512,  768], [640,  768], [768,  768], [896,  768],
                        [0,  896], [128,  896], [256,  896], [384,  896], [512,  896], [640,  896], [768,  896], [896,  896],
                        [0, 1024], [128, 1024], [256, 1024], [384, 1024], [512, 1024], [640, 1024], [768, 1024], [896, 1024],

                    ],
                    x, y,
                    128, 128,
                    2)

class BrawlerSprite(UnitSprite):
    def __init__(self, x, y):
            UnitSprite.__init__(
                    self,
                    "game/visualizer/assets/brawler.png",
                    [
                        [0,   0], [128,   0],
                        [0, 128], [128, 128],
                        [0, 256]
                    ],
                    x, y,
                    128, 128,
                    2)

class PikemanSprite(UnitSprite):
    def __init__(self, x, y):
            UnitSprite.__init__(
                    self,
                    "game/visualizer/assets/spearman.png",
                    [
                        [0,   0], [128,   0], [256,   0], [384,   0],
                        [0, 128], [128, 128], [256, 128], [384, 128],
                        [0, 256], [128, 256], [256, 256], [384, 256],
                        [0, 384], [128, 384], [256, 384], [384, 384]

                    ],
                    x, y,
                    128, 128,
                    2)

class RogueSprite(UnitSprite):
    def __init__(self, x, y):
            UnitSprite.__init__(
                    self,
                    "game/visualizer/assets/rogue.png",
                    [
                        [0,   0], [128,   0], [256,   0], [384,   0],
                        [0, 128], [128, 128], [256, 128], [384, 128],
                        [0, 256], [128, 256], [256, 256], [384, 256],
                        [0, 384], [128, 384], [256, 384], [384, 384],
                        [0, 512], [128, 512]

                    ],
                    x, y,
                    128, 128,
                    2)

class MagusSprite(UnitSprite):
    def __init__(self, x, y):
            UnitSprite.__init__(
                    self,
                    "game/visualizer/assets/magus.png",
                    [
                        [0,   0], [128,   0], [256,   0], [384,   0], [512,   0],
                        [0, 128], [128, 128], [256, 128], [384, 128], [512, 128],
                        [0, 256], [128, 256], [256, 256], [384, 256], [512, 256],
                        [0, 384], [128, 384], [256, 384], [384, 384], [512, 384],
                        [0, 512]

                    ],
                    x, y,
                    128, 128,
                    2)

class WizardSprite(UnitSprite):
    def __init__(self, x, y):
            UnitSprite.__init__(
                    self,
                    "game/visualizer/assets/wizard.png",
                    [
                        [0,   0], [128,   0], [256,   0],
                        [0, 128], [128, 128], [256, 128],
                        [0, 256], [128, 256]

                    ],
                    x, y,
                    128, 128,
                    2)

class SorcererSprite(UnitSprite):
    def __init__(self, x, y):
            UnitSprite.__init__(
                    self,
                    "game/visualizer/assets/sorcerer.png",
                    [
                        [0,   0], [128,   0], [256,   0], [384,   0],
                        [0, 128], [128, 128], [256, 128], [384, 128],
                        [0, 256], [128, 256], [256, 256], [384, 256],
                        [0, 384], [128, 384], [256, 384], [384, 384],
                        [0, 512], [128, 512]

                    ],
                    x, y,
                    128, 128,
                    3)

class AlchemistSprite(UnitSprite):
    def __init__(self, x, y):
            UnitSprite.__init__(
                    self,
                    "game/visualizer/assets/alchemist.png",
                    [
                        [0,   0], [128,   0], [256,   0], [384,   0],
                        [0, 128], [128, 128], [256, 128], [384, 128],
                        [0, 256], [128, 256], [256, 256], [384, 256],
                        [0, 384], [128, 384]

                    ],
                    x, y,
                    128, 128,
                    2)


def get_unit_sprite(unit_class, xy):
    if unit_class is UnitClass.knight:
        return KnightSprite(*xy)
    elif unit_class is UnitClass.brawler:
        return BrawlerSprite(*xy)
    elif unit_class is UnitClass.pikeman:
        return PikemanSprite(*xy)
    elif unit_class is UnitClass.rogue:
        return RogueSprite(*xy)
    elif unit_class is UnitClass.magus:
        return MagusSprite(*xy)
    elif unit_class is UnitClass.wizard:
        return WizardSprite(*xy)
    elif unit_class is UnitClass.sorcerer:
        return SorcererSprite(*xy)
    elif unit_class is UnitClass.alchemist:
        return AlchemistSprite(*xy)
    else:
        return None



class ArchwaySprite(pygame.sprite.Sprite):
    def __init__(self, x, y, text, show_arrow):
        super().__init__()

        self.tick_counter = 0

        self.text = text

        self.first = True

        self.h = 128
        self.w = 128

        self.x = x
        self.y = y

        self.show_arrow = show_arrow
        self.scale = 2

        self.cache = pygame.image.load("game/visualizer/assets/archway.png")
        rect = self.cache.get_rect()
        self.cache  = pygame.transform.scale(self.cache, (math.floor(rect.h*self.scale), math.floor(rect.w*self.scale)))

        self.arrow = pygame.image.load("game/visualizer/assets/arrow.png")
        arrow_rect = self.arrow.get_rect()
        self.arrow = pygame.transform.scale(self.arrow, (arrow_rect.w*3, arrow_rect.h*2))



    def update(self):
        if self.first or self.show_arrow:
            self.first = False

            self.tick_counter += 1

            if self.tick_counter > 10:
                self.tick_counter = 0

            self.image = self.cache.copy()

            text = ptext.draw(
                    self.text,
                    (0,0),
                    color=pygame.Color("#FFFFFF"),
                    owidth=1.0,
                    ocolor=(0, 0, 0),
                    alpha=1.0,
                    fontsize=14,
                    width=100,
                    fontname='game/visualizer/assets/joystix/joystix monospace.ttf')[0]

            # center text in arch
            text_rect = text.get_rect()
            image_rect = self.image.get_rect()

            text_pos = [
                math.floor(image_rect.w/2.0) - math.floor(text_rect.w/2.0),
                120
            ]

            # blit text onto image

            self.image.blit(text, text_pos)

            if self.show_arrow and self.tick_counter >= 5:
                arrow_rect = self.arrow.get_rect()
                self.image.blit(self.arrow, (
                    math.floor(image_rect.w/2.0) - math.floor(arrow_rect.w/2.0),
                    150))

            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y



class TrapSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_path, frames, x, y, h, w, animation_speed, scale=1):
        super().__init__()

        self.frames = frames
        self.index = 0
        self.tick_counter = 0
        self.animation_speed = animation_speed
        self.scale = scale

        self.h = h
        self.w = w

        self.sprite_sheet = SpriteSheet(sprite_sheet_path)

        self.image = self.sprite_sheet.get_image(
            self.frames[self.index][0],
            self.frames[self.index][1],
            self.h,
            self.w
        )

        self.image = pygame.transform.scale(self.image, (self.h*self.scale, self.w*self.scale))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        self.index = 0
        self.tick_counter = 0

    def update(self):
        self.tick_counter += 1
        if self.tick_counter % self.animation_speed is 0:
            if self.index < len(self.frames)-1:
                self.index += 1
            else:
                self.index = 0
        self.image = self.sprite_sheet.get_image(
            self.frames[self.index][0],
            self.frames[self.index][1],
            self.h,
            self.w
        )
        self.image = pygame.transform.scale(self.image, (self.h*self.scale, self.w*self.scale))

class SpikeTrap(TrapSprite):

    def __init__(self):
        TrapSprite.__init__(self, "game/visualizer/assets/spikes.png", [
            [ 0,    0 ]
        ], 0, 290, 1280, 128, 3)

class RiddleOfTheSphinxTrap(TrapSprite):

    def __init__(self):
        TrapSprite.__init__(self, "game/visualizer/assets/sphinx.png", [
            [ 0,    0 ]
        ], 448, 10, 128, 128, 3, scale=3)

class PuzzleBoxTrap(TrapSprite):

    def __init__(self):
        TrapSprite.__init__(self, "game/visualizer/assets/puzzle_box.png", [
            [ 0,    0 ]
        ], 512, 65, 128, 128, 3, scale=2)

class FallingCeilingTrap(TrapSprite):

    def __init__(self):
        TrapSprite.__init__(self, "game/visualizer/assets/falling_ceiling.png", [
            [0,    0], [1280,    0], [2560,    0], [3840,    0],
            [0,  720], [1280,  720], [2560,  720], [3840,  720],
            [0, 1440], [1280, 1440], [2560, 1440], [3840, 1440],
            [0, 2160], [1280, 2160], [2560, 2160], [3840, 2160],
            [0, 2880], [1280, 2880], [2560, 2880], [3840, 2880],
            [0, 3600], [1280, 3600], [2560, 3600]
        ], 0, 0, 1280, 720, 10, scale=1)

class EldritchBarrierTrap(TrapSprite):

    def __init__(self):
        TrapSprite.__init__(self, "game/visualizer/assets/eldritch_trap.png", [
            [ 0,    0 ]
        ], 512, 65, 128, 128, 10, scale=2)

class PendulumnBridgeTrap(TrapSprite):

    def __init__(self):
        TrapSprite.__init__(self, "game/visualizer/assets/pendulum.png", [
            [ 0,    0 ]
        ], 0, 0, 1280, 720, 3, scale=1)


loaded_trap_sprites = {}

def get_trap_sprite(trap_type):

    cls = None

    if trap_type == TrapType.spike_trap:
        cls = SpikeTrap
    elif trap_type == TrapType.riddles_of_the_sphinx:
        cls = RiddleOfTheSphinxTrap
    elif trap_type == TrapType.puzzle_box:
        cls = PuzzleBoxTrap
    elif trap_type == TrapType.falling_ceiling:
        cls = FallingCeilingTrap
    elif trap_type == TrapType.eldritch_barrier:
        cls = EldritchBarrierTrap
    elif trap_type == TrapType.pendulum_bridge:
        cls = PendulumnBridgeTrap
    else:
        cls = RiddleOfTheSphinxTrap

    if cls is not None and cls not in loaded_trap_sprites:
        loaded_trap_sprites[cls] = cls()

    loaded_trap_sprites[cls].reset()
    return loaded_trap_sprites[cls]


class SpecialAbilityAnimation(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_path, frames, x, y, h, w, animation_speed, scale=1, repeat=1):
        super().__init__()

        self.frames = frames
        self.index = 0
        self.tick_counter = 0
        self.animation_speed = animation_speed

        self.h = h
        self.w = w

        self.scale = scale

        self.repeat = repeat

        self.sprite_sheet = SpriteSheet(sprite_sheet_path)

        self.image = self.sprite_sheet.get_image(
            self.frames[self.index][0],
            self.frames[self.index][1],
            self.h,
            self.w
        )

        self.image = pygame.transform.scale(self.image, (self.h*self.scale, self.w*self.scale))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, obj):

        self.tick_counter += 1
        if self.tick_counter % self.animation_speed is 0:
            if self.index < len(self.frames)-1:
                self.index += 1
            else:
                self.index = 0
                self.repeat -= 1

        if self.repeat <= 0:
            obj.remove(self)

        self.image = self.sprite_sheet.get_image(
            self.frames[self.index][0],
            self.frames[self.index][1],
            self.h,
            self.w
        )

        self.image = pygame.transform.scale(self.image, (self.h*self.scale, self.w*self.scale))

class ResupplyAnimation(SpecialAbilityAnimation):
    def __init__(self, x, y):
        super().__init__(
            "game/visualizer/assets/resupply_animation.png",
            [
                [0,   0], [32,   0], [64,   0],
                [0,  32], [32,  32], [64,  32],
                [0,  64], [32,  64], [64,  64],

            ],
            x, y,
            32, 32,
            2, scale=2)

class IllusionAnimation(SpecialAbilityAnimation):
    def __init__(self, x, y):
        super().__init__(
            "game/visualizer/assets/illusion_animation.png",
            [
                [0,   0], [32,   0], [64,   0],
                [0,  32], [32,  32], [64,  32],
                [0,  64], [32,  64], [64,  64],

            ],
            x, y,
            32, 32,
            2, scale=8)


class Illusion2Animation(SpecialAbilityAnimation):
    def __init__(self, x, y):
        super().__init__(
            "game/visualizer/assets/illusion_2_animation.png",
            [
                [0,   0], [64,   0], [128,   0], [192,   0],
                [0,  64], [64,  64], [128,  64], [192,  64],
                [0,  96], [64,  96], [128,  96], [192,  96],
                [0, 128], [64, 128], [128, 128], [192, 128]

            ],
            x, y,
            64, 64,
            1, scale=4)

class InvigorateAnimation(SpecialAbilityAnimation):
    def __init__(self, x, y):
        super().__init__(
            "game/visualizer/assets/invigorate_animation.png",
            [
                [0,   0], [32,   0], [64,   0],
                [0,  32], [32,  32], [64,  32],
                [0,  64], [32,  64], [64,  64],

            ],
            x, y,
            32, 32,
            2, scale=8)


class ElementalBurstAnimation(SpecialAbilityAnimation):
    def __init__(self, x, y):
        super().__init__(
            "game/visualizer/assets/elemental_burst_animation.png",
            [
                [0,   0], [32,   0], [64,   0], [96, 0],
                [0,  32], [32,  32], [64,  32], [96, 32],
                [0,  64], [32,  64], [64,  64], [96, 64],
                [0,  96], [32,  96], [64,  96], [96, 96]
            ],
            x, y,
            32, 32,
            2, scale=10)

class TargetWeaknessAnimation(SpecialAbilityAnimation):
    def __init__(self, x, y):
        super().__init__(
            "game/visualizer/assets/target_weakness_animation.png",
            [
                [0,   0], [32,   0], [64,   0], [96,    0], [128,   0], [160,   0],
                [0,  32], [32,  32], [64,  32], [96,   32], [128,  32], [160,  32],
                [0,  64], [32,  64], [64,  64], [96,   64], [128,  64], [160,  64],
                [0,  96], [32,  96], [64,  96], [96,   96], [128,  96], [160,  96],
                [0, 128], [32, 128], [64, 128], [96,  128], [128, 128], [160, 128],
                [0, 160], [32, 160], [64, 160], [96,  160], [128, 160], [160, 160],
            ],
            x, y,
            32, 32,
            1, scale=6)

class FitOfRageAnimation(SpecialAbilityAnimation):
    def __init__(self, x, y):
        super().__init__(
            "game/visualizer/assets/fit_of_rage_animation.png",
            [
                # 3x4 sprite sheet
                [0,   0], [64,   0], [128,   0],
                [0,  64], [64,  64], [128,  64],
                [0, 128], [64, 128], [128, 128],
                [0, 192], [64, 192], [128, 192]
            ],
            x, y,
            64, 64,
            2, scale=1)

class TauntAnimation(SpecialAbilityAnimation):
    def __init__(self, x, y):
        super().__init__(
            "game/visualizer/assets/taunt_animation.png",
            [
                [0,   0],
                [0,  64],
            ],
            x, y,
            64, 64,
            4, scale=1, repeat=3)
