import os
import pygame
import random
import main
import text
pygame.font.init()
pygame.mixer.init()


class Character:

    def __init__(self, name, hp, damage, spell_damage):
        self.name = name
        self.hp = hp
        self.hp_max = hp
        self.damage = damage
        self.spell_damage = spell_damage
        self.turn_count = 0
        self.is_parrying = False
        self.is_casting = False
        self.is_interrupting = False
        self.is_preparing_attack = False
        self.is_preparing_spell = False
        self.is_idle = True
        self.is_moving = False
        self.is_moving_forward = True
        self.is_taking_damage = False
        self.animation_index = 0
        self.spell_fired = False
        self.playing_attack_animation = False
        self.status_message = ''
        self.idle_index = 0
        self.is_dead = False


# display
WIDTH, HEIGHT = main.WIDTH, main.HEIGHT
WIN = main.WIN

# backgrounds
BG = pygame.image.load(os.path.join('Assets', 'Background', 'background2.png'))
TEXT_BG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'UI', 'text_bg.png')), (WIDTH, HEIGHT))

# clock
clock = pygame.time.Clock()
frame_count = 0

# text and color
TEXT_FONT = pygame.font.SysFont('comicsans', 18)
BLACK = (0, 0, 0)

# healthbar images
HEALTHBAR = pygame.image.load(os.path.join('Assets', 'UI', 'healthbar.png'))
HEALTHBAR_SEGMENT = pygame.image.load(os.path.join('Assets', 'UI', 'healthbar_segment.png'))

# sounds
slash_sound = pygame.mixer.Sound(os.path.join('Assets', 'Sound', 'slash.wav'))
block_sound = pygame.mixer.Sound(os.path.join('Assets', 'Sound', 'block.wav'))
thunder_sound = pygame.mixer.Sound(os.path.join('Assets', 'Sound', 'thunder.wav'))

# actors, their rectangles and movement speed
lavender = Character(name="Lavender", hp=100, damage=10, spell_damage=10)
sblade = Character(name="Spellblade", hp=150, damage=7, spell_damage=11)
CHAR_WIDTH = 128
CHAR_HEIGHT = 128
lav_rect = pygame.Rect(300, HEIGHT*0.4, CHAR_WIDTH, CHAR_HEIGHT)
sblade_rect = pygame.Rect(980-CHAR_WIDTH, HEIGHT*0.4, CHAR_WIDTH, CHAR_HEIGHT)
movement_speed = 40

# stuff for spell projectiles
SPELL_WIDTH = 64
SPELL_HEIGHT = 64
lav_spell_rect = pygame.Rect(300+CHAR_WIDTH-35, HEIGHT*0.4+CHAR_HEIGHT//2-8, SPELL_WIDTH, SPELL_HEIGHT)
sblade_spell_rect = pygame.Rect(980-CHAR_WIDTH-SPELL_WIDTH+40, HEIGHT*0.4+CHAR_HEIGHT//2-10, SPELL_WIDTH, SPELL_HEIGHT)
anim_index_lav = 0
spell_anim_index = 0
spell_explosion_playing = False

# actor positions for movement
lavender_end_pos = 800
lavender_start_pos = 300
sblade_end_pos = 350
sblade_end_pos_channeled_spell = 373
sblade_start_pos = 800 + sblade_rect.width

# arrow positions and tabs
ARROW_WIDTH = 32
ARROW_HEIGHT = 32
ARROW_IMAGE = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'UI', 'arrow.png')), (ARROW_WIDTH, ARROW_HEIGHT)), 270)
TAB_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'UI', 'tab.png')), (120, 40))
pos4 = (10+TAB_IMAGE.get_width()+5, HEIGHT*0.8-TAB_IMAGE.get_height()+5)
pos3 = (10+TAB_IMAGE.get_width()+5, HEIGHT*0.8-TAB_IMAGE.get_height()*2+5)
pos2 = (10+TAB_IMAGE.get_width()+5, HEIGHT*0.8-TAB_IMAGE.get_height()*3+5)
pos1 = (10+TAB_IMAGE.get_width()+5, HEIGHT*0.8-TAB_IMAGE.get_height()*4+5)
positions = [pos1, pos2, pos3, pos4]
arrow_rect = pygame.Rect(pos1[0], pos1[1], ARROW_WIDTH, ARROW_HEIGHT)

# stuff for handling turns
virtual_keypress = False
action_generated = False
third_status_message = ''
action = 0
player_turn = True
keys_locked = False

# animations lists
LAVENDER_ATTACK_LIST = [pygame.image.load(os.path.join('Assets', 'Lavender', 'attack1.png')),
                        pygame.image.load(os.path.join('Assets', 'Lavender', 'attack2.png')),
                        pygame.image.load(os.path.join('Assets', 'Lavender', 'attack3.png')),
                        pygame.image.load(os.path.join('Assets', 'Lavender', 'attack4.png')),
                        pygame.image.load(os.path.join('Assets', 'Lavender', 'attack5.png'))]
