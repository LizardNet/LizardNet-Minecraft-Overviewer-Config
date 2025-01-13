ENTITY_NAMES = {
    'allay': 'Allay',
    'armadillo': 'Armadillo',
    'axolotl': 'Axolotl',
    'bat': 'Bat',
    'bee': 'Bee',
    'blaze': 'Blaze',
    'bogged': 'Bogged',
    'breeze': 'Breeze',
    'camel': 'Camel',
    # 'camel_husk': 'Camel Husk',
    'cat': 'Cat',
    'cave_spider': 'Cave Spider',
    'chicken': 'Chicken',
    'cod': 'Cod',
    'copper_golem': 'Copper Golem',
    'cow': 'Cow',
    'creaking': 'Creaking',
    'creeper': 'Creeper',
    'dolphin': 'Dolphin',
    'donkey': 'Donkey',
    'drowned': 'Drowned',
    'elder_guardian': 'Elder Guardian',
    'ender_dragon': 'Ender Dragon',
    'enderman': 'Enderman',
    'endermite': 'Endermite',
    'evoker': 'Evoker',
    'fox': 'Fox',
    'frog': 'Frog',
    'ghast': 'Ghast',
    'glow_squid': 'Glow Squid',
    'goat': 'Goat',
    'guardian': 'Guardian',
    'happy_ghast': 'Happy Ghast',
    'hoglin': 'Hoglin',
    'horse': 'Horse',
    'husk': 'Husk',
    'illusioner': 'Illusioner',
    'iron_golem': 'Iron Golem',
    'llama': 'Llama',
    'magma_cube': 'Magma Cube',
    'mooshroom': 'Mooshroom',
    'mule': 'Mule',
    # 'nautilus': 'Nautilus',
    'ocelot': 'Ocelot',
    'panda': 'Panda',
    # 'parched': 'Parched',
    'parrot': 'Parrot',
    'phantom': 'Phantom',
    'pig': 'Pig',
    'piglin_brute': 'Piglin Brute',
    'piglin': 'Piglin',
    'pillager': 'Pillager',
    'polar_bear': 'Polar Bear',
    'pufferfish': 'Pufferfish',
    'rabbit': 'Rabbit',
    'ravager': 'Ravager',
    'salmon': 'Salmon',
    'sheep': 'Sheep',
    'shulker': 'Shulker',
    'silverfish': 'Silverfish',
    'skeleton_horse': 'Skeleton Horse',
    'skeleton': 'Skeleton',
    'slime': 'Slime',
    'sniffer': 'Sniffer',
    'snow_golem': 'Snow Golem',
    'spider': 'Spider',
    'squid': 'Squid',
    'stray': 'Stray',
    'strider': 'Strider',
    'tadpole': 'Tadpole',
    'trader_llama': 'Trader Llama',
    'tropical_fish': 'Tropical Fish',
    'turtle': 'Turtle',
    'vex': 'Vex',
    'villager': 'Villager',
    'vindicator': 'Vindicator',
    'wandering_trader': 'Wandering Trader',
    'warden': 'Warden',
    'witch': 'Witch',
    'wither_skeleton': 'Wither Skeleton',
    'wither': 'Wither',
    'wolf': 'Wolf',
    'zoglin': 'Zoglin',
    # 'zombie_horse': 'Zombie Horse',
    # 'zombie_nautilus': 'Zombie Nautilus',
    'zombie_villager': 'Zombie Villager',
    'zombie': 'Zombie',
    'zombified_piglin': 'Zombified Piglin',
}

