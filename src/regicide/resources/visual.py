'''
Created on Mar 2, 2013

@author: Devindra

This module loads and stores all graphical assets for the game.
'''
from pyglet import image

class ImageSet(object):
    def __init__(self, name, rows, columns):
        self.palette = image.ImageGrid(image.load('resources/visual/'+name+'.png'), rows=rows, columns=columns)
    
    def get(self, index):
        return self.palette[index]
    
class Character(object):
    ELLIOT = image.load('resources/visual/characters/elliot.png')
    HELENA = image.load('resources/visual/characters/helena.png')
    LANCEL = image.load('resources/visual/characters/lancel.png')
    SHALOTT = image.load('resources/visual/characters/shalott.png')
    VIVIEN = image.load('resources/visual/characters/vivien.png')
    YORICK = image.load('resources/visual/characters/yorick.png')

class Icon(ImageSet):
    LVL, NUMBER_1, NUMBER_2, NUMBER_3, NUMBER_4, NUMBER_5, NUMBER_6, NUMBER_7, NUMBER_8, NUMBER_9, NUMBER_10, QUESTION, EXCLAMATION = range(13)
    GO, CLOCK_LARGE, FLAG, DIRECTIONS, ARROW_RIGHT, ARROW_DOWN_RIGHT, ARROW_UP_RIGHT, ARROW_UP, ARROW_RIGHT_UP, ARROW_LEFT_UP, ARROW_LEFT, ARROW_UP_LEFT, ARROW_DOWN_LEFT, ARROW_DOWN, ARROW_RIGHT_DOWN, ARROW_LEFT_DOWN = range(16, 32)
    POINTER, CANCEL, CLOCK, BOX, HEART, FIST, SWORD, ARMOUR, SHIELD, STAR, HOURGLASS, COIN, SKULL, KEY, PAGE, BOOK = range(32, 48)
    
    instance = ImageSet('icons', 3, 16)
    
    @staticmethod
    def get(index):
        return Icon.instance.get(index)

class Entity(ImageSet):
    GOBLIN, ZOMBIE, SKELETON, ORC, OGRE, WEREWOLF, GOLEM, DEMON = range(8)
    SLIME_SWARM, SLIME_LARGE, SCORPION, OCTOPUS, VAMPIRE, MUMMY, WRAITH, BEHOLDER = range(8, 16)
    MUSHROOMS, RABBIT, BAT_SMALL, BAT_LARGE, SNAKE, WOLF, BOAR, BEAR = range(16, 24)
    RAT, SPIDER_SWARM, LIZARD, SPIDER_LARGE, FROG, BEETLE, CENTIPEDE, DRAGON = range(24, 32)
    ELF_MALE, DWARF, BARBARIAN, ELF_FEMALE, RANGER, KNIGHT, WIZARD, SORCEROR = range(32, 40)
    
    instance = ImageSet('units', 5, 8)
    
    @staticmethod
    def get(index):
        return Entity.instance.get(index)

class Tile(ImageSet):
    COLUMNS, COLUMNS_GATE, GRATE, SPIKES, TILES, WAVES, BUBBLES, STARS = range(8)
    PLINTH_EYE, PLINTH, BRICK_LARGE, BRICK, BRICK_HOLE, GATE_1, GATE_2, GATE_3 = range(8, 16)
    BLOCK_LIGHT, PLINTH_LIGHT, BLOCK, BLOCK_CRACKED, BLOCK_LOCKED, STAIRS_DOWN, STAIRS_UP, PIT = range(16, 24)
    SHADE_1, SHADE_2, SHADE_3, SHADE_4, SHADE_5, SHADE_6, SHADE_7, SHADE_8 = range(24, 32)
    
    instance = ImageSet('tiles', 4, 8)
    
    @staticmethod
    def get(index):
        return Tile.instance.get(index)

