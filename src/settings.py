WINDOW_WIDTH, WINDOW_HEIGHT = 800, 800
PLAYER_ANIMATIONSW, PLAYER_ANIMATIONSH = 64, 64

PATHS = {
    "enemy": "graphics/player",
    "player": "graphics/player/spritesPlayer.png",
    "arrow": "graphics/weapon/arrow2.png",
    "font": "graphics/other/subatomic.ttf",
    "menufont": "graphics/other/font.ttf",
    "background": "graphics/other/tumba.png",
    "background_bosque": "graphics/other/bosque.png",
    "bullet": "graphics/weapon/bullet.png",
    "fireball": "graphics/weapon/fireball.png",
    "tumba": "data/tumba.tmx",
    "tienda": "data/tienda.tmx",
    "bosque": "data/bosque.tmx",
    "pueblo": "data/pueblo.tmx",
    "esqueleto": "graphics/esqueleto/",
    "humano1": "graphics/humano1/",
    "humano2": "graphics/humano2/",
    "momia": "graphics/momia/",
    "zombie1": "graphics/zombie1/",
    "zombie2": "graphics/zombie2/",
    "bossH": "graphics/boss/herido/hacha.png",
    "bossN": "graphics/boss/normal/hacha.png",
    "sword": "graphics/weapon/sword.png",
    "bow": "graphics/weapon/bow.png",
    "staff": "graphics/weapon/staff.png",
    "mace": "graphics/weapon/maza.png",
    "latigo": "graphics/weapon/latigo.png",
    "crossbow": "graphics/weapon/crossbow.png",
    "hacha": "graphics/weapon/hacha.png",
    "spear": "graphics/weapon/spear.png",
    "spearP": "graphics/Personaje/spear.png",
    "swordP": "graphics/Personaje/sword.png",
    "bowP": "graphics/Personaje/bow.png",
    "staffP": "graphics/Personaje/staff.png",
    "maceP": "graphics/Personaje/mace.png",
    "latigoP": "graphics/Personaje/latigo.png",
    "crossbowP": "graphics/Personaje/crossbow.png",
    "hachaP": "graphics/Personaje/axe.png",
    "playbutton": "graphics/other/PlayButton.png",
    "quitbutton": "graphics/other/QuitButton.png",
    "menuBG": "graphics/other/MenuBackground.png",
    "carta": "graphics/other/carta.png",
    "heart": "graphics/other/heart.png",
    "coin": "graphics/other/coin.png",
    "victoria": "graphics/other/victoria.png",
    "tutorialtienda": "graphics/other/tiendaTutorial.png",
    "tutorial": "graphics/other/tutorial.png",
    "level_arrow": "graphics/other/level_arrow.png"
}

MAP_LAYERS = {
    'bosque': [('Hierba', False), ('Coli_3', True), ('Coli_1', True), ('Puertas', False), ('Acc_agua', True)],
    'pueblo': [('Segunda base', False), ('Coli', True)],
    'tumba': [('intermedio', False), ('bloqueo', False), ('objetos', True), ('runas', False)],
    'tienda': [('Fondo', False), ('Base', False), ('Colisionables', True)]
}

SWORD_ANIMATIONS = {
    "10": "down.9",
    "28": "down_attack.6.3",
    "10.2": "down_idle.1",
    "9": "left.9",
    "25": "left_attack.6.3",
    "9.2": "left_idle.1",
    "8": "up.9",
    "22": "up_attack.6.3",
    "8.2": "up_idle.1",
    "11": "right.9",
    "31": "right_attack.6.3",
    "11.2": "right_idle.1",
    "20": "death.6",
}

AXE_ANIMATIONS = SWORD_ANIMATIONS

CROSSBOW_ANIMATIONS = {
    "10": "down.9",
    "6": "down_attack.8",
    "10.2": "down_idle.1",
    "9": "left.9",
    "5": "left_attack.8",
    "9.2": "left_idle.1",
    "8": "up.9",
    "4": "up_attack.8",
    "8.2": "up_idle.1",
    "11": "right.9",
    "7": "right_attack.8",
    "11.2": "right_idle.1",
    "20": "death.6",
}

BOW_ANIMATIONS = {
    "25.5": "down.7.2",
    "18": "down_attack.13",
    "10.2": "down_idle.1",
    "23.5": "left.7.2",
    "17": "left_attack.13",
    "9.2": "left_idle.1",
    "21.5": "up.7.2",
    "16": "up_attack.13",
    "8.2": "up_idle.1",
    "27.5": "right.7.2",
    "19": "right_attack.13",
    "11.2": "right_idle.1",
    "20": "death.6",
}

MAGIC_ANIMATIONS = {
    "10": "down.9",
    "28": "down_attack.8.3",
    "10.2": "down_idle.1",
    "9": "left.9",
    "25": "left_attack.8.3",
    "9.2": "left_idle.1",
    "8": "up.9",
    "22": "up_attack.8.3",
    "8.2": "up_idle.1",
    "11": "right.9",
    "31": "right_attack.8.3",
    "11.2": "right_idle.1",
    "20": "death.6",
}

MACE_ANIMATIONS = SWORD_ANIMATIONS

SPEAR_ANIMATIONS = {
    "10": "down.9",
    "6": "down_attack.8",
    "10.2": "down_idle.1",
    "9": "left.9",
    "5": "left_attack.8",
    "9.2": "left_idle.1",
    "8": "up.9",
    "4": "up_attack.8",
    "8.2": "up_idle.1",
    "11": "right.9",
    "7": "right_attack.8",
    "11.2": "right_idle.1",
    "20": "death.6",
}

LATIGO_ANIMATIONS = {
    "10": "down.9",
    "28": "down_attack.8.3:0:64",
    "10.2": "down_idle.1",
    "9": "left.9",
    "25": "left_attack.8.3:-64:0",
    "9.2": "left_idle.1",
    "8": "up.9",
    "22": "up_attack.8.3:64:0",
    "8.2": "up_idle.1",
    "11": "right.9",
    "31": "right_attack.8.3:64:0",
    "11.2": "right_idle.1",
    "20": "death.6",
}

ANIMATIONS = {
    "sword": SWORD_ANIMATIONS,
    "bow": BOW_ANIMATIONS,
    "staff": MAGIC_ANIMATIONS,
    "mace": MACE_ANIMATIONS,
    "latigo": LATIGO_ANIMATIONS,
    "crossbow": CROSSBOW_ANIMATIONS,
    "hacha": AXE_ANIMATIONS,
    "spear": SPEAR_ANIMATIONS
}
