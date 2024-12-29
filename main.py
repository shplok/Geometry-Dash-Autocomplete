import pyautogui
import time
import cv2
import numpy as np
import mss

def capture_screen(region=None):
    with mss.mss() as sct:
        screenshot = sct.grab(region or sct.monitors[1])
        img = np.array(screenshot)
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

def locate_image_on_screen(template_path, region=None, threshold=0.8):
    """Locate an image on the screen."""
    screen = capture_screen(region)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        return max_loc  # Return top-left corner of the match
    return None

def click_position(x, y):
    """Move the mouse to a position and click."""
    pyautogui.moveTo(x, y, duration=0.2)
    pyautogui.click()

def search_for_auto_levels():
    """Navigate to the search menu and search for 'auto' levels."""
    print("Navigating to the search menu...")
    # Adjust coordinates based on your screen/game setup
    click_position(100, 200)  # Example: Click the search menu button
    time.sleep(1)


    print("Pressing search...")
    click_position(150, 300)  # Example: Click the search button
    time.sleep(2)

def check_and_download_level(download_icon_path, play_button_path):
    """Check if the level is downloaded and download if necessary."""
    download_icon_pos = locate_image_on_screen(download_icon_path)
    if download_icon_pos:
        print("Level not downloaded. Downloading now...")
        click_position(download_icon_pos[0], download_icon_pos[1])
        time.sleep(2)
        
        # Locate and click the play button
        play_button_pos = locate_image_on_screen(play_button_path)
        if play_button_pos:
            print("Starting the level...")
            click_position(play_button_pos[0], play_button_pos[1])
            time.sleep(2)
    else:
        print("Level already downloaded. Skipping...")

def main():
    print("Starting the Geometry Dash bot...")
    time.sleep(3)  # Allow time to switch to the game

    search_for_auto_levels()

    # Paths to template images for detection
    download_icon_path = "images/download_icon.png"
    play_button_path = "images/play_button.png"

    while True:
        check_and_download_level(download_icon_path, play_button_path)
        # Implement logic to move to the next level in the list
        print("Moving to the next level...")
        click_position(500, 600)  # Example: Click the next level button
        time.sleep(2)

if __name__ == "__main__":
    main()