class Misc(ImageSet):
    SYMBOL_PENTAGRAM, SYMBOL_ANKH, SYMBOL_EYE, SYMBOL_TRI, SYMBOL_DIRECTIONS, SYMBOL_PERSON, BANNER, SIGN = range(8)
    SKULLS_MANY, SKULL, BONES, GRAVE, ALTAR, FOUNTAIN, GEMS, SPHERE = range(8, 16)
    COINS_FEW, COINS_MANY, BUBBLES, JEWEL, RING_SMALL, RING_LARGE, AMULET_SMALL, AMULET_LARGE = range(16, 24)
    SCEPTER_1, SCEPTER_2, SCEPTER_3, SCEPTER_4, SCEPTER_5, SCEPTER_6, SCEPTER_7, SCEPTER_8 = range(24, 32)
    SHIELD_1, SHIELD_2, SHIELD_3, SHIELD_4, SHIELD_5, SHIELD_6, SHIELD_7, SHIELD_8 = range(32, 40)
    HELMET_1, HELMET_2, HELMET_3, HELMET_4, HELMET_5, HELMET_6, HELMET_7, HELMET_8 = range(40, 48)
    TUNIC_1, TUNIC_2, TUNIC_3, TUNIC_4, TUNIC_5, TUNIC_6, TUNIC_7, TUNIC_8 = range(48, 56)
    BOMBS_1, BOMBS_2, BOMBS_3, ARROWS_1, ARROWS_2, ARROWS_3, BOLTS_1, BOLTS_2 = range(56, 64)
    SHURIKEN_1, SHURIKEN_2, THROWING_DAGGERS, BOW_1, BOW_2, BOW_3, CROSSBOW_1, CROSSBOW_2 = range(64, 72)
    AXE_1, AXE_2, AXE_3, AXE_4, AXE_5, AXE_6, AXE_7, AXE_8 = range(72, 80)
    SWORD_1, SWORD_2, SWORD_3, SWORD_4, SWORD_5, SWORD_6, SWORD_7, SWORD_8 = range(80, 88)
    SCROLL_1, SCROLL_2, SCROLL_3, SCROLL_4, SCROLL_5, SCROLL_6, SCROLL_7, SCROLL_8 = range(88, 96)
    POTION_1, POTION_2, POTION_3, POTION_4, POTION_5, POTION_6, POTION_7, POTION_8 = range(96, 104)
    CHEST, CHEST_OPEN, KEY_1, KEY_2, KEY_3, KEY_4, KEY_5, KEY_6 = range(104, 112)
    
    instance = ImageSet('misc', 14, 8)
    
    @staticmethod
    def get(index):
        return Misc.instance.get(index)

class UI(ImageSet):
    BAR_LEFT, BAR_100, BAR_75, BAR_50, BAR_25, BAR_0, BAR_RIGHT = range(7)
    HEART_100, HEART_75, HEART_50, HEART_25, HEART_0, HEART_EMPTY = range(7, 13)
    
    instance = ImageSet('ui', 2, 7)
    
    @staticmethod
    def get(index):
        return UI.instance.get(index)

class Cursor(ImageSet):
    SELECT, TARGET, GREEN, YELLOW = range(4)
    
    instance = ImageSet('cursor', 1, 4)
    
    @staticmethod
    def get(index):
        return Cursor.instance.get(index)

class ASCII(ImageSet):
    instance = ImageSet('ascii', 16, 16)
    
    @staticmethod
    def get(index):
        return ASCII.instance.get(index)
    
    @staticmethod
    def get_index(x, y):
        return x + y*16


class Pattern(ImageSet):
    instance = ImageSet('patterns', 1, 8)
    
    @staticmethod
    def get(index):
        return Pattern.instance.get(index)


class Number(object):
    palette_large = image.ImageGrid(image.load('resources/visual/numbers-large.png'), rows=2, columns=10)
    palette_small = image.ImageGrid(image.load('resources/visual/numbers-small.png'), rows=2, columns=10)
    
    @staticmethod
    def get(value, large=False, highlight=False):
        value = value % 10
        
        if (highlight):
            value += 10
        
        if (large):
            return Number.palette_large[value]
        else:
            return Number.palette_small[value]
    
    
