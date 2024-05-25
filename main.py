import pygame
import os
import text
import combat
pygame.font.init()
pygame.mixer.init()

# display
WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
SMALL_TEXT_POS = (0, HEIGHT*0.8)
pygame.display.set_caption("Itsy Bitsy Tiny Game except with Pygame")

# text and colors
TEXT_FONT = pygame.font.SysFont('comicsans', 25)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()

# a gazillion variables for tracking states
walk_index = 0
idle_index_hero = 0
idle_index_sblade = 0
idle_index_fire1 = 0
idle_index_fire2 = 0
facing_right = True
is_walking = False
text_skipped = False
small_text_skipped = True
section_index = 0
death_screen_index = 0
second_puzzle_won = False
third_puzzle_won = False
third_puzzle_init = False
fire_lit = False
potion_drunk = 0

# backgrounds
BG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Background', 'background.png')), (WIDTH, HEIGHT))
TEXT_BG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'UI', 'text_bg.png')), (WIDTH, HEIGHT))
BG_LIGHTNING = pygame.image.load(os.path.join('Assets', 'Background', 'death_lightning.png'))
BG_FALLING = pygame.image.load(os.path.join('Assets', 'Background', 'death_falling.png'))
BG_CRUSHED = pygame.image.load(os.path.join('Assets', 'Background', 'death_crushed.png'))
BG_POISONED = pygame.image.load(os.path.join('Assets', 'Background', 'death_poison.png'))
BG_BURNT = pygame.image.load(os.path.join('Assets', 'Background', 'death_burn.png'))
BG_STUCK = pygame.image.load(os.path.join('Assets', 'Background', 'game_over.png'))
BG_KILLED = pygame.image.load(os.path.join('Assets', 'Background', 'death_killed.png'))
DOOR = pygame.image.load(os.path.join('Assets', 'Background', 'door.png'))
POTIONS = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Background', 'potions.png')), (WIDTH, HEIGHT))
TABLE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'Background', 'table.png')), (128, 128))

# actors
HERO_WIDTH = 128
HERO_HEIGHT = 128
HERO = pygame.Rect(100, HEIGHT // 4 * 3 - HERO_HEIGHT, HERO_WIDTH, HERO_HEIGHT)
HERO_IDLE_LIST = [pygame.image.load(os.path.join('Assets', 'Lavender', 'idle1.png')),
                  pygame.image.load(os.path.join('Assets', 'Lavender', 'idle2.png')),
                  pygame.image.load(os.path.join('Assets', 'Lavender', 'idle3.png')),
                  pygame.image.load(os.path.join('Assets', 'Lavender', 'idle4.png')),
                  pygame.image.load(os.path.join('Assets', 'Lavender', 'idle5.png')),]
SBLADE = pygame.Rect(1180, HEIGHT//4*3 - HERO_HEIGHT, HERO_WIDTH, HERO_HEIGHT)
SBLADE_IDLE_LIST = [pygame.image.load(os.path.join('Assets', 'Spellblade', 'spectre_idle1.png')),
                    pygame.image.load(os.path.join('Assets', 'Spellblade', 'spectre_idle2.png')),
                    pygame.image.load(os.path.join('Assets', 'Spellblade', 'spectre_idle3.png')),
                    pygame.image.load(os.path.join('Assets', 'Spellblade', 'spectre_idle4.png')),
                    pygame.image.load(os.path.join('Assets', 'Spellblade', 'spectre_idle5.png')),
                    pygame.image.load(os.path.join('Assets', 'Spellblade', 'spectre_idle6.png')),
                    pygame.image.load(os.path.join('Assets', 'Spellblade', 'spectre_idle7.png'))]

# arrows and tabs
ARROW_WIDTH = 32
ARROW_HEIGHT = 32
ARROW_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'UI', 'arrow.png')), (ARROW_WIDTH, ARROW_HEIGHT))
arrow_start_pos_first_puzzle = 660, 500
arrow_start_pos_second_puzzle = 304, 58
arrow_start_pos_third_puzzle = 358, 440
TAB_IMAGE = pygame.image.load(os.path.join('Assets', 'UI', 'tab.png'))