LAVENDER_SPELL_LIST = [pygame.image.load(os.path.join('Assets', 'Lavender', 'spell1.png')),
                       pygame.image.load(os.path.join('Assets', 'Lavender', 'spell2.png')),
                       pygame.image.load(os.path.join('Assets', 'Lavender', 'spell3.png')),
                       pygame.image.load(os.path.join('Assets', 'Lavender', 'spell4.png')),]
LAVENDER_PARRY_LIST = [pygame.image.load(os.path.join('Assets', 'Lavender', 'protect1.png')),
                       pygame.image.load(os.path.join('Assets', 'Lavender', 'protect2.png'))]
LAVENDER_MAGIC_MISSILE_LIST = [pygame.image.load(os.path.join('Assets', 'Lavender', 'magic1.png')),
                               pygame.image.load(os.path.join('Assets', 'Lavender', 'magic2.png')),
                               pygame.image.load(os.path.join('Assets', 'Lavender', 'magic3.png')),
                               pygame.image.load(os.path.join('Assets', 'Lavender', 'magic4.png')),
                               pygame.image.load(os.path.join('Assets', 'Lavender', 'magic5.png')),
                               pygame.image.load(os.path.join('Assets', 'Lavender', 'magic6.png'))]
LAVENDER_DEAD_LIST = [pygame.image.load(os.path.join('Assets', 'Lavender', 'dead1.png')),
                      pygame.image.load(os.path.join('Assets', 'Lavender', 'dead2.png')),
                      pygame.image.load(os.path.join('Assets', 'Lavender', 'dead3.png')),
                      pygame.image.load(os.path.join('Assets', 'Lavender', 'dead4.png')),
                      pygame.image.load(os.path.join('Assets', 'Lavender', 'dead5.png')),
                      pygame.image.load(os.path.join('Assets', 'Lavender', 'dead6.png')),
                      pygame.image.load(os.path.join('Assets', 'Lavender', 'dead7.png')),
                      pygame.image.load(os.path.join('Assets', 'Lavender', 'dead8.png'))]
LAVENDER_IDLE_LIST = [pygame.image.load(os.path.join('Assets', 'Lavender', 'idle1.png')),
                      pygame.image.load(os.path.join('Assets', 'Lavender', 'idle2.png')),
                      pygame.image.load(os.path.join('Assets', 'Lavender', 'idle3.png')),
                      pygame.image.load(os.path.join('Assets', 'Lavender', 'idle4.png')),
                      pygame.image.load(os.path.join('Assets', 'Lavender', 'idle5.png')),]
LAVENDER_HURT_LIST = [pygame.image.load(os.path.join('Assets', 'Lavender', 'hurt.png')),
                      pygame.image.load(os.path.join('Assets', 'Lavender', 'hurt.png')),
                      pygame.image.load(os.path.join('Assets', 'Lavender', 'hurt.png')),
                      pygame.image.load(os.path.join('Assets', 'Lavender', 'hurt.png')),
                      pygame.image.load(os.path.join('Assets', 'Lavender', 'hurt.png'))]
SBLADE_ATTACK_LIST = [pygame.image.load(os.path.join('Assets', 'Spellblade', 'attack1.png')),
                      pygame.image.load(os.path.join('Assets', 'Spellblade', 'attack2.png')),
                      pygame.image.load(os.path.join('Assets', 'Spellblade', 'attack3.png')),
                      pygame.image.load(os.path.join('Assets', 'Spellblade', 'attack4.png'))]
SBLADE_SPELL_LIST = [pygame.image.load(os.path.join('Assets', 'Spellblade', 'fireball1.png')),
                     pygame.image.load(os.path.join('Assets', 'Spellblade', 'fireball2.png')),
                     pygame.image.load(os.path.join('Assets', 'Spellblade', 'fireball3.png')),
                     pygame.image.load(os.path.join('Assets', 'Spellblade', 'fireball4.png')),
                     pygame.image.load(os.path.join('Assets', 'Spellblade', 'fireball5.png')),
                     pygame.image.load(os.path.join('Assets', 'Spellblade', 'fireball6.png')),
                     pygame.image.load(os.path.join('Assets', 'Spellblade', 'fireball7.png')),
                     pygame.image.load(os.path.join('Assets', 'Spellblade', 'fireball8.png'))]
SBLADE_CHARGED_ATTACK1_LIST = [pygame.image.load(os.path.join('Assets', 'Spellblade', 'charged_attack1.png')),
                               pygame.image.load(os.path.join('Assets', 'Spellblade', 'charged_attack2.png'))]
SBLADE_CHARGED_ATTACK2_LIST = [pygame.image.load(os.path.join('Assets', 'Spellblade', 'charged_attack3.png')),
                               pygame.image.load(os.path.join('Assets', 'Spellblade', 'charged_attack4.png'))]
SBLADE_CHARGED_SPELL1_LIST = [pygame.image.load(os.path.join('Assets', 'Spellblade', 'flamejet1.png')),
                              pygame.image.load(os.path.join('Assets', 'Spellblade', 'flamejet2.png'))]
