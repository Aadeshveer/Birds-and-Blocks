from .utils import load_image, load_images, load_sound, Animation
import pygame

def assets_loader(game):

    game.assets = {

        'background' : load_images('background',scaling=game.SIZE),
        
        'launcher' : load_images('projectile_shooter'),
        'launcher_flipped' : load_images('projectile_shooter', flip = True),
        
        'projectile' : {
        
            'basic' : {
                'idle' : Animation(load_images('projectiles/basic/idle')),
                'in_air' : Animation(load_images('projectiles/basic/in_air')),
                'feather' : Animation(load_images('projectiles/basic/feather'), img_dur=10, loop=False),
                'upgrade' : load_image('projectiles/basic/upgrade/upgrade.png'),
            },
        
            'wood' : {
                'idle' : Animation(load_images('projectiles/wood/idle')),
                'in_air' : Animation(load_images('projectiles/wood/in_air')),
                'feather' : Animation(load_images('projectiles/wood/feather'), img_dur=10, loop=False),
                'upgrade' : load_image('projectiles/wood/upgrade/upgrade.png'),
            },
        
            'stone' : {
                'idle' : Animation(load_images('projectiles/stone/idle')),
                'in_air' : Animation(load_images('projectiles/stone/in_air')),
                'feather' : Animation(load_images('projectiles/stone/feather'), img_dur=10, loop=False),
                'upgrade' : load_image('projectiles/stone/upgrade/upgrade.png'),
            },
        
            'glass' : {
                'idle' : Animation(load_images('projectiles/glass/idle')),
                'in_air' : Animation(load_images('projectiles/glass/in_air')),
                'feather' : Animation(load_images('projectiles/glass/feather'), img_dur=10, loop=False),
                'upgrade' : load_image('projectiles/glass/upgrade/upgrade.png'),
            },
        },
        
        'projectile_flipped' : {
        
            'basic' : {
                'idle' : Animation(load_images('projectiles/basic/idle', flip = True)),
                'in_air' : Animation(load_images('projectiles/basic/in_air', flip = True)),
                'feather' : Animation(load_images('projectiles/basic/feather', flip = True), img_dur=10, loop=False),
                'upgrade' : load_image('projectiles/basic/upgrade/upgrade.png', flip=True),
            },
        
            'wood' : {
                'idle' : Animation(load_images('projectiles/wood/idle', flip = True)),
                'in_air' : Animation(load_images('projectiles/wood/in_air', flip = True)),
                'feather' : Animation(load_images('projectiles/wood/feather', flip = True), img_dur=10, loop=False),
                'upgrade' : load_image('projectiles/wood/upgrade/upgrade.png', flip=True),
            },
        
            'stone' : {
                'idle' : Animation(load_images('projectiles/stone/idle', flip = True)),
                'in_air' : Animation(load_images('projectiles/stone/in_air', flip = True)),
                'feather' : Animation(load_images('projectiles/stone/feather', flip = True), img_dur=10, loop=False),
                'upgrade' : load_image('projectiles/stone/upgrade/upgrade.png', flip=True),
            },
        
            'glass' : {
                'idle' : Animation(load_images('projectiles/glass/idle', flip = True)),
                'in_air' : Animation(load_images('projectiles/glass/in_air', flip = True)),
                'feather' : Animation(load_images('projectiles/glass/feather', flip = True), img_dur=10, loop=False),
                'upgrade' : load_image('projectiles/glass/upgrade/upgrade.png', flip=True),
            },
        },
        
        'cards' : {
        
            'basic' : load_image('cards/bird/red/red.png'),
            'wood' : load_image('cards/bird/wood/wood.png'),
            'stone' : load_image('cards/bird/stone/stone.png'),
            'glass' : load_image('cards/bird/glass/glass.png'),
        
            'upgrade_basic' : load_image('cards/upgrade/red/red.png'),
            'upgrade_wood' : load_image('cards/upgrade/wood/wood.png'),
            'upgrade_stone' : load_image('cards/upgrade/stone/stone.png'),
            'upgrade_glass' : load_image('cards/upgrade/glass/glass.png'),
        },
        
        'blocks' : {
            'glass' : Animation(load_images('blocks/glass'), img_dur = 1),
            'wood' : Animation(load_images('blocks/wood'), img_dur = 1),
            'stone' : Animation(load_images('blocks/stone'), img_dur = 1),
        },
        
        'effects' : {
            'dust' : Animation(load_images('effects/dust'), img_dur = 1, loop=False),
            'particle' : Animation(load_images('effects/particles'), img_dur=3, loop=False)
        },
        
        'shards' : {
            'glass' : Animation(load_images('effects/shards/glass'), img_dur=10),
            'wood' : Animation(load_images('effects/shards/wood'), img_dur=10),
            'stone' : Animation(load_images('effects/shards/stone'), img_dur=10),
        },
        
        'clouds' : Animation(load_images('clouds', scaling=(160,64)), img_dur=10),
        
        'UI' : {
        
            'title' : load_image('UI/menu/title.png', scaling=game.SIZE),
        
            'play_button' : Animation(load_images('UI/menu/play_button', scaling=game.SIZE), img_dur=10),
            'tutorial_button' : Animation(load_images('UI/menu/tutorial_button', scaling=game.SIZE), img_dur=10),
            'credits_button' : Animation(load_images('UI/menu/credits_button', scaling=game.SIZE), img_dur=10),
        
            'game_over' : load_image('UI/game_over/game_over.png', scaling=game.SIZE),
            'player_box' : load_image('UI/game_over/player_box.png', scaling=game.SIZE),
            'menu_button' : Animation(load_images('UI/game_over/menu_button', scaling=game.SIZE), img_dur=10),
        
            'player_name' : {
                'left' : Animation(load_images('UI/player_name/1', scaling=game.SIZE), img_dur=10),
                'right' : Animation(load_images('UI/player_name/2', scaling=game.SIZE), img_dur=10),
            },
        
            'util_buttons' : {
                'back_button' : Animation(load_images('UI/buttons/back_button', scaling=game.SIZE), img_dur=10),
                'mute_button' : Animation(load_images('UI/buttons/voice', scaling=game.SIZE), img_dur=10),
                'leaderboard' : Animation(load_images('UI/buttons/leaderboard', scaling=game.SIZE), img_dur=10),
            },
        
            'tutorial' : Animation(load_images('UI/tutorial', scaling=game.SIZE, alpha=True), img_dur=10),
            'credits' : Animation(load_images('UI/credits', scaling=game.SIZE, alpha=True), img_dur=10),
            'leaderboard' : Animation(load_images('UI/leaderboard', scaling=game.SIZE, alpha=True), img_dur=10),
            'turn_display' : Animation(load_images('UI/turn_display', scaling=game.SIZE), img_dur=10),
            'pygame' : load_image('UI/msc/pygame_logo-removebg.png', scaling=(200,80)),
            'icon' : load_image('UI/icon/icon.png'),
        },
    }

    game.audio = {
    
        'glass_break' : load_sound('glass_break'),
        'stone_break' : load_sound('stone_break'),
        'wood_break' : load_sound('wood_break'),
    
        'glass_yell' : load_sound('glass_yell'),
        'basic_yell' : load_sound('basic_yell'),
        'wood_yell' : load_sound('wood_yell'),
        'stone_yell' : load_sound('stone_yell'),
    
        'button' : load_sound('button'),
    
        'upgrade' : load_sound('upgrade'),
    
        'bomb' : load_sound('bomb'),
    
        'hit' : load_sound('hit'),
    }

    game.fonts = {
        'monospace' : pygame.font.Font('assets/fonts/custom_font.ttf'),
    }
