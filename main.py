import pyautogui
import time
import cv2
import numpy as np
import mss
import os

# Get the absolute path of the images relative to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
download_icon_path = os.path.join(script_dir, "get_button.png")
play_button_path = os.path.join(script_dir, "view_button.png")

# get the current screen dimensions
def get_screen_size():
    screen_width, screen_height = pyautogui.size()
    return screen_width, screen_height

# convert normalized coordinates to absolute screen coordinates
def normalize_coordinates(normalized_x, normalized_y):
    screen_width, screen_height = get_screen_size()
    x = int(normalized_x * screen_width)
    y = int(normalized_y * screen_height)
    return x, y

# click at a position defined by normalized coordinates
def click_normalized(normalized_x, normalized_y):
    x, y = normalize_coordinates(normalized_x, normalized_y)
    pyautogui.moveTo(x, y, duration=0.2)
    pyautogui.click()

# capture a screenshot of the screen or a region
def capture_screen(region=None):
    with mss.mss() as sct:
        screenshot = sct.grab(region or sct.monitors[1])
        img = np.array(screenshot)
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

# locate an image on the screen
def locate_image_on_screen(template_path, region=None, threshold=0.8):
    screen = capture_screen(region)
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)

    # Match templates using color
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        return max_loc  # return top-left corner of the match
    return None

# navigate to the search menu and search for 'auto' levels
def search_for_auto_levels():
    print("navigating to the search menu from the main menu...")
    click_normalized(0.7, 0.5)  # adjust based on game ui
    time.sleep(0.2)
    print("configuring search...")
    click_normalized(0.85, 0.75)  # adjust based on game ui
    time.sleep(0.2)
    click_normalized(0.25, 0.75)
    click_normalized(0.85, 0.75)
    time.sleep(0.2)
    print("pressing search...")
    click_normalized(0.66, 0.1)


# check if the level is downloaded and download if necessary
def check_and_download_level(download_icon_path, play_button_path):
    print("checking for the download icon...")
    download_icon_pos = locate_image_on_screen(download_icon_path)
    if download_icon_pos:
        print("level not downloaded. downloading now...")
        pyautogui.moveTo(download_icon_pos[0], download_icon_pos[1], duration=0.2)
        pyautogui.click()
        time.sleep(2)

        print("checking for the play button...")
        play_button_pos = locate_image_on_screen(play_button_path)
        if play_button_pos:
            print("starting the level...")
            pyautogui.moveTo(play_button_pos[0], play_button_pos[1], duration=0.2)
            pyautogui.click()
            time.sleep(2)
        else:
            print("play button not found")
    else:
        print("level already downloaded. skipping")


# main function to run the bot
def main():
    print("starting the geometry dash bot...")
    time.sleep(3)  # allow time to switch to the game

    search_for_auto_levels()


    while True:
        check_and_download_level(download_icon_path, play_button_path)

        print("scrolling down...")
        for i in range(7):
            pyautogui.scroll(-1)  # adjust normalized coordinates for the "next level" button
        time.sleep(2)

if __name__ == "__main__":
    main()