SBLADE_CHARGED_SPELL2_LIST = [pygame.image.load(os.path.join('Assets', 'Spellblade', 'flamejet3.png')),
                              pygame.image.load(os.path.join('Assets', 'Spellblade', 'flamejet4.png')),
                              pygame.image.load(os.path.join('Assets', 'Spellblade', 'flamejet5.png')),
                              pygame.image.load(os.path.join('Assets', 'Spellblade', 'flamejet6.png')),
                              pygame.image.load(os.path.join('Assets', 'Spellblade', 'flamejet7.png')),
                              pygame.image.load(os.path.join('Assets', 'Spellblade', 'flamejet8.png')),
                              pygame.image.load(os.path.join('Assets', 'Spellblade', 'flamejet9.png')),
                              pygame.image.load(os.path.join('Assets', 'Spellblade', 'flamejet10.png')),
                              pygame.image.load(os.path.join('Assets', 'Spellblade', 'flamejet11.png')),
                              pygame.image.load(os.path.join('Assets', 'Spellblade', 'flamejet12.png')),
                              pygame.image.load(os.path.join('Assets', 'Spellblade', 'flamejet13.png')),
                              pygame.image.load(os.path.join('Assets', 'Spellblade', 'flamejet14.png'))]
SBLADE_MAGIC_MISSLE1_LIST = [pygame.image.load(os.path.join('Assets', 'Spellblade', 'magic1.png')),
                             pygame.image.load(os.path.join('Assets', 'Spellblade', 'magic2.png')),
                             pygame.image.load(os.path.join('Assets', 'Spellblade', 'magic3.png')),
                             pygame.image.load(os.path.join('Assets', 'Spellblade', 'magic4.png')),
                             pygame.image.load(os.path.join('Assets', 'Spellblade', 'magic5.png'))]
SBLADE_MAGIC_MISSLE2_LIST = [pygame.image.load(os.path.join('Assets', 'Spellblade', 'magic6.png')),
                             pygame.image.load(os.path.join('Assets', 'Spellblade', 'magic7.png')),
                             pygame.image.load(os.path.join('Assets', 'Spellblade', 'magic8.png')),
                             pygame.image.load(os.path.join('Assets', 'Spellblade', 'magic9.png')),
                             pygame.image.load(os.path.join('Assets', 'Spellblade', 'magic10.png')),
                             pygame.image.load(os.path.join('Assets', 'Spellblade', 'magic11.png')),
                             pygame.image.load(os.path.join('Assets', 'Spellblade', 'magic12.png'))]
SBLADE_IDLE_LIST = [pygame.image.load(os.path.join('Assets', 'Spellblade', 'idle1.png')),
                    pygame.image.load(os.path.join('Assets', 'Spellblade', 'idle2.png')),
                    pygame.image.load(os.path.join('Assets', 'Spellblade', 'idle3.png')),
                    pygame.image.load(os.path.join('Assets', 'Spellblade', 'idle4.png')),
                    pygame.image.load(os.path.join('Assets', 'Spellblade', 'idle5.png')),
                    pygame.image.load(os.path.join('Assets', 'Spellblade', 'idle6.png')),
                    pygame.image.load(os.path.join('Assets', 'Spellblade', 'idle7.png'))]
SBLADE_HURT_LIST = [pygame.image.load(os.path.join('Assets', 'Spellblade', 'hurt1.png')),
                    pygame.image.load(os.path.join('Assets', 'Spellblade', 'hurt2.png')),
                    pygame.image.load(os.path.join('Assets', 'Spellblade', 'hurt3.png'))]
SBLADE_DEAD_LIST = [pygame.image.load(os.path.join('Assets', 'Spellblade', 'dead1.png')),
                    pygame.image.load(os.path.join('Assets', 'Spellblade', 'dead2.png')),
                    pygame.image.load(os.path.join('Assets', 'Spellblade', 'dead3.png')),
                    pygame.image.load(os.path.join('Assets', 'Spellblade', 'dead4.png')),
                    pygame.image.load(os.path.join('Assets', 'Spellblade', 'dead5.png')),
                    pygame.image.load(os.path.join('Assets', 'Spellblade', 'dead6.png'))]
SBLADE_PARRY_LIST = [pygame.image.load(os.path.join('Assets', 'Spellblade', 'parry.png')),
                     pygame.image.load(os.path.join('Assets', 'Spellblade', 'parry.png')),
                     pygame.image.load(os.path.join('Assets', 'Spellblade', 'parry.png')),
                     pygame.image.load(os.path.join('Assets', 'Spellblade', 'parry.png')),
                     pygame.image.load(os.path.join('Assets', 'Spellblade', 'parry.png')),
                     pygame.image.load(os.path.join('Assets', 'Spellblade', 'parry.png')),]