MOB_VARIANTS = {
    'axolotl': {
        'tag': 'Variant',
        'default': 'lucy',
        'values': {
            0: 'lucy',
            1: 'wild',
            2: 'gold',
            3: 'cyan',
            4: 'blue'
        }
    },
    'cat': {
        'tag': 'variant',
        'default': 'jellie',
        'values': {
            'minecraft:white': 'white',
            'minecraft:black': 'black',
            'minecraft:red': 'red',
            'minecraft:siamese': 'siamese',
            'minecraft:british_shorthair': 'british_shorthair',
            'minecraft:calico': 'calico',
            'minecraft:persian': 'persian',
            'minecraft:ragdoll': 'ragdoll',
            'minecraft:tabby': 'tabby',
            'minecraft:all_black': 'all_black',
            'minecraft:jellie': 'jellie',
        }
    },
    'chicken': {
        'tag': 'variant',
        'default': 'temperate',
        'values': {
            'minecraft:warm': 'warm',
            'minecraft:temperate': 'temperate',
            'minecraft:cold': 'cold'
        }
    },
    'copper_golem': {
        'tag': 'weather_state',
        'default': 'unaffected',
        'values': ['unaffected', 'exposed', 'weathered', 'oxidized']
    },
    'cow': {
        'tag': 'variant',
        'default': 'temperate',
        'values': {
            'minecraft:warm': 'warm',
            'minecraft:temperate': 'temperate',
            'minecraft:cold': 'cold'
        }
    },
    'fox': {
        'tag': 'Type',
        'default': 'red',
        'values': ['red', 'snow']
    },
    'frog': {
        'tag': 'variant',
        'default': 'temperate',
        'values': {
            'minecraft:warm': 'warm',
            'minecraft:temperate': 'temperate',
            'minecraft:cold': 'cold'
        }
    },
    'horse': {
        'tag': 'Variant',
        'default': '',
        'values': [] # Horses have complex variants based on color and markings. We'll ignore it for now.
    },
    'llama': {
        'tag': 'Variant',
        'default': 'creamy',
        'values': {
            0: 'creamy',
            1: 'white',
            2: 'brown',
            3: 'gray'
        }
    },
    'mooshroom': {
        'tag': 'Type',
        'default': 'red',
        'values': ['red', 'brown']
    },
    'panda': {
        'tag': 'MainGene',
        'default': '',
        'values': [] # Pandas have complex variants based on personality traits. Ignored for now.
    },
    'parrot': {
        'tag': 'Variant',
        'default': 'red_blue',
        'values': {
            0: 'red_blue',
            1: 'blue',
            2: 'green',
            3: 'yellow_blue',
            4: 'gray'
        }
    },
    'pig': {
        'tag': 'variant',
        'default': 'temperate',
        'values': {
            'minecraft:warm': 'warm',
            'minecraft:temperate': 'temperate',
            'minecraft:cold': 'cold'
        }
    },
    'rabbit': {
        'tag': 'RabbitType',
        'default': 'brown',
        'values': {
            0: 'brown',
            1: 'white',
            2: 'black',
            3: 'white_splotched',
            4: 'gold',
            5: 'salt_pepper',
            99: 'killer'
            # Toast
        }
    },
    'sheep': {
        'tag': 'Color',
        'default': 'white',
        'values': {
            0: 'white',
            1: 'orange',
            2: 'magenta',
            3: 'light_blue',
            4: 'yellow',
            5: 'lime',
            6: 'pink',
            7: 'gray',
            8: 'light_gray',
            9: 'cyan',
            10: 'purple',
            11: 'blue',
            12: 'brown',
            13: 'green',
            14: 'red',
            15: 'black'
        }
    },
    'trader_llama': {
        'tag': 'Variant',
        'default': 'creamy',
        'values': {
            0: 'creamy',
            1: 'white',
            2: 'brown',
            3: 'gray'
        }
    },
    'tropical_fish': {
        'tag': 'Variant',
        'default': '',
        'values': [] # Complex variants based on body, pattern, and colors. Ignored for now.
    },
    'wolf': {
        'tag': 'variant',
        'default': 'pale',
        'values': ['pale', 'ashen', 'black', 'chestnut', 'rusty', 'snowy', 'spotted', 'striped', 'woods']
    },
}