import json
import os
import pygame
import random

pygame.init()

# This is to set the dimensions for the video game to keep consistency throughout the code.
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
LANE_WIDTH = SCREEN_WIDTH // 5
LANE_POSITIONS = [(SCREEN_WIDTH // 5) * i + (SCREEN_WIDTH // 10) for i in range(5)]
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 50, 50
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 80
AMMO_WIDTH, AMMO_HEIGHT = 30, 30
BULLET_WIDTH, BULLET_HEIGHT = 10, 20
COIN_WIDTH, COIN_HEIGHT = 360, 30


def load_image(path, width=None, height=None):
    # This function was created to load the images to get rid of repetitive code for loading images
    image = pygame.image.load(path)
    if width and height:
        image = pygame.transform.scale(image, (width, height))
    return image


def play_music(music_path):
    # This function was created to play the music for when the game is running
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(loops=-1)


def stop_music():
    # This function was created to stop playing the music
    pygame.mixer.music.stop()


# These are the font styles that were used to give the future retro vibes.
# This is where it was created, so it can be called later on in the code by the variable name.
TITLE_FONT_STYLE = pygame.font.Font("fonts/Retro_font_One.otf", 50)
SUBTITLE_FONT_STYLE = pygame.font.Font("fonts/Retro_font_Two.otf", 24)
GAME_OVER_FONT_STYLE = pygame.font.Font("fonts/Retro_font_Two.otf", 100)
NAV_BUTTON_FONT_STYLE = pygame.font.Font("fonts/Retro_font_Three.otf", 35)
TEXT_SCORE_FONT_STYLE = pygame.font.Font("fonts/Retro_font_Two.otf", 20)
HEADING_ONE_FONT_STYLE = pygame.font.Font("fonts/Retro_font_Four.otf", 15)
STORY_FONT_STYLE = pygame.font.Font("fonts/Retro_font_Five.otf", 15)
ITEM_BUTTON_FONT_STYLE = pygame.font.Font("fonts/Retro_font_Six.otf", 12)
ITEM_NAME_FONT_STYLE = pygame.font.Font("fonts/Retro_font_Six.otf", 18)

# These are the images that are loaded using the load_image function and the certain requirements.
# It can be loaded here, so it can be called by the variable name in the code.
gameplay_background_image = load_image('images/Background_1.png', SCREEN_WIDTH, SCREEN_HEIGHT)
home_background_image = load_image('images/Background_2.png', SCREEN_WIDTH, SCREEN_HEIGHT)
left_arrow_image = load_image('images/Left_Arrow.png', 50, 50)
right_arrow_image = load_image('images/Right_Arrow.png', 50, 50)
space_bar_image = load_image('images/Space_Bar.png', 50, 50)
story_raccoon_image = load_image('images/Story_Raccoon.png', 300, 300)
obstacle_one_image = load_image('images/Obstacle_1.png', OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
obstacle_two_image = load_image('images/Obstacle_2.png', OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
obstacle_three_image = load_image('images/Obstacle_3.png', OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
obstacle_four_image = load_image('images/Obstacle_4.png', OBSTACLE_WIDTH, OBSTACLE_HEIGHT)

# This is where the sound effects and music is loaded. The sound effects uses mixer sound while the music is only
# loaded from the file location as it is going to be used on a constant loop of playing the music.
laser_sound = pygame.mixer.Sound('sounds/Laser_shoot_sound.wav')
explosion_sound = pygame.mixer.Sound('sounds/Explosion_sound.wav')
coin_sound = pygame.mixer.Sound('sounds/Coin_pickup_sound.wav')
ammo_sound = pygame.mixer.Sound('sounds/Ammo_pickup_sound.flac')
GAME_OVER_MUSIC = 'sounds/Gameover_page_background.mp3'
HOME_PAGE_MUSIC = 'sounds/Home_page_background.mp3'
GAME_PLAY_MUSIC = 'sounds/Gameplay_page_background.mp3'

# This is where the difficulty for the game is set incase the player wants a bit more of a challenge. It is where the
# amount of ammo you start with and the speed of the game.
DIFFICULTY_LEVELS = ['Easy', 'Medium', 'Hard', 'Expert']
CURRENT_DIFFICULTY = 0
DIFFICULTY_SETTINGS = {
    "Easy": {"ammo": 3, "obstacle_speed": 2},
    "Medium": {"ammo": 2, "obstacle_speed": 4},
    "Hard": {"ammo": 1, "obstacle_speed": 6},
    "Expert": {"ammo": 0, "obstacle_speed": 8}
}

# This is to load the high score file, so it can be displayed on the home page to see the highest score currently.
HIGHEST_SCORE_FILE = 'highest_score.txt'

# This is to set the screen and title caption of the screen for the video game.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Raccoon Madness")


def load_skins():
    # This function is used to load the skins. It is used for the item shop incase the user wants to purchase a skin and
    # equip it. It will remember which one is currently purchased or which is equipped.
    try:
        # it will try open the file if it exists. It will then load all the data inside the file.
        with open('game_data.json', 'r') as f:
            data = json.load(f)
            return data["skins"], data["ammo_colours"], data["player_coins"]
    except FileNotFoundError:
        # If the file was not found, or it was deleted, it will create another one with it being set to the default.
        raccoon_skins = [
            {"name": "Nymphia", "image_path": 'images/Raccoon_1.png', "equipped": True, "purchased": True, "price": 0},
            {"name": "Bianca", "image_path": 'images/Raccoon_2.png', "equipped": False, "purchased": False, "price": 50},
            {"name": "Dawn", "image_path": 'images/Raccoon_3.png', "equipped": False, "purchased": False, "price": 100},
            {"name": "Amanda", "image_path": 'images/Raccoon_4.png', "equipped": False, "purchased": False, "price": 150},
            {"name": "Willow", "image_path": 'images/Raccoon_5.png', "equipped": False, "purchased": False, "price": 200},
            {"name": "Trixie", "image_path": 'images/Raccoon_6.png', "equipped": False, "purchased": False, "price": 250},
        ]
        ammo_colours = [
            {"name": "Pink", "image_path": 'images/Ammo_1.png', "color": (222, 57, 232), "equipped": True, "purchased": True, "price": 0},
            {"name": "Red", "image_path": 'images/Ammo_2.png', "color": (241, 36, 14), "equipped": False, "purchased": False, "price": 25},
            {"name": "Blue", "image_path": 'images/Ammo_3.png', "color": (24, 203, 231), "equipped": False, "purchased": False, "price": 50},
            {"name": "Orange", "image_path": 'images/Ammo_4.png', "color": (255, 127, 0), "equipped": False, "purchased": False, "price": 75},
            {"name": "Yellow", "image_path": 'images/Ammo_5.png', "color": (227, 243, 19), "equipped": False, "purchased": False, "price": 100},
            {"name": "Green", "image_path": 'images/Ammo_6.png', "color": (20, 235, 86), "equipped": False, "purchased": False, "price": 125},
        ]
        default_player_coins = 0
        # After setting the default amounts and variables, it will create the new JSON file for the user.
        with open('game_data.json', 'w') as f:
            json.dump({
                "skins": raccoon_skins,
                "ammo_colours": ammo_colours,
                "player_coins": default_player_coins
            }, f, indent=4)
        return raccoon_skins, ammo_colours, default_player_coins


def load_highest_score():
    # This is to load the highest score in the file. If the file does not exist, it will set the value to zero.
    # The file will get created when the user plays and will create one when there is a highscore to be saved.
    if os.path.exists(HIGHEST_SCORE_FILE):
        with open(HIGHEST_SCORE_FILE, "r") as file:
            try:
                return int(file.read().strip())
            except ValueError:
                return 0
    return 0


def save_skins(skin, ammo_colour, player_coin):
    # This is used to save the changes made in the item shop. If the user purchased a new skin, it will update here.
    # If the user selected a skin to equip, it will be loaded and saved here to make sure these changes are saved.
    with open('game_data.json', 'w') as f:
        data = {
            "skins": skin,
            "ammo_colours": ammo_colour,
            "player_coins": player_coin
        }
        json.dump(data, f, indent=4)


def save_highest_score(highest_score):
    # This is to create the high score in the text file. This function is only called when the high score is higher in
    # the text file.
    with open(HIGHEST_SCORE_FILE, "w") as file:
        file.write(str(highest_score))


skins, ammo_colors, player_coins = load_skins()


class Player:
    def __init__(self):
        # This is to initialize the player for position and size on the screen.
        # It sets the starting position to the middle lane and to the bottom of the screen.
        self.rect = pygame.Rect(LANE_POSITIONS[2], SCREEN_HEIGHT - PLAYER_HEIGHT - 20, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.current_lane = 2
        self.ammo = 0
        self.collected_coins = 0

    def move_left(self):
        # This is to move the player one lane to the left if they are not already in the leftmost lane.
        if self.current_lane > 1:
            self.current_lane -= 1
            self.rect.x = LANE_POSITIONS[self.current_lane]

    def move_right(self):
        # This is to move the player one lane to the right if they are not already in the rightmost lane.
        if self.current_lane < 3:
            self.current_lane += 1
            self.rect.x = LANE_POSITIONS[self.current_lane]

    def collect_ammo(self):
        # This is when ammo is collected it will play the sound effect and increase the player's ammo count by one.
        ammo_sound.play()
        self.ammo += 1

    def collect_coin(self):
        # This is when coins are collected it will play the sound effect and increase the player's collected coins by one.
        coin_sound.play()
        self.collected_coins += 1
        self.save_total_coins()

    def save_total_coins(self):
        # This is to save the total number of coins collected to the JSON file for persistence.
        try:
            with open('game_data.json', 'r') as f:
                data = json.load(f)
            # Update the total coin count with the newly collected coins.
            data["player_coins"] += self.collected_coins
            self.collected_coins = 0  # Reset the temporary coin count after saving.
            # Write the updated data back to the JSON file.
            with open('game_data.json', 'w') as f:
                json.dump(data, f, indent=4)
        except FileNotFoundError:
            # This is to call the initial file if the file does not exist.
            load_skins()


class Coin:
    def __init__(self, lane):
        # This is to initialize the coin's animation frames, position, and movement speed.
        self.frames = None
        self.lane = lane
        self.rect = pygame.Rect(LANE_POSITIONS[lane], -COIN_HEIGHT, COIN_WIDTH, COIN_HEIGHT)
        self.speed = 5
        self.load_frames()
        self.current_frame = 0
        self.frame_delay = 5  # Number of update cycles between each frame switch.
        self.frame_counter = 0  # Counter to keep track of the delay between frame changes.

    def load_frames(self):
        # This is to load the coin sprite sheet and scale it to the desired size of the coin width and height.
        sprite_sheet = pygame.image.load("images/Coin_Sprite.png").convert_alpha()
        sprite_sheet = pygame.transform.scale(sprite_sheet, (COIN_WIDTH, COIN_HEIGHT))
        # This is to calculate the width of each individual frame in the sprite sheet. There are 12 images in the coin
        # sprite sheet.
        frame_width = COIN_WIDTH // 12
        # This is to extract each frame from the sprite sheet and store it in the frames list.
        self.frames = [
            sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, COIN_HEIGHT))
            for i in range(12)
        ]

    def update(self):
        # This is to update the coin's position by moving it down the screen.
        self.rect.y += self.speed
        # Increment the frame counter, and switch to the next frame if the delay has passed.
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0  # Reset the frame counter.
            # This will move to the next frame, looping back to the first frame if at the end.
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def is_off_screen(self):
        # This is to check if the coin has moved below the bottom of the screen.
        return self.rect.y > SCREEN_HEIGHT

    def draw(self, game_screen):
        # This is to draw the current frame of the coin at its current position on the screen.
        game_screen.blit(self.frames[self.current_frame], self.rect.topleft)


class Obstacle:
    def __init__(self, lane):
        # This is to initialize the obstacle's position, image, and speed.
        self.lane = lane
        self.rect = pygame.Rect(LANE_POSITIONS[lane], -OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
        self.image = random.choice([obstacle_one_image, obstacle_two_image, obstacle_three_image, obstacle_four_image])
        self.speed = 0

    def update(self):
        # This is to update the obstacle's position by moving it down the screen based on its speed.
        self.rect.y += self.speed

    def is_off_screen(self):
        # This is to check if the obstacle has moved below the bottom of the screen.
        return self.rect.y > SCREEN_HEIGHT

    def draw(self, game_screen):
        # This is to draw the obstacle's image at its current position on the screen.
        game_screen.blit(self.image, self.rect.topleft)


class AmmoPickup:
    def __init__(self, lane):
        # This is to initialize the ammo pickup's lane, position, and speed.
        self.lane = lane
        self.rect = pygame.Rect(LANE_POSITIONS[lane], -AMMO_HEIGHT, AMMO_WIDTH, AMMO_HEIGHT)
        self.speed = 0

    def update(self):
        # This is to update the ammo pickup's position by moving it down the screen based on its speed.
        self.rect.y += self.speed

    def is_off_screen(self):
        # This is to check if the ammo pickup has moved below the bottom of the screen.
        return self.rect.y > SCREEN_HEIGHT

    def draw(self, game_screen):
        # This will draw the equipped ammo image at the ammo pickup's current position on the screen.
        for ammo in ammo_colors:
            if ammo["equipped"]:
                # This will load the equipped ammo image and resize it to fit the ammo pickup dimensions.
                equipped_image = pygame.image.load(ammo["image_path"])
                equipped_image = pygame.transform.scale(equipped_image, (AMMO_WIDTH, AMMO_HEIGHT))
                # This will display the equipped ammo image at the ammo pickup's position.
                game_screen.blit(equipped_image, self.rect.topleft)
                break


class Bullet:
    def __init__(self, x, y):
        # This is to initialize two beams for the bullet: one on the left and one on the right.
        # The x and y parameters determine the starting position of the bullet beams.
        self.left_beam = pygame.Rect(x - 15, y, 2, 20)
        self.right_beam = pygame.Rect(x + 15, y, 2, 20)
        self.speed = 10

    def update(self):
        # This will update the position of both beams by moving them upward based on the bullet's speed.
        self.left_beam.y -= self.speed
        self.right_beam.y -= self.speed

    def is_off_screen(self):
        # This will check if both beams have moved off the top of the screen.
        return self.left_beam.y < 0 and self.right_beam.y < 0

    def draw(self, game_screen):
        # This will draw each beam in the color of the currently equipped ammo.
        for ammo in ammo_colors:
            if ammo["equipped"]:
                # This will get the color of the equipped ammo and draw both beams with that color.
                ammo_color = ammo["color"]
                pygame.draw.rect(game_screen, ammo_color, self.left_beam)
                pygame.draw.rect(game_screen, ammo_color, self.right_beam)
                break


class Explosion:
    def __init__(self, x, y):
        # This is to initialize the explosion with position, frames for animation, and active status.
        self.frames = []
        self.load_frames()
        self.current_frame = 0
        self.rect = pygame.Rect(x, y, 50, 50)
        self.active = True

    def load_frames(self):
        # This is to load the explosion frames from the sprite sheet.
        sprite_sheet = pygame.image.load("images/Explosion_Sprite.png").convert_alpha()
        sheet_width, sheet_height = sprite_sheet.get_size()

        # This will calculate the dimensions of each frame.
        frame_width = sheet_width // 7  # 7 columns in the sprite sheet.
        frame_height = sheet_height // 2  # 2 rows in the sprite sheet.

        # This will then loop through the rows and the columns to extract each frame from the sprite sheet.
        for row in range(2):
            for col in range(7):
                frame = sprite_sheet.subsurface(
                    pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
                )
                self.frames.append(frame)  # Add each frame to the frames list.

    def update(self):
        # This will then update the current frame of the explosion.
        if self.current_frame < len(self.frames) - 1:
            # It will move to the next frame if not at the end of the animation.
            self.current_frame += 1
        else:
            # If the last frame has been displayed, deactivate the explosion.
            self.active = False

    def draw(self, game_screen):
        # This will draw the current frame of the explosion if it is active.
        if self.active:
            game_screen.blit(self.frames[self.current_frame], self.rect.topleft)


def draw_button(text, rect):
    # This is to create the buttons and give it the hover effect when the mouse interacts with the button.
    button_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        button_color = (150, 150, 150, 255)
    else:
        button_color = (0, 0, 0, 128)
    button_surface.fill(button_color)
    screen.blit(button_surface, rect.topleft)
    text_surface = NAV_BUTTON_FONT_STYLE.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def render_controls(image, description, action, y_offset):
    # This function is used to render and set the items in the control page. It is used to get rid of repetitive code
    screen.blit(image, (30, y_offset + 10))
    description_text = HEADING_ONE_FONT_STYLE.render(description, True, (255, 255, 255))
    screen.blit(description_text, (110, y_offset + 20))
    action_text = HEADING_ONE_FONT_STYLE.render(action, True, (255, 255, 255))
    screen.blit(action_text, (340, y_offset + 20))


def home_page():
    # This is used for the home page to display the following information on the home page.
    # It then loads the file to make sure if it exists or not to avoid any crashes of no files not existing. It loads
    # the high score file as well.
    load_skins()
    highest_score = load_highest_score()
    title_text = TITLE_FONT_STYLE.render("Raccoon Madness", True, (255, 255, 255))
    screen.blit(title_text, title_text.get_rect(center=(SCREEN_WIDTH // 2, 50)))
    coin_text = TITLE_FONT_STYLE.render(f"Highest Score: {highest_score}", True, (255, 255, 255))
    screen.blit(coin_text, coin_text.get_rect(center=(SCREEN_WIDTH // 2, 120)))
    difficulty_text = DIFFICULTY_LEVELS[CURRENT_DIFFICULTY]
    # These are the buttons that are used to take the player to the following pages, and it is used to detect any clicks
    # from the mouse between those points.
    draw_button("Play", pygame.Rect(100, 300, 400, 60))
    draw_button(f"Level: {difficulty_text}", pygame.Rect(100, 380, 400, 60))
    draw_button("Shop", pygame.Rect(100, 460, 400, 60))
    draw_button("Story", pygame.Rect(100, 540, 400, 60))
    draw_button("Controls", pygame.Rect(100, 620, 400, 60))
    draw_button("Quit", pygame.Rect(100, 700, 400, 60))
    pygame.display.flip()


def store_page(skin, ammo_colour):
    # This is the store page where the items the user can purchase or equip can be seen.
    title_text = TITLE_FONT_STYLE.render(" item store ", True, (255, 255, 255))
    screen.blit(title_text, title_text.get_rect(center=(SCREEN_WIDTH // 2, 50)))
    coins_text = STORY_FONT_STYLE.render(f"Available Coins: {load_skins()[2]}", True, (255, 255, 255))
    screen.blit(coins_text, coins_text.get_rect(center=(SCREEN_WIDTH // 2, 100)))
    raccoon_text = HEADING_ONE_FONT_STYLE.render("Raccoon Skins", True, (255, 255, 255))
    screen.blit(raccoon_text, (15, 150))

    mouse_pos = pygame.mouse.get_pos()

    for i, s in enumerate(skin):
        # it uses a for loop to load all the items in the file for the skins
        skin_image = pygame.image.load(s["image_path"])
        skin_image_resized = pygame.transform.scale(skin_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        screen.blit(skin_image_resized, (25 + i * 100, 220))
        label_text = ITEM_NAME_FONT_STYLE.render(s["name"], True, (255, 255, 255))
        screen.blit(label_text, (25 + i * 100, 190))
        # Determine button text and label color
        if s["equipped"]:
            button_text = "SELECTED"
        elif s["purchased"]:
            button_text = "EQUIP"
        else:
            button_text = "PURCHASE"
        button_rect = pygame.Rect(15 + i * 100, 350, 70, 28)
        if button_rect.collidepoint(mouse_pos):
            button_color = (150, 150, 150, 255)
            button_label_color = (0, 0, 0)
        else:
            button_color = (0, 0, 0, 128)
            button_label_color = (255, 255, 255)
        pygame.draw.rect(screen, button_color, button_rect)
        button_label = ITEM_BUTTON_FONT_STYLE.render(button_text, True, button_label_color)
        label_width = button_label.get_width()
        label_height = button_label.get_height()
        label_x = button_rect.x + (button_rect.width - label_width) // 2
        label_y = button_rect.y + (button_rect.height - label_height) // 2
        screen.blit(button_label, (label_x, label_y))
        if not s["purchased"]:
            price_label = ITEM_BUTTON_FONT_STYLE.render(f"{s['price']} Coins", True, (255, 255, 255))
            screen.blit(price_label, (25 + i * 100, 320))

    ammo_text = HEADING_ONE_FONT_STYLE.render("ammo Colours", True, (255, 255, 255))
    screen.blit(ammo_text, (15, 430))
    mouse_pos = pygame.mouse.get_pos()

    for i, a in enumerate(ammo_colour):
        # This is the for loop for the ammo colours the user wants to purchase or select.
        ammo_label_text = ITEM_NAME_FONT_STYLE.render(a["name"], True, (255, 255, 255))
        screen.blit(ammo_label_text, (25 + i * 100, 480))
        ammo_image = pygame.image.load(a["image_path"])
        ammo_image_resized = pygame.transform.scale(ammo_image, (AMMO_WIDTH, AMMO_HEIGHT))
        screen.blit(ammo_image_resized, (25 + i * 100, 520))
        if not a["purchased"]:
            price_label = ITEM_BUTTON_FONT_STYLE.render(f"{a['price']} Coins", True, (255, 255, 255))
            screen.blit(price_label, (25 + i * 100, 570))
        if a["equipped"]:
            button_text = "SELECTED"
        elif a["purchased"]:
            button_text = "EQUIP"
        else:
            button_text = "PURCHASE"
        button_rect = pygame.Rect(15 + i * 100, 610, 70, 28)
        if button_rect.collidepoint(mouse_pos):
            button_color = (150, 150, 150, 255)
            button_label_color = (0, 0, 0)
        else:
            button_color = (0, 0, 0, 128)
            button_label_color = (255, 255, 255)
        pygame.draw.rect(screen, button_color, button_rect)
        button_label = ITEM_BUTTON_FONT_STYLE.render(button_text, True, button_label_color)
        label_width = button_label.get_width()
        label_height = button_label.get_height()
        label_x = button_rect.x + (button_rect.width - label_width) // 2
        label_y = button_rect.y + (button_rect.height - label_height) // 2
        screen.blit(button_label, (label_x, label_y))
    draw_button("Go Back", pygame.Rect(100, 720, 400, 50))
    pygame.display.flip()


def handle_click(raccoon_skins, ammo_color, player_coin, mouse_pos):
    # This function is used to handle the logic of checking if the item was purchased, equipped or selected. It is used
    # when the user enters the home page to display all the logic of what button should display what in the JSON file.
    for i, skin in enumerate(raccoon_skins):
        button_rect = pygame.Rect(15 + i * 100, 350, 70, 28)
        if button_rect.collidepoint(mouse_pos):
            if skin["purchased"]:
                if not skin["equipped"]:
                    for s in raccoon_skins:
                        if s["equipped"]:
                            s["equipped"] = False
                    skin["equipped"] = True
            else:
                if player_coin >= skin["price"]:
                    player_coin -= skin["price"]
                    skin["purchased"] = True

    for i, ammo in enumerate(ammo_color):
        button_rect = pygame.Rect(15 + i * 100, 610, 70, 28)
        if button_rect.collidepoint(mouse_pos):
            if ammo["purchased"]:
                if not ammo["equipped"]:
                    for a in ammo_color:
                        if a["equipped"]:
                            a["equipped"] = False
                    ammo["equipped"] = True
            else:
                if player_coin >= ammo["price"]:
                    player_coin -= ammo["price"]
                    ammo["purchased"] = True
    save_skins(raccoon_skins, ammo_color, player_coin)
    return player_coin


def story_page():
    # This page is used for giving the background of why the user is playing as a raccoon and why they have laser goggles.
    # It helps the user feel more immersed in the story of the game.
    title_text = TITLE_FONT_STYLE.render(" the raccoon story ", True, (255, 255, 255))
    screen.blit(title_text, title_text.get_rect(center=(SCREEN_WIDTH // 2, 100)))
    story_lines = [
        "In the late 3000s, Earth’s cities are ruled by robots,",
        "with no life remaining—except you, a lone raccoon",
        "scavenging for survival. While sneaking into",
        "a futuristic lab, you stumble upon laser goggles",
        "goggles and accidentally trigger the robot security.",
        "Now on the run, the goggles reveal hidden traps and",
        "allow you to outmaneuver the relentless machines.",
        "As they close in, you discover the goggles can fire",
        "lasers, and with a daring blast, you break",
        "through their defenses, racing to escape",
        "the robot-controlled metropolis."
    ]
    for i, line in enumerate(story_lines):
        story_text = STORY_FONT_STYLE.render(line, True, (255, 255, 255))
        screen.blit(story_text, story_text.get_rect(center=(SCREEN_WIDTH // 2, 170 + i * 30)))
    screen.blit(story_raccoon_image, story_raccoon_image.get_rect(center=(SCREEN_WIDTH // 2, 580)))
    draw_button("Go Back", pygame.Rect(100, 720, 400, 50))
    pygame.display.flip()


def controls_page():
    # This is the controls page where it explains the controls, objectives, and obstacles in the game to help explain
    # to the user, so they can understand the game logic.
    controls_title = SUBTITLE_FONT_STYLE.render("Controls:", True, (255, 255, 255))
    screen.blit(controls_title, (30, 15))
    render_controls(left_arrow_image, "left arrow key", "turns left", 50)
    render_controls(right_arrow_image, "right arrow key", "turns right", 105)
    render_controls(space_bar_image, "space bar key", "shoots lasers", 160)
    obstacles_title = SUBTITLE_FONT_STYLE.render("Obstacles:", True, (255, 255, 255))
    screen.blit(obstacles_title, (30, 240))
    render_controls(obstacle_one_image, "purple security bot", "destroy with laser", 275)
    render_controls(obstacle_two_image, "blue security bot", "destroy with laser", 330)
    render_controls(obstacle_three_image, "green security bot", "destroy with laser", 385)
    render_controls(obstacle_four_image, "trash can", "destroy with laser", 440)
    items_title = SUBTITLE_FONT_STYLE.render("Items:", True, (255, 255, 255))
    screen.blit(items_title, (30, 520))
    for ammo in ammo_colors:
        if ammo["equipped"]:
            equipped_image = pygame.image.load(ammo["image_path"])
            equipped_image = pygame.transform.scale(equipped_image, (AMMO_WIDTH, AMMO_HEIGHT))
            render_controls(equipped_image, "laser ammunition", "used to shoot lasers", 555)
            break
    sprite_sheet = pygame.image.load("images/Coin_Sprite.png").convert_alpha()
    sprite_sheet = pygame.transform.scale(sprite_sheet, (COIN_WIDTH, COIN_HEIGHT))
    frame_width = COIN_WIDTH // 12
    frames = [sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, COIN_HEIGHT)) for i in range(12)]
    render_controls(frames[0], "coins", "used to purchase items", 610)
    draw_button("Go Back", pygame.Rect(100, 720, 400, 50))
    pygame.display.flip()


def game_over_page():
    # This is the game over page when the user crashes or loses in the game. It will give the option of going back to the
    # home page or trying again.
    game_text = GAME_OVER_FONT_STYLE.render("GAME", True, (255, 255, 255))
    screen.blit(game_text, (140, 180))
    over_text = GAME_OVER_FONT_STYLE.render("Over", True, (255, 255, 255))
    screen.blit(over_text, (170, 280))
    draw_button("Retry", pygame.Rect(200, 400, 200, 80))
    draw_button("Home", pygame.Rect(200, 500, 200, 80))
    pygame.display.flip()


def game_loop():
    # This is the main loop function for when the game plays. it sets all the initial variables for the game and plays
    # the music of the home page since the application has just started.
    global CURRENT_DIFFICULTY, player_coins, obstacle_speed, background_speed
    clock = pygame.time.Clock()
    player = Player()
    obstacles = []
    bullets = []
    ammo_pickups = []
    explosions = []
    coins = []
    collected_coins = 0
    score = 0
    running = True
    move_delay = 0
    state = 'HOME'
    start_time = pygame.time.get_ticks()
    play_music(HOME_PAGE_MUSIC)
    background_y1 = 0
    background_y2 = -SCREEN_HEIGHT
    background_x1 = 0
    background_x2 = home_background_image.get_width()

    while running:
        # It will take the user to the home page first where they will be able to select what page they want to view.
        if state == 'HOME':
            # it calls the home page function and displays the movement of the background image.
            home_page()
            background_x1 -= 0.15
            background_x2 -= 0.15
            if background_x1 <= -home_background_image.get_width():
                background_x1 = home_background_image.get_width()
            if background_x2 <= -home_background_image.get_width():
                background_x2 = home_background_image.get_width()
            screen.blit(home_background_image, (background_x1, 0))
            screen.blit(home_background_image, (background_x2, 0))

            for event in pygame.event.get():
                # This is to listen where the mouse clicks to perform the following actions if the mouse interacts at
                # these given points.
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if pygame.Rect(100, 300, 400, 60).collidepoint(mouse_pos):
                        # This is for the playing game state when the user wants to play the game and will go to the
                        # playing state. It will then stop the home music and begin the game play music.
                        state = 'PLAYING'
                        player = Player()
                        player.ammo = DIFFICULTY_SETTINGS[DIFFICULTY_LEVELS[CURRENT_DIFFICULTY]]["ammo"]
                        obstacle_speed = DIFFICULTY_SETTINGS[DIFFICULTY_LEVELS[CURRENT_DIFFICULTY]]["obstacle_speed"]
                        background_speed = obstacle_speed
                        obstacles = []
                        bullets = []
                        ammo_pickups = []
                        explosions = []
                        score = 0
                        stop_music()
                        play_music(GAME_PLAY_MUSIC)
                    elif pygame.Rect(100, 380, 400, 60).collidepoint(mouse_pos):
                        # This is to change the difficulty of the game when the user clicks this button.
                        CURRENT_DIFFICULTY = (CURRENT_DIFFICULTY + 1) % len(DIFFICULTY_LEVELS)
                    elif pygame.Rect(100, 460, 400, 60).collidepoint(mouse_pos):
                        # This will call the store state which will be the store page
                        state = 'STORE'
                    elif pygame.Rect(100, 540, 400, 60).collidepoint(mouse_pos):
                        # This will call the story state which will be the story page
                        state = 'STORY'
                    elif pygame.Rect(100, 620, 400, 60).collidepoint(mouse_pos):
                        # This will call the controls state which will be the controls page
                        state = 'CONTROLS'
                    elif pygame.Rect(100, 700, 400, 60).collidepoint(mouse_pos):
                        # This will close the application as it is to close the game
                        running = False
        elif state == 'STORE':
            # This state is for the store. It creates the background movement for the background image
            background_x1 -= 0.15
            background_x2 -= 0.15
            if background_x1 <= -home_background_image.get_width():
                background_x1 = home_background_image.get_width()
            if background_x2 <= -home_background_image.get_width():
                background_x2 = home_background_image.get_width()
            screen.blit(home_background_image, (background_x1, 0))
            screen.blit(home_background_image, (background_x2, 0))
            rect_surface = pygame.Surface((600, 800))
            rect_surface.set_alpha(150)
            rect_surface.fill((0, 0, 0))
            screen.blit(rect_surface, (0, 0))

            # It then calls the storepage function where it will display all the information in the store based on the
            # JSON file
            store_page(skins, ammo_colors)

            for event in pygame.event.get():
                # This then listens to see which button is clicked. There is a go back button and the handle click
                # button function.
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if pygame.Rect(100, 720, 400, 50).collidepoint(mouse_pos):
                        state = 'HOME'
                    else:
                        player_coins = handle_click(skins, ammo_colors, player_coins, mouse_pos)
            pygame.display.flip()

        elif state == 'STORY':
            # This state is for the Story page. It will load the information from the story page function and have the
            # moving background image of the home background.
            story_page()
            background_x1 -= 0.15
            background_x2 -= 0.15
            if background_x1 <= -home_background_image.get_width():
                background_x1 = home_background_image.get_width()
            if background_x2 <= -home_background_image.get_width():
                background_x2 = home_background_image.get_width()
            screen.blit(home_background_image, (background_x1, 0))
            screen.blit(home_background_image, (background_x2, 0))
            rect_surface = pygame.Surface((600, 800))
            rect_surface.set_alpha(150)
            rect_surface.fill((0, 0, 0))
            screen.blit(rect_surface, (0, 0))

            for event in pygame.event.get():
                # This is to listen to the action of the mouse and see what action needs to be performed. Which will
                # be the go back button to the home page.
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if pygame.Rect(100, 720, 400, 50).collidepoint(mouse_pos):
                        state = 'HOME'

        elif state == 'CONTROLS':
            # This state is for the controls page where it displays the information from the controls page function.
            # It also loads the background movement of the home background image.
            controls_page()
            background_x1 -= 0.15
            background_x2 -= 0.15
            if background_x1 <= -home_background_image.get_width():
                background_x1 = home_background_image.get_width()
            if background_x2 <= -home_background_image.get_width():
                background_x2 = home_background_image.get_width()
            screen.blit(home_background_image, (background_x1, 0))
            screen.blit(home_background_image, (background_x2, 0))
            rect_surface = pygame.Surface((600, 800))
            rect_surface.set_alpha(150)
            rect_surface.fill((0, 0, 0))
            screen.blit(rect_surface, (0, 0))

            for event in pygame.event.get():
                # This is to listen to the mouse and see what it pushes which is the go back button which will take
                # the user back to the home page.
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if pygame.Rect(100, 720, 400, 50).collidepoint(mouse_pos):
                        state = 'HOME'

        elif state == 'PLAYING':
            # This state is for when the user is playing the video game. The background image will be changed to the
            # gameplay background where it will move in a different direction.
            screen.blit(gameplay_background_image, (0, background_y1))
            screen.blit(gameplay_background_image, (0, background_y2))
            background_y1 += background_speed
            background_y2 += background_speed
            if background_y1 >= SCREEN_HEIGHT:
                background_y1 = -SCREEN_HEIGHT
            if background_y2 >= SCREEN_HEIGHT:
                background_y2 = -SCREEN_HEIGHT
            screen.blit(gameplay_background_image, (0, background_y1))
            screen.blit(gameplay_background_image, (0, background_y2))

            current_time = pygame.time.get_ticks()
            # This is to increase the speed of the game every 10 seconds to make the game progressively more difficult.
            if (current_time - start_time) // 1000 >= 10:
                obstacle_speed += 0.25
                background_speed += 0.25
                start_time = current_time

            for event in pygame.event.get():
                # This is to listen to the key bind of the space bar being pressed. This is used to shoot the ammo of the
                # laser.
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and player.ammo > 0:
                        # It deducts the ammo amount and plays the laser sound
                        bullets.append(Bullet(player.rect.centerx, player.rect.y))
                        player.ammo -= 1
                        laser_sound.play()

            keys = pygame.key.get_pressed()
            # This is to listen to what key is pressed for the movement. The user can move left or right
            if move_delay == 0:
                if keys[pygame.K_LEFT]:
                    player.move_left()
                    move_delay = 10
                if keys[pygame.K_RIGHT]:
                    player.move_right()
                    move_delay = 10

            if move_delay > 0:
                move_delay -= 1

            if random.randint(1, 50) == 1:
                # This is to randomly generate the obstacles on the screen making it more common.
                # It will only spawn in the three lanes
                lane = random.randint(1, 3)
                safe_to_spawn = True
                for obstacle in obstacles:
                    if obstacle.lane == lane and obstacle.rect.y < OBSTACLE_HEIGHT * 2:
                        safe_to_spawn = False
                        break
                if safe_to_spawn:
                    obstacles.append(Obstacle(lane))

            if random.randint(1, 200) == 1:
                # This is to randomly generate the coins on the screen making it a bit rare.
                lane = random.randint(1, 3)
                coins.append(Coin(lane))

            if random.randint(1, 150) == 1:
                # This is to randomly generate the ammo on the screen making it slightly rare.
                possible_lanes = [1, 2, 3]
                for obstacle in obstacles:
                    if obstacle.rect.y < AMMO_HEIGHT and obstacle.rect.y + OBSTACLE_HEIGHT > -AMMO_HEIGHT:
                        if obstacle.lane in possible_lanes:
                            possible_lanes.remove(obstacle.lane)
                if possible_lanes:
                    lane = random.choice(possible_lanes)
                    ammo_pickups.append(AmmoPickup(lane))

            for bullet in bullets[:]:
                # This is to update the bullet in the Bullet Class and check if it is off-screen
                bullet.update()
                if bullet.is_off_screen():
                    bullets.remove(bullet)

            for obstacle in obstacles[:]:
                # This is to update the obstacle and speed in the Obstacle Class and check if it is off-screen and increase
                # the score
                obstacle.speed = obstacle_speed
                obstacle.update()
                if obstacle.is_off_screen():
                    obstacles.remove(obstacle)
                    score += 1

            for ammo in ammo_pickups[:]:
                # This is to update the ammo and speed in the Ammo Class and check if it is off-screen and increase the ammo
                # collection if the player collected the ammo.
                ammo.speed = obstacle_speed
                ammo.update()
                if ammo.is_off_screen():
                    ammo_pickups.remove(ammo)
                if player.rect.colliderect(ammo.rect):
                    player.collect_ammo()
                    ammo_pickups.remove(ammo)

            for coin in coins[:]:
                # This is to update the coins and speed in the Coin Class and check if it is off-screen and increase the coins
                # collected if the player collected a coin
                coin.speed = obstacle_speed
                coin.update()
                if coin.is_off_screen():
                    coins.remove(coin)
                if player.rect.colliderect(coin.rect):
                    player.collect_coin()
                    collected_coins += 1
                    coins.remove(coin)

            for explosion in explosions[:]:
                # This is to check if there was an explosion and updates it in the Explosion Class.
                explosion.update()
                if not explosion.active:
                    explosions.remove(explosion)

            for bullet in bullets[:]:
                # This is to check if the bullet collided with the object and plays the explosion sound and increases the
                # players score by 5.
                for obstacle in obstacles[:]:
                    if bullet.left_beam.colliderect(obstacle.rect) or bullet.right_beam.colliderect(obstacle.rect):
                        obstacles.remove(obstacle)
                        bullets.remove(bullet)
                        explosions.append(Explosion(obstacle.rect.x, obstacle.rect.y))
                        explosion_sound.play()
                        score += 5
                        break

            for obstacle in obstacles:
                # This is to check if the user collided in the obstacle and stops the music and calls the GAME OVER state
                # to show that the game is over.
                if player.rect.colliderect(obstacle.rect):
                    stop_music()
                    rect_surface = pygame.Surface((600, 800))
                    rect_surface.set_alpha(150)
                    rect_surface.fill((0, 0, 0))
                    screen.blit(rect_surface, (0, 0))
                    play_music(GAME_OVER_MUSIC)
                    state = 'GAME_OVER'

            for skin in skins:
                # This is to display the skin the user currently has equipped when they play the game.
                if skin["equipped"]:
                    equipped_image = pygame.image.load(skin["image_path"])
                    equipped_image = pygame.transform.scale(equipped_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
                    screen.blit(equipped_image, player.rect.topleft)
                    break

            for obstacle in obstacles:
                # This is to draw the obstacles on the screen
                obstacle.draw(screen)

            for bullet in bullets:
                # This is to draw the bullets on the screen
                bullet.draw(screen)

            for ammo in ammo_pickups:
                # This is to draw the ammo on the screen
                ammo.draw(screen)

            for coin in coins:
                # This is to draw the coins on the screen
                coin.draw(screen)

            for explosion in explosions:
                # This is to draw the explosion on the screen
                explosion.draw(screen)

            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 600, 30))
            # This is to draw the amount of ammo, the amount of score, and the amount of coins while they user is playing
            # the game so that they can keep track.
            ammo_text = TEXT_SCORE_FONT_STYLE.render(f"Ammo: {player.ammo}", True, (255, 255, 255))
            screen.blit(ammo_text, (10, 5))
            score_text = TEXT_SCORE_FONT_STYLE.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (250, 5))
            coin_text = TEXT_SCORE_FONT_STYLE.render(f"Coins: {collected_coins}", True, (255, 255, 255))
            screen.blit(coin_text, (480, 5))
            pygame.display.flip()
            clock.tick(60)

        elif state == 'GAME_OVER':
            # This is when the game over state is called and displays the game over function that will display all the information
            # inside that function.
            game_over_page()

            for event in pygame.event.get():
                # It will then listen to the option the user wants to select. They can either select the button to retry and will
                # restart the game from the beginning again. Or they can select the go back button which will take the user back to
                # the home page incase they want to go to a different page or change the difficulty.
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if pygame.Rect(200, 400, 200, 80).collidepoint(mouse_pos):
                        state = 'PLAYING'
                        total_coins = load_skins()[2]
                        total_coins += player.collected_coins
                        player.save_total_coins()
                        high_score = load_highest_score()
                        if score > high_score:
                            save_highest_score(score)
                        player = Player()
                        player.ammo = DIFFICULTY_SETTINGS[DIFFICULTY_LEVELS[CURRENT_DIFFICULTY]]["ammo"]
                        obstacle_speed = DIFFICULTY_SETTINGS[DIFFICULTY_LEVELS[CURRENT_DIFFICULTY]]["obstacle_speed"]
                        obstacles = []
                        bullets = []
                        ammo_pickups = []
                        coins = []
                        explosions = []
                        score = 0
                        play_music(GAME_PLAY_MUSIC)
                    elif pygame.Rect(200, 500, 200, 80).collidepoint(mouse_pos):
                        total_coins = load_skins()[2]
                        total_coins += player.collected_coins
                        player.save_total_coins()
                        high_score = load_highest_score()
                        if score > high_score:
                            save_highest_score(score)
                        stop_music()
                        play_music(HOME_PAGE_MUSIC)
                        state = 'HOME'
    pygame.quit()


game_loop()  # This is to call the main function of the game loop.