SBLADE_INTERRUPT_LIST = [pygame.image.load(os.path.join('Assets', 'Spellblade', 'interrupt.png')),
                         pygame.image.load(os.path.join('Assets', 'Spellblade', 'interrupt.png')),
                         pygame.image.load(os.path.join('Assets', 'Spellblade', 'interrupt.png')),
                         pygame.image.load(os.path.join('Assets', 'Spellblade', 'interrupt.png')),
                         pygame.image.load(os.path.join('Assets', 'Spellblade', 'interrupt.png')),
                         pygame.image.load(os.path.join('Assets', 'Spellblade', 'interrupt.png'))]


def healthbars():
    WIN.blit(HEALTHBAR, (lav_rect.x, lav_rect.y-10))
    for i in range(lavender.hp//(lavender.hp_max//10)):
        WIN.blit(HEALTHBAR_SEGMENT, (lav_rect.x+4+12*i, lav_rect.y-10))
    WIN.blit(HEALTHBAR, (sblade_rect.x, sblade_rect.y-10))
    for i in range(sblade.hp//(sblade.hp_max//10)):
        WIN.blit(HEALTHBAR_SEGMENT, (sblade_rect.x+4+12*i, sblade_rect.y-10))


def status_messages():
    status_lavender_render = TEXT_FONT.render(lavender.status_message, 1, BLACK)
    status_sblade_render = TEXT_FONT.render(sblade.status_message, 1, BLACK)
    satus_third_render = TEXT_FONT.render(third_status_message, 1, BLACK)
    WIN.blit(status_lavender_render, (10, HEIGHT*0.8))
    WIN.blit(status_sblade_render, (10, HEIGHT*0.8+status_lavender_render.get_height()))
    WIN.blit(satus_third_render, (10, HEIGHT*0.8+status_lavender_render.get_height()*2))


def lavender_idle_animations():
    if lavender.hp <= 0:
        if lavender.idle_index >= len(LAVENDER_DEAD_LIST):
            WIN.blit(LAVENDER_DEAD_LIST[lavender.idle_index-1], (lav_rect.x, lav_rect.y))
            pygame.time.delay(100)
            lavender.is_dead = True
        else:
            WIN.blit(LAVENDER_DEAD_LIST[lavender.idle_index], (lav_rect.x, lav_rect.y))
            if frame_count % 8 == 0:
                lavender.idle_index += 1
    elif lavender.is_parrying or lavender.is_interrupting:
        if lavender.idle_index >= len(LAVENDER_PARRY_LIST):
            lavender.idle_index = 0
        WIN.blit(LAVENDER_PARRY_LIST[lavender.idle_index], (lav_rect.x, lav_rect.y))
        if frame_count % 20 == 0:
            lavender.idle_index += 1
    elif lavender.is_taking_damage:
        if lavender.idle_index >= len(LAVENDER_HURT_LIST):
            lavender.idle_index = 0
            lavender.is_taking_damage = False
        WIN.blit(LAVENDER_HURT_LIST[lavender.idle_index], (lav_rect.x, lav_rect.y))
        lavender.idle_index += 1
    elif lavender.is_idle:
        if lavender.idle_index >= len(LAVENDER_IDLE_LIST):
            lavender.idle_index = 0
        WIN.blit(LAVENDER_IDLE_LIST[lavender.idle_index], (lav_rect.x, lav_rect.y))
        if frame_count % 8 == 0:
            lavender.idle_index += 1


def sblade_idle_animations():
    if sblade.hp <= 0:
        if sblade.idle_index >= len(SBLADE_DEAD_LIST):
            WIN.blit(SBLADE_DEAD_LIST[sblade.idle_index-1], (sblade_rect.x, sblade_rect.y))
            pygame.time.delay(100)
            sblade.is_dead = True
        else:
            WIN.blit(SBLADE_DEAD_LIST[sblade.idle_index], (sblade_rect.x, sblade_rect.y))
            if frame_count % 6 == 0:
                sblade.idle_index += 1
    elif sblade.is_preparing_attack and not sblade.playing_attack_animation and sblade.is_idle:
        if sblade.idle_index >= len(SBLADE_CHARGED_ATTACK1_LIST):
            sblade.idle_index = 0
        WIN.blit(SBLADE_CHARGED_ATTACK1_LIST[sblade.idle_index], (sblade_rect.x, sblade_rect.y))
        if frame_count % 25 == 0:
            sblade.idle_index += 1
    elif sblade.is_preparing_spell and not sblade.playing_attack_animation and sblade.is_idle:
        if sblade.idle_index >= len(SBLADE_CHARGED_SPELL1_LIST):
            sblade.idle_index = 0
        WIN.blit(SBLADE_CHARGED_SPELL1_LIST[sblade.idle_index], (sblade_rect.x, sblade_rect.y))
        if frame_count % 25 == 0:
            sblade.idle_index += 1
    elif sblade.is_taking_damage:
        if sblade.idle_index >= len(SBLADE_HURT_LIST):
            sblade.idle_index = 0
            sblade.is_taking_damage = False
        WIN.blit(SBLADE_HURT_LIST[sblade.idle_index], (sblade_rect.x, sblade_rect.y))
        if frame_count % 6 == 0:
            sblade.idle_index += 1
    elif sblade.is_interrupting:
        if sblade.idle_index >= len(SBLADE_INTERRUPT_LIST):
            sblade.idle_index = 0
        WIN.blit(SBLADE_INTERRUPT_LIST[sblade.idle_index], (sblade_rect.x, sblade_rect.y))
        sblade.idle_index += 1
    elif sblade.is_parrying:
        if sblade.idle_index >= len(SBLADE_PARRY_LIST):
            sblade.idle_index = 0
        WIN.blit(SBLADE_PARRY_LIST[sblade.idle_index], (sblade_rect.x, sblade_rect.y))
    elif sblade.is_idle:
        if sblade.idle_index >= len(SBLADE_IDLE_LIST):
            sblade.idle_index = 0
        WIN.blit(SBLADE_IDLE_LIST[sblade.idle_index], (sblade_rect.x, sblade_rect.y))
        if frame_count % 8 == 0:
            sblade.idle_index += 1


def arrow_movement(keys_pressed, arrow):
    if keys_pressed[pygame.K_s]:
        main.arrow_movement_sound.play()
        pygame.time.delay(130)
        if positions.index((arrow.x, arrow.y)) == len(positions)-1:
            arrow.x, arrow.y = positions[0]
        else:
            arrow.x, arrow.y = positions[positions.index((arrow.x, arrow.y))+1]
    if keys_pressed[pygame.K_w]:
        main.arrow_movement_sound.play()
        pygame.time.delay(130)
        if positions.index((arrow.x, arrow.y)) == 0:
            arrow.x, arrow.y = positions[len(positions)-1]
        else:
            arrow.x, arrow.y = positions[positions.index((arrow.x, arrow.y))-1]


def attack_animation(actor, target, animation: list):
    actor.is_idle = False
    actor.playing_attack_animation = True
    if actor.animation_index >= len(animation):
        actor.animation_index = 0
        actor.playing_attack_animation = False
        if target.is_parrying:
            target.is_parrying = False
            actor.status_message = f"{actor.name}'s attack was parried by {target.name}"
            block_sound.play()
        elif not target.is_parrying:
            if target.is_interrupting:
                target.status_message = f"{actor.name}'s attack causes {target.name} to lose concentration on the counterspell"
            target.is_interrupting = False
            target.hp -= actor.damage
            target.is_taking_damage = True
            actor.playing_attack_animation = False
            target.idle_index = 0
            actor.status_message = f"{actor.name} deals {actor.damage} damage to {target.name}"
            slash_sound.play()
        actor.is_moving = True
        actor.is_moving_forward = False
        actor.is_idle = True

    if actor is lavender:
        WIN.blit(animation[actor.animation_index], (lav_rect.x, lav_rect.y))
    elif actor is sblade:
        WIN.blit(animation[actor.animation_index], (sblade_rect.x, sblade_rect.y))
    if frame_count % 5 == 0:
        actor.animation_index += 1


def spell_cast_animation(actor, animation: list):
    actor.is_idle = False
    if actor.animation_index >= len(animation):
        actor.animation_index = 0
        actor.is_idle = True
        actor.is_casting = False
        actor.spell_fired = True
        if actor is lavender:
            thunder_sound.play()
        elif actor is sblade:
            main.fire_sound.play()

    if actor is lavender:
        WIN.blit(animation[actor.animation_index], (lav_rect.x, lav_rect.y))
    elif actor is sblade:
        WIN.blit(animation[actor.animation_index], (sblade_rect.x, sblade_rect.y))
    if frame_count % 6 == 0:
        actor.animation_index += 1


def attack(actor, target, animation: list):
    global virtual_keypress
    global player_turn
    global keys_locked
    global action_generated

    if actor is lavender:
        if actor.is_moving and actor.is_moving_forward:
            lav_rect.x += movement_speed
            if lav_rect.x > lavender_end_pos:
                actor.is_moving = False
    elif actor is sblade:
        if actor.is_moving and actor.is_moving_forward:
            sblade_rect.x -= movement_speed
            if sblade_rect.x < sblade_end_pos:
                actor.is_moving = False

    if actor is lavender:
        if lav_rect.x > lavender_end_pos:
            attack_animation(actor, target, animation)
    elif actor is sblade:
        if sblade_rect.x < sblade_end_pos:
            attack_animation(actor, target, animation)

    if actor is lavender:
        if actor.is_moving and not actor.is_moving_forward and lav_rect.x > lavender_start_pos:
            lav_rect.x -= movement_speed
            if lav_rect.x <= lavender_start_pos:
                actor.is_moving = False
                keys_locked = False
                actor.turn_count += 1
                action_generated = False
                player_turn = not player_turn
    if actor is sblade:
        if actor.is_moving and not actor.is_moving_forward and sblade_rect.x < sblade_start_pos:
            sblade_rect.x += movement_speed
            if sblade_rect.x >= sblade_start_pos:
                actor.is_moving = False
                virtual_keypress = False
                keys_locked = False
                actor.turn_count += 1
                sblade.is_preparing_attack = False
                sblade.is_preparing_spell = False
                action_generated = False
                player_turn = not player_turn


def spell(actor, target):
    global player_turn
    global spell_anim_index
    global keys_locked
    global spell_explosion_playing
    global action_generated
    global virtual_keypress

    if actor is lavender:
        animation = LAVENDER_SPELL_LIST
    elif actor is sblade:
        animation = SBLADE_SPELL_LIST

    if actor.is_casting:
        spell_cast_animation(actor, animation)

    if actor.spell_fired:
        if not target.is_interrupting:
            if actor is lavender:
                if spell_anim_index >= len(LAVENDER_MAGIC_MISSILE_LIST):
                    WIN.blit(LAVENDER_MAGIC_MISSILE_LIST[spell_anim_index-1], (lav_spell_rect.x, lav_spell_rect.y))
                else:
                    WIN.blit(LAVENDER_MAGIC_MISSILE_LIST[spell_anim_index], (lav_spell_rect.x, lav_spell_rect.y))
                    spell_anim_index += 1
                if lav_spell_rect.x < 880:
                    lav_spell_rect.x += 10
            if actor is sblade:
                if spell_anim_index >= len(SBLADE_MAGIC_MISSLE1_LIST):
                    WIN.blit(SBLADE_MAGIC_MISSLE1_LIST[spell_anim_index-1], (sblade_spell_rect.x, sblade_spell_rect.y))
                else:
                    WIN.blit(SBLADE_MAGIC_MISSLE1_LIST[spell_anim_index], (sblade_spell_rect.x, sblade_spell_rect.y))
                    if frame_count % 5 == 0:
                        spell_anim_index += 1
                if sblade_spell_rect.x > 350:
                    sblade_spell_rect.x -= 10
        elif target.is_interrupting:
            target.is_interrupting = False
            target.status_message = f"{target.name} interrupted {actor.name}'s spell."
            actor.spell_fired = False
            actor.turn_count += 1
            keys_locked = False
            virtual_keypress = False
            action_generated = False
            player_turn = not player_turn

    if lav_spell_rect.x >= 880:
        if target.is_parrying:
            sblade.status_message = f"{actor.name}'s spell causes {target.name} to drop his guard."
        target.is_parrying = False
        target.hp -= actor.spell_damage
        target.is_taking_damage = True
        target.idle_index = 0
        actor.status_message = f"{actor.name} deals {actor.spell_damage} damage to {target.name}."
        actor.spell_fired = False
        lav_spell_rect.x = 300+CHAR_WIDTH-35
        spell_anim_index = 0
        actor.turn_count += 1
        action_generated = False
        keys_locked = False
        player_turn = not player_turn
    if sblade_spell_rect.x <= 350:
        if target.is_parrying:
            lavender.status_message = f"{actor.name}'s spell causes {target.name} to drop his guard."
        target.is_parrying = False
        target.hp -= actor.spell_damage
        target.is_taking_damage = True
        target.idle_index = 0
        actor.status_message = f"{actor.name} deals {actor.spell_damage} damage to {target.name}."
        spell_explosion_playing = True
        actor.spell_fired = False
        sblade_spell_rect.x = 980-CHAR_WIDTH-SPELL_WIDTH+40
        spell_anim_index = 0
        actor.turn_count += 1
        keys_locked = False
        action_generated = False
        virtual_keypress = False
        player_turn = not player_turn


def channeled_attack_animation(actor, target, animation: list):
    actor.is_idle = False
    actor.playing_attack_animation = True

    if actor.animation_index >= len(animation):
        actor.animation_index = 0
        actor.playing_attack_animation = False
        if target.is_parrying and animation is SBLADE_CHARGED_ATTACK2_LIST:
            target.is_parrying = False
            actor.status_message = f"{actor.name}'s attack was parried by {target.name}"
            block_sound.play()
        elif not target.is_parrying and animation is SBLADE_CHARGED_ATTACK2_LIST:
            if target.is_interrupting:
                target.status_message = f"{actor.name}'s attack causes {target.name} to lose concentration on the counterspell"
                target.is_interrupting = False
            target.hp -= actor.damage*2
            target.is_taking_damage = True
            actor.playing_attack_animation = False
            target.idle_index = 0
            actor.status_message = f"{actor.name} deals {str(int(actor.damage)*2)} damage to {target.name}"
            slash_sound.play()
        elif not target.is_interrupting and animation is SBLADE_CHARGED_SPELL2_LIST:
            if target.is_parrying:
                target.status_message = f"{actor.name}'s spell causes {target.name} to drop his guard."
                target.is_parrying = False
            target.hp -= actor.spell_damage*2
            target.is_taking_damage = True
            actor.playing_attack_animation = False
            target.idle_index = 0
            actor.status_message = f"{actor.name} deals {str(int(actor.spell_damage)*2)} damage to {target.name}"
        actor.is_moving = True
        actor.is_moving_forward = False
        actor.is_idle = True

    WIN.blit(animation[actor.animation_index], (sblade_rect.x, sblade_rect.y))
    if animation is SBLADE_CHARGED_ATTACK2_LIST:
        if frame_count % 25 == 0:
            actor.animation_index += 1
    elif animation is SBLADE_CHARGED_SPELL2_LIST:
        if frame_count % 7 == 0:
            actor.animation_index += 1


def channeled_attack(actor, target, animation: list):
    global virtual_keypress
    global player_turn
    global keys_locked
    global action_generated

    if animation is SBLADE_CHARGED_ATTACK2_LIST:
        end_pos = sblade_end_pos
    elif animation is SBLADE_CHARGED_SPELL2_LIST:
        end_pos = sblade_end_pos_channeled_spell

    if actor.is_moving and actor.is_moving_forward:
        sblade_rect.x -= movement_speed
        if sblade_rect.x < end_pos:
            actor.is_moving = False

    if sblade_rect.x < end_pos:
        if animation is SBLADE_CHARGED_ATTACK2_LIST or (animation is SBLADE_CHARGED_SPELL2_LIST and not target.is_interrupting):
            if animation is SBLADE_CHARGED_SPELL2_LIST:
                main.fire_sound.play()
            channeled_attack_animation(actor, target, animation)
        elif animation is SBLADE_CHARGED_SPELL2_LIST and target.is_interrupting:
            actor.status_message = f"{actor.name}'s spell is interrupted by {target.name}"
            target.is_interrupting = False
            actor.is_moving = True
            actor.is_moving_forward = False

    if actor.is_moving and not actor.is_moving_forward and sblade_rect.x < sblade_start_pos:
        sblade_rect.x += movement_speed
        if sblade_rect.x >= sblade_start_pos:
            actor.is_moving = False
            virtual_keypress = False
            keys_locked = False
            actor.turn_count += 1
            sblade.is_preparing_attack = False
            sblade.is_preparing_spell = False
            action_generated = False
            player_turn = not player_turn


def fireball_explosion():
    global spell_anim_index
    global spell_explosion_playing
    if spell_explosion_playing:
        if spell_anim_index >= len(SBLADE_MAGIC_MISSLE2_LIST):
            spell_anim_index = 0
            spell_explosion_playing = False
        else:
            WIN.blit(SBLADE_MAGIC_MISSLE2_LIST[spell_anim_index], (350, sblade_spell_rect.y))
            if frame_count % 8 == 0:
                spell_anim_index += 1


def combat():
    global spell_explosion_playing
    global spell_anim_index
    global player_turn
    global action_generated
    global third_status_message
    global virtual_keypress
    global keys_locked
    global action
    global frame_count

    WIN.blit(BG, (0, 0))
    WIN.blit(TEXT_BG, (0, HEIGHT*0.8))
    WIN.blit(ARROW_IMAGE, (arrow_rect.x, arrow_rect.y))
    WIN.blit(TAB_IMAGE, (10, HEIGHT*0.8-TAB_IMAGE.get_height()))
    WIN.blit(TAB_IMAGE, (10, HEIGHT*0.8-TAB_IMAGE.get_height()*2))
    WIN.blit(TAB_IMAGE, (10, HEIGHT*0.8-TAB_IMAGE.get_height()*3))
    WIN.blit(TAB_IMAGE, (10, HEIGHT*0.8-TAB_IMAGE.get_height()*4))
    text_attack = TEXT_FONT.render("Attack", 1, BLACK)
    text_spell = TEXT_FONT.render("Spell", 1, BLACK)
    text_parry = TEXT_FONT.render('Parry', 1, BLACK)
    text_mind = TEXT_FONT.render('Mind Blast', 1, BLACK)
    WIN.blit(text_attack, (10+TAB_IMAGE.get_width()//2-text_attack.get_width()//2, HEIGHT*0.8-TAB_IMAGE.get_height()*3.5-text_attack.get_height()//2))
    WIN.blit(text_spell, (10+TAB_IMAGE.get_width()//2-text_spell.get_width()//2, HEIGHT*0.8-TAB_IMAGE.get_height()*2.5-text_spell.get_height()//2))
    WIN.blit(text_parry, (10+TAB_IMAGE.get_width()//2-text_parry.get_width()//2, HEIGHT*0.8-TAB_IMAGE.get_height()*1.5-text_parry.get_height()//2))
    WIN.blit(text_mind, (10+TAB_IMAGE.get_width()//2-text_mind.get_width()//2, HEIGHT*0.8-TAB_IMAGE.get_height()//2-text_mind.get_height()//2))
    healthbars()
    lavender_idle_animations()
    sblade_idle_animations()
    fireball_explosion()
    status_messages()

    keys_pressed = pygame.key.get_pressed()

    if not player_turn and not lavender.is_dead and not sblade.is_dead:
        if sblade.hp < sblade.hp_max*0.3:
            if not action_generated:
                action = random.randint(1, 2)
                action_generated = True
            if action == 1:
                sblade.idle_index = 0
                sblade.is_interrupting = False
                sblade.is_preparing_attack = False
                sblade.is_preparing_spell = False
                sblade.is_idle = True
                third_status_message = f"{sblade.name} looks scared and is taking a defensive posture."
                sblade.is_parrying = True
                player_turn = not player_turn
            elif action == 2:
                sblade.idle_index = 0
                sblade.is_parrying = False
                sblade.is_preparing_attack = False
                sblade.is_preparing_spell = False
                sblade.is_idle = True
                third_status_message = f"{sblade.name} looks scared and is preparing a counterspell"
                sblade.is_interrupting = True
                player_turn = not player_turn
        else:
            if sblade.is_preparing_attack:
                if not virtual_keypress:
                    # enemy uses the same attack functions as the player and they rely on variables being set to certain
                    # values by the player pressing Enter so there's a virtual keypress for the enemy
                    keys_locked = True
                    sblade.is_moving = True
                    sblade.is_moving_forward = True
                    virtual_keypress = True
                channeled_attack(sblade, lavender, SBLADE_CHARGED_ATTACK2_LIST)
            elif sblade.is_preparing_spell:
                if not virtual_keypress:
                    keys_locked = True
                    sblade.is_moving = True
                    sblade.is_moving_forward = True
                    virtual_keypress = True
                channeled_attack(sblade, lavender, SBLADE_CHARGED_SPELL2_LIST)
            else:
                if not action_generated:
                    action = random.randint(1, 4)
                    action_generated = True
                if action == 1:
                    if not virtual_keypress:
                        keys_locked = True
                        sblade.is_parrying = False
                        sblade.is_interrupting = False
                        sblade.is_moving = True
                        sblade.is_moving_forward = True
                        virtual_keypress = True
                    attack(sblade, lavender, SBLADE_ATTACK_LIST)
                elif action == 2:
                    if not virtual_keypress:
                        keys_locked = True
                        sblade.is_parrying = False
                        sblade.is_interrupting = False
                        sblade.is_casting = True
                        virtual_keypress = True
                    spell(sblade, lavender)
                elif action == 3:
                    sblade.idle_index = 0
                    sblade.is_interrupting = False
                    sblade.is_parrying = False
                    sblade.is_preparing_attack = True
                    sblade.status_message = f"{sblade.name} is looking for an opening."
                    player_turn = not player_turn
                elif action == 4:
                    sblade.idle_index = 0
                    sblade.is_parrying = False
                    sblade.is_interrupting = False
                    sblade.is_preparing_spell = True
                    sblade.status_message = f"{sblade.name} is looking focused."
                    player_turn = not player_turn

    elif player_turn and not lavender.is_dead and not sblade.is_dead:
        if not keys_locked:
            arrow_movement(keys_pressed, arrow_rect)
        if arrow_rect.y == pos1[1]:
            if keys_pressed[pygame.K_RETURN] and not keys_locked:
                main.confirm_sound.play()
                keys_locked = True
                lavender.is_parrying = False
                lavender.is_interrupting = False
                lavender.is_moving = True
                lavender.is_moving_forward = True
            attack(lavender, sblade, LAVENDER_ATTACK_LIST)
        if arrow_rect.y == pos2[1]:
            if keys_pressed[pygame.K_RETURN] and not keys_locked:
                main.confirm_sound.play()
                keys_locked = True
                lavender.is_parrying = False
                lavender.is_interrupting = False
                lavender.is_casting = True
            spell(lavender, sblade)
        if arrow_rect.y == pos3[1]:
            if keys_pressed[pygame.K_RETURN] and not keys_locked:
                main.confirm_sound.play()
                lavender.is_parrying = True
                lavender.is_interrupting = False
                lavender.status_message = "Lavender is preparing to parry."
                action_generated = False
                virtual_keypress = False
                player_turn = not player_turn
        if arrow_rect.y == pos4[1]:
            if keys_pressed[pygame.K_RETURN] and not keys_locked:
                main.confirm_sound.play()
                lavender.is_interrupting = True
                lavender.is_parrying = False
                lavender.status_message = "Lavender is preparing to interrupt a spell."
                action_generated = False
                virtual_keypress = False
                player_turn = not player_turn

    if lavender.is_dead:
        WIN.blit(main.BG_KILLED, (0, 0))
        main.blit_small_text(keys_pressed,"You'd hear the spellblade laugh maniacally but that's kinda hard to do when you're dead.")
        if keys_pressed[pygame.K_SPACE]:
            quit()
    if sblade.is_dead:
        main.blit_text(keys_pressed, text.end(), (0, 0))
        if keys_pressed[pygame.K_SPACE]:
            quit()

    if frame_count >= 10000:
        frame_count = 0
    frame_count += 1