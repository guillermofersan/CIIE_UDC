import random

from monster import *
from observer import Observer, Subject
from resources import *


class Zone(Observer):
    def __init__(self, director, left, right):
        self.director = director
        self.left_border = left
        self.right_border = right
        self.enemy_counter = 0

    def is_in_zone(self, obj):
        return self.left_border < obj.x < self.right_border

    def setup_weapons(self):
        for obj in self.director.get_map_layer("weapon"):
            # if self.is_in_zone(obj):
            Weapon((obj.x, obj.y), ResourceManager.load(obj.name), [self.director.weapons, self.director.all_sprites],
                   obj.name, 1)

    def setup_enemy(self):
        for obj in self.director.get_map_layer("enemy"):
            args = {
                "pos": (obj.x, obj.y),
                "name": obj.name,
                "groups": self.director.get_enemy_groups(),
                "collision_sprites": self.director.get_colliders(),
                "player": self.director.get_player(),
            }
            if self.is_in_zone(obj):
                match random.randint(0, 3):
                    case 0:
                        monster = MonsterCrossBow(bullet_groups=self.director.get_bullet_groups(), **args)
                    case 1:
                        monster = MonsterSword(**args)
                    case 2:
                        monster = MonsterBow(bullet_groups=self.director.get_bullet_groups(), **args)
                    case 3:
                        monster = MonsterStaff(bullet_groups=self.director.get_bullet_groups(), **args)
                w = monster.image.get_size()[0]
                h = monster.image.get_size()[1]
                healthBar = HealthBar(obj.x - int(w / 2), obj.y + int(h / 2), w, 5, monster.health,
                                      self.director.get_health_bar())
                monster.attach(healthBar)
                monster.attach(self)
                monster.healthBar = healthBar
                self.enemy_counter += 1

    def spawnHeart(self, pos):
        Heart(pos, ResourceManager.load("heart"), [self.director.all_sprites, self.director.hearts])

    def spawnCoin(self, pos):
        Heart(pos, ResourceManager.load("coin"), [self.director.all_sprites, self.director.coins])

    def update(self, subject: Subject):
        if (subject.health <= 0):
            self.enemy_counter -= 1
            if random.randint(1, 10) <= 5:
                self.spawnHeart(subject.pos + (20, 0))
            else:
                self.spawnCoin(subject.pos)


class Zone1(Zone):
    def __init__(self, director):
        super().__init__(director, 0, WINDOW_WIDTH)

    def setup(self):
        self.setup_enemy()
        self.setup_weapons()

    def next_zone(self):
        return Zone2(self.director)


class Zone2(Zone):
    def __init__(self, director):
        super().__init__(director, WINDOW_WIDTH, WINDOW_WIDTH * 2)

    def setup(self):
        self.setup_enemy()
        self.setup_weapons()

    def next_zone(self):
        return Zone3(self.director)


class Zone3(Zone):
    def __init__(self, director):
        super().__init__(director, WINDOW_WIDTH * 2, WINDOW_WIDTH * 3)

    def setup(self):
        self.setup_enemy()
        self.setup_weapons()
        self.load_boss()

    def next_zone(self):
        return None

    def load_boss(self):
        for obj in self.director.get_map_layer("boss"):
            monster = MonsterBoss(
                pos=(obj.x, obj.y),
                groups=[self.director.all_sprites, self.director.enemy],
                path=PATHS["bossN"],
                collision_sprites=self.director.colliders,
                health=20,
                player=self.director.player,
                shot_speed=500,
                animations=AXE_ANIMATIONS
            )
            w = monster.image.get_size()[0]
            h = monster.image.get_size()[1]
            healthBar = HealthBar(obj.x - int(w / 2), obj.y + int(h / 2), w, 5, monster.health,
                                  self.director.get_health_bar())
            monster.attach(healthBar)
            monster.attach(self)
            monster.healthBar = healthBar
            self.enemy_counter += 1