# fire animations lists and frame counter
FIRE1_IDLE_LIST = [pygame.image.load(os.path.join('Assets', 'flame1', '00.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '01.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '02.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '03.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '04.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '05.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '06.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '07.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '08.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '09.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '10.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '11.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '12.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '13.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '14.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '15.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '16.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '17.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '18.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '19.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '20.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '21.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '22.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '23.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '24.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '25.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '26.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '27.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '28.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '29.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '30.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '31.png')),
                   pygame.image.load(os.path.join('Assets', 'flame1', '32.png'))]
FIRE2_IDLE_LIST = [pygame.image.load(os.path.join('Assets', 'flame2', '00.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '01.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '02.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '03.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '04.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '05.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '06.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '07.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '08.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '09.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '10.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '11.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '12.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '13.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '14.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '15.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '16.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '17.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '18.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '19.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '20.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '21.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '22.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '23.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '24.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '25.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '26.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '27.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '28.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '29.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '30.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '31.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '32.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '33.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '34.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '35.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '36.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '37.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '38.png')),
                   pygame.image.load(os.path.join('Assets', 'flame2', '39.png'))]
frame_count = 0

# sounds
arrow_movement_sound = pygame.mixer.Sound(os.path.join('Assets', 'Sound', 'hover.wav'))
confirm_sound = pygame.mixer.Sound(os.path.join('Assets', 'Sound', 'confirm.wav'))
fire_sound = pygame.mixer.Sound(os.path.join('Assets', 'Sound', 'fire.wav'))
footstep_sound = pygame.mixer.Sound(os.path.join('Assets', 'Sound', 'step.wav'))


def blit_interact():
    word = TEXT_FONT.render("Press E to interact", 0, BLACK)
    WIN.blit(word, (WIDTH // 2 - word.get_width() // 2, HEIGHT * 0.9))


def handle_idle_hero(hero):
    global idle_index_hero
    global facing_right
    x = hero.left
    y = hero.top

    hero_idle = HERO_IDLE_LIST[idle_index_hero]

    if frame_count % 8 == 0:
        idle_index_hero += 1
    if idle_index_hero >= len(HERO_IDLE_LIST):
        idle_index_hero = 0
    if facing_right:
        WIN.blit(hero_idle, (x, y))
    else:
        WIN.blit(pygame.transform.flip(hero_idle, True, False), (x, y))


def handle_idle_sblade(sblade):
    global idle_index_sblade
    x = sblade.left
    y = sblade.top

    hero_idle = pygame.transform.flip(SBLADE_IDLE_LIST[idle_index_sblade], True, False)

    if frame_count % 8 == 0:
        idle_index_sblade += 1
    if idle_index_sblade >= len(SBLADE_IDLE_LIST):
        idle_index_sblade = 0
    WIN.blit(hero_idle, (x, y))


def handle_idle_fire():
    global idle_index_fire1
    global idle_index_fire2

    fire_width = 200
    fire_height = 200
    list1 = FIRE1_IDLE_LIST
    list2 = FIRE2_IDLE_LIST
    fire1 = pygame.transform.scale(list1[idle_index_fire1], (fire_width, fire_height))
    fire2 = pygame.transform.scale(list2[idle_index_fire2], (fire_width, fire_height))
    y_list = [HEIGHT*0.4, HEIGHT*0.5, HEIGHT*0.6, HEIGHT*0.7, HEIGHT*0.8, HEIGHT*0.9, HEIGHT]

    if idle_index_fire1 == 0:
        fire_sound.play()
    for y in y_list:
        WIN.blit(fire1, (0-80, y))
        WIN.blit(fire2, (WIDTH-fire2.get_width()+80, y))
    if frame_count % 2 == 0:
        idle_index_fire1 += 1
        idle_index_fire2 += 1
    if idle_index_fire1 >= len(list1):
        idle_index_fire1 = 0
    if idle_index_fire2 >= len(list1):
        idle_index_fire2 = 0


def handle_movement(keys_pressed, hero):
    global walk_index
    global facing_right
    x = hero.left
    y = hero.top
    walk_speed = 15

    hero_walk_list = [pygame.image.load(os.path.join('Assets', 'Lavender', 'walk1.png')),
                      pygame.image.load(os.path.join('Assets', 'Lavender', 'walk2.png')),
                      pygame.image.load(os.path.join('Assets', 'Lavender', 'walk3.png')),
                      pygame.image.load(os.path.join('Assets', 'Lavender', 'walk4.png')),
                      pygame.image.load(os.path.join('Assets', 'Lavender', 'walk5.png')),
                      pygame.image.load(os.path.join('Assets', 'Lavender', 'walk6.png')),
                      pygame.image.load(os.path.join('Assets', 'Lavender', 'walk7.png')),
                      pygame.image.load(os.path.join('Assets', 'Lavender', 'walk8.png'))]
    hero_walk = hero_walk_list[walk_index]
    if keys_pressed[pygame.K_a] and hero.x > 0:
        hero.x -= walk_speed
        if frame_count % 10 == 0:
            walk_index += 1
        if walk_index >= len(hero_walk_list):
            walk_index = 0
        facing_right = False

    if keys_pressed[pygame.K_d] and hero.x < WIDTH - hero.width:
        hero.x += walk_speed
        if frame_count % 10 == 0:
            walk_index += 1
        if walk_index >= len(hero_walk_list):
            walk_index = 0
        facing_right = True

    if keys_pressed[pygame.K_w] and hero.y > HEIGHT//3:
        hero.y -= walk_speed
        if frame_count % 10 == 0:
            walk_index += 1
        if walk_index >= len(hero_walk_list):
            walk_index = 0

    if keys_pressed[pygame.K_s] and hero.y < HEIGHT - hero.height:
        hero.y += walk_speed
        if frame_count % 10 == 0:
            walk_index += 1
        if walk_index >= len(hero_walk_list):
            walk_index = 0

    if facing_right:
        WIN.blit(hero_walk, (x, y))
    else:
        WIN.blit(pygame.transform.flip(hero_walk, True, False), (x, y))


def blit_text(keys_pressed, message, position: tuple):
    global text_skipped

    if not text_skipped:
        words = [word.split(' ') for word in message.splitlines()]
        space = TEXT_FONT.size(' ')[0]
        max_width, max_height = WIN.get_size()
        x, y = position
        WIN.blit(TEXT_BG, position)
        for line in words:
            for word in line:
                word_surface = TEXT_FONT.render(word, 0, BLACK)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = position[0]
                    y += word_height
                WIN.blit(word_surface, (x, y))
                x += word_width + space
            x = position[0]
            y += word_height
        if keys_pressed[pygame.K_SPACE]:
            text_skipped = True


def blit_small_text(keys_pressed, message):
    global section_index
    global text_skipped
    global small_text_skipped
    small_text_skipped = False

    if not small_text_skipped:
        word_surface = TEXT_FONT.render(message, 0, BLACK)
        WIN.blit(TEXT_BG, SMALL_TEXT_POS)
        WIN.blit(word_surface, SMALL_TEXT_POS)
    if keys_pressed[pygame.K_SPACE]:
        small_text_skipped = True
        if message is text.first_puzzle_intro() or message is text.second_puzzle_leave():
            section_index += 1


def blit_tooltip(message):
    words = [word.split(' ') for word in message.splitlines()]
    space = TEXT_FONT.size(' ')[0]
    max_width, max_height = WIN.get_size()
    x, y = SMALL_TEXT_POS
    WIN.blit(TEXT_BG, SMALL_TEXT_POS)

    for line in words:
        for word in line:
            word_surface = TEXT_FONT.render(word, 0, BLACK)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = SMALL_TEXT_POS[0]
                y += word_height
            WIN.blit(word_surface, (x, y))
            x += word_width + space
        x = SMALL_TEXT_POS[0]
        y += word_height


def arrow_movement(keys_pressed, arrow, positions: list):
    if keys_pressed[pygame.K_d]:
        arrow_movement_sound.play()
        pygame.time.delay(130)
        if positions.index((arrow.x, arrow.y)) == len(positions)-1:
            arrow.x, arrow.y = positions[0]
        else:
            arrow.x, arrow.y = positions[positions.index((arrow.x, arrow.y))+1]
    if keys_pressed[pygame.K_a]:
        arrow_movement_sound.play()
        pygame.time.delay(130)
        if positions.index((arrow.x, arrow.y)) == 0:
            arrow.x, arrow.y = positions[len(positions)-1]
        else:
            arrow.x, arrow.y = positions[positions.index((arrow.x, arrow.y))-1]


def entrance(keys_pressed, hero):
    global section_index
    global small_text_skipped
    global text_skipped
    WIN.blit(BG, (0, 0))

    if (keys_pressed[pygame.K_a] or keys_pressed[pygame.K_w] or keys_pressed[pygame.K_s] or keys_pressed[pygame.K_d]) and text_skipped and small_text_skipped:
        handle_movement(keys_pressed, HERO)
    elif text_skipped:
        handle_idle_hero(HERO)
    blit_text(keys_pressed, text.intro(), (0, 0))

    if hero.x < 20 and HEIGHT * 0.6 - hero.height < hero.y < HEIGHT * 0.9 - hero.height:
        blit_interact()
        if keys_pressed[pygame.K_e]:
            small_text_skipped = False
        if not small_text_skipped:
            blit_small_text(keys_pressed, text.intro_stalling())

    if hero.x + hero.width > WIDTH - 20 and HEIGHT * 0.6 - hero.height < hero.y < HEIGHT * 0.9 - hero.height:
        blit_interact()
        if keys_pressed[pygame.K_e]:
            small_text_skipped = False
        if not small_text_skipped:
            blit_small_text(keys_pressed, text.first_puzzle_intro())
            if keys_pressed[pygame.K_SPACE]:
                text_skipped = False


def first_puzzle(keys_pressed, arrow):
    global small_text_skipped
    global death_screen_index
    global text_skipped
    global section_index
    arrow_pos_2 = 676, 500
    arrow_pos_3 = 694, 500
    positions = [arrow_start_pos_first_puzzle, arrow_pos_2, arrow_pos_3]
    blit_text(keys_pressed, text.first_puzzle_text(), (0, 0))

    if text_skipped:
        WIN.blit(BG, (0, 0))
        WIN.blit(DOOR, (WIDTH//2 - DOOR.get_width()//2, 0))
        blit_tooltip(text.first_puzzle_text_small())
        arrow_movement(keys_pressed, arrow, positions)
        WIN.blit(ARROW_IMAGE, (arrow.x, arrow.y))

        if keys_pressed[pygame.K_RETURN]:
            confirm_sound.play()
            if (arrow.x, arrow.y) == positions[0]:
                section_index += 1
                text_skipped = False
            elif (arrow.x, arrow.y) == positions[1]:
                death_screen_index = 1
            elif (arrow.x, arrow.y) == positions[2]:
                death_screen_index = 2


def second_puzzle(keys_pressed, arrow, hero):
    global small_text_skipped
    global text_skipped
    global section_index
    global death_screen_index
    global second_puzzle_won
    tab_pos_height = 100
    tab = pygame.transform.scale(TAB_IMAGE, (150, 50))
    tab1 = (WIDTH//4-tab.get_width()//2, tab_pos_height)
    tab2 = (WIDTH//2-tab.get_width()//2, tab_pos_height)
    tab3 = (WIDTH*0.75-tab.get_width()//2, tab_pos_height)
    name1 = TEXT_FONT.render('Kolbert', 1, BLACK)
    name2 = TEXT_FONT.render('Wolfgang', 1, BLACK)
    name3 = TEXT_FONT.render('Chris', 1, BLACK)
    arrow_pos2 = tab2[0]+tab.get_width()//2-arrow.width//2, tab2[1]-arrow.height-10
    arrow_pos3 = tab3[0]+tab.get_width()//2-arrow.width//2, tab3[1]-arrow.height-10
    positions = [arrow_start_pos_second_puzzle, arrow_pos2, arrow_pos3]

    blit_text(keys_pressed, text.second_puzzle_text(), (0, 0))

    if text_skipped and not second_puzzle_won:
        HERO.x, HERO.y = (100, HEIGHT // 4 * 3 - HERO_HEIGHT)
        WIN.blit(BG, (0, 0))
        blit_tooltip(text.second_puzzle_text_small())
        handle_idle_hero(HERO)
        handle_idle_sblade(SBLADE)
        WIN.blit(tab, tab1)
        WIN.blit(tab, tab2)
        WIN.blit(tab, tab3)
        WIN.blit(name1, (tab1[0]+tab.get_width()//2-name1.get_width()//2, tab1[1]+tab.get_height()//2-name1.get_height()//2))
        WIN.blit(name2, (tab2[0]+tab.get_width()//2-name2.get_width()//2, tab2[1]+tab.get_height()//2-name2.get_height()//2))
        WIN.blit(name3, (tab3[0]+tab.get_width()//2-name3.get_width()//2, tab1[1]+tab.get_height()//2-name3.get_height()//2))
        WIN.blit(ARROW_IMAGE, (arrow.x, arrow.y))

        arrow_movement(keys_pressed, arrow, positions)

        if keys_pressed[pygame.K_RETURN]:
            confirm_sound.play()
            if (arrow.x, arrow.y) == positions[0]:
                second_puzzle_won = True
            else:
                death_screen_index = 3

    if text_skipped and second_puzzle_won:
        WIN.blit(BG, (0, 0))
        if (keys_pressed[pygame.K_a] or keys_pressed[pygame.K_w] or keys_pressed[pygame.K_s] or keys_pressed[pygame.K_d]) and small_text_skipped:
            handle_movement(keys_pressed, hero)
        else:
            handle_idle_hero(HERO)

        if hero.x < 20 and HEIGHT * 0.6 - hero.height < hero.y < HEIGHT * 0.9 - hero.height:
            blit_interact()
            if keys_pressed[pygame.K_e]:
                small_text_skipped = False
            if not small_text_skipped:
                blit_small_text(keys_pressed, text.second_puzzle_stalling())
        if hero.x + hero.width > WIDTH - 20 and HEIGHT * 0.6 - hero.height < hero.y < HEIGHT * 0.9 - hero.height:
            blit_interact()
            if keys_pressed[pygame.K_e]:
                small_text_skipped = False
            if not small_text_skipped:
                blit_small_text(keys_pressed, text.second_puzzle_leave())
                if keys_pressed[pygame.K_SPACE]:
                    HERO.x, HERO.y = (100, HEIGHT // 4 * 3 - HERO_HEIGHT)


def third_puzzle(keys_pressed, arrow):
    global potion_drunk
    global third_puzzle_won
    global third_puzzle_init
    global death_screen_index
    arrow_pos2 = 427, 384
    arrow_pos3 = 489, 458
    arrow_pos4 = 546, 366
    arrow_pos5 = 609, 440
    arrow_pos6 = 672, 330
    arrow_pos7 = 737, 440
    positions = [arrow_start_pos_third_puzzle, arrow_pos2, arrow_pos3, arrow_pos4, arrow_pos5, arrow_pos6, arrow_pos7]

    WIN.blit(POTIONS, (0, 0))
    WIN.blit(ARROW_IMAGE, (arrow.x, arrow.y))
    blit_tooltip(text.third_puzzle_small_text())

    arrow_movement(keys_pressed, arrow, positions)

    if keys_pressed[pygame.K_RETURN]:
        confirm_sound.play()
        if (arrow.x, arrow.y) == positions[2]:
            potion_drunk = 1
            # go forward
        elif (arrow.x, arrow.y) == positions[6]:
            potion_drunk = 2
            # go back
        elif (arrow.x, arrow.y) == positions[1] or (arrow.x, arrow.y) == positions[5]:
            potion_drunk = 3
            # wine
        else:
            death_screen_index = 4
            # poison
        third_puzzle_init = False


def third_puzzle_room(keys_pressed, hero, arrow):
    global section_index
    global death_screen_index
    global third_puzzle_init
    global text_skipped
    global small_text_skipped
    global fire_lit
    WIN.blit(BG, (0, 0))
    WIN.blit(TABLE, (WIDTH//2-TABLE.get_width()//2, HEIGHT*0.55))
    if (keys_pressed[pygame.K_a] or keys_pressed[pygame.K_d] or keys_pressed[pygame.K_w] or keys_pressed[pygame.K_s]) and text_skipped and small_text_skipped and not third_puzzle_init:
        fire_lit = True
        handle_movement(keys_pressed, hero)
    elif text_skipped:
        handle_idle_hero(hero)
    if fire_lit:
        handle_idle_fire()

    if hero.x < 20 and HEIGHT * 0.6 - hero.height < hero.y < HEIGHT * 0.9 - hero.height:
        blit_interact()
        if keys_pressed[pygame.K_e]:
            small_text_skipped = False
            if potion_drunk == 2:
                death_screen_index = 5
            elif potion_drunk != 0:
                death_screen_index = 6
        if potion_drunk == 0 and not small_text_skipped:
            blit_small_text(keys_pressed, "That looks too deadly to enter.")

    if hero.x + hero.width > WIDTH - 20 and HEIGHT * 0.6 - hero.height < hero.y < HEIGHT * 0.9 - hero.height:
        blit_interact()
        if keys_pressed[pygame.K_e]:
            small_text_skipped = False
            if potion_drunk != 0 and potion_drunk != 1:
                death_screen_index = 6
            elif potion_drunk == 1:
                text_skipped = False
                section_index += 1
        if not small_text_skipped and potion_drunk == 0:
            blit_small_text(keys_pressed, "That looks too deadly to enter.")

    if WIDTH//2-TABLE.get_width()//2+64 > hero.x > WIDTH//2-TABLE.get_width()//2-64 and HEIGHT*0.55+64 > hero.y > HEIGHT*0.55-64 and not third_puzzle_won and not third_puzzle_init:
        blit_interact()
        if keys_pressed[pygame.K_e]:
            text_skipped = False
        if not text_skipped:
            blit_text(keys_pressed, text.third_puzzle_text(), (0, 0))
            if keys_pressed[pygame.K_SPACE]:
                third_puzzle_init = True
    if third_puzzle_init:
        third_puzzle(keys_pressed, arrow)


def death(keys_pressed):
    if death_screen_index == 1:
        WIN.blit(BG_LIGHTNING, (0, 0))
        blit_small_text(keys_pressed, "A bolt of lightning shoots off the ceiling and murders you to death.")
    if death_screen_index == 2:
        WIN.blit(BG_FALLING, (0, 0))
        blit_small_text(keys_pressed, "The floor under your feet disappears and you fall to your death.")
    if death_screen_index == 3:
        WIN.blit(BG_CRUSHED, (0, 0))
        blit_small_text(keys_pressed, '"Wrong!" the spellblade spectre laughs. Then, a massive stone slab falls from the ceiling an crushes you.')
    if death_screen_index == 4:
        WIN.blit(BG_POISONED, (0, 0))
        blit_small_text(keys_pressed, "You drink a potion. Well, more like a potion with an s and the third and fourth letters swapped.")
    if death_screen_index == 5:
        WIN.blit(BG_STUCK, (0, 0))
        blit_small_text(keys_pressed, "As you pass through the flames, the door behind you slams shut, cutting you off from the Spellblade.")
    if death_screen_index == 6:
        WIN.blit(BG_BURNT, (0, 0))
        blit_small_text(keys_pressed, "The look of a pile of ash does not suit you.")
    if death_screen_index == 7:
        WIN.blit(BG_KILLED, (0, 0))
        blit_small_text(keys_pressed, "You'd hear the spellblade laugh maniacally but that's kinda hard to do when you're dead.")
    if keys_pressed[pygame.K_SPACE]:
        quit()


def main():
    global frame_count
    global text_skipped
    arrow1 = pygame.Rect(arrow_start_pos_first_puzzle[0], arrow_start_pos_first_puzzle[1], ARROW_WIDTH, ARROW_HEIGHT)
    arrow2 = pygame.Rect(arrow_start_pos_second_puzzle[0], arrow_start_pos_second_puzzle[1], ARROW_WIDTH, ARROW_HEIGHT)
    arrow3 = pygame.Rect(arrow_start_pos_third_puzzle[0], arrow_start_pos_third_puzzle[1], ARROW_WIDTH, ARROW_HEIGHT)
    # arrow x and y has to be same as the starting position in the corresponding function because the arrow's movement
    # depends on the current location and setting it in the function makes it reset all the time because of while loop
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        keys_pressed = pygame.key.get_pressed()
        if death_screen_index != 0:
            death(keys_pressed)
        elif section_index == 0:
            entrance(keys_pressed, HERO)
        elif section_index == 1:
            first_puzzle(keys_pressed, arrow1)
        elif section_index == 2:
            second_puzzle(keys_pressed, arrow2, HERO)
        elif section_index == 3:
            third_puzzle_room(keys_pressed, HERO, arrow3)
        elif section_index == 4:
            blit_text(keys_pressed, text.meeting(), (0, 0))
            if text_skipped:
                combat.combat()
        if frame_count >= 10000:
            frame_count = 0
        frame_count += 1
        pygame.display.update()


if __name__ == "__main__":
    main()


