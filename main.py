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

# Get the current screen dimensions
def get_screen_size():
    screen_width, screen_height = pyautogui.size()
    return screen_width, screen_height

# Convert normalized coordinates to absolute screen coordinates
def normalize_coordinates(normalized_x, normalized_y):
    screen_width, screen_height = get_screen_size()
    x = int(normalized_x * screen_width)
    y = int(normalized_y * screen_height)
    return x, y

# Capture a screenshot of the screen or a region
def capture_screen(region=None):
    with mss.mss() as sct:
        screenshot = sct.grab(region or sct.monitors[1])
        img = np.array(screenshot)
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

# Load the image and check if it's loaded correctly
def load_image(path):
    template = cv2.imread(path, cv2.IMREAD_COLOR)
    if template is None:
        print(f"Error: Unable to load image {path}")
        return None
    return template

# Locate an image on the screen with normalized region support
def locate_image_on_screen(template_path, region=None, threshold=0.8):
    template = load_image(template_path)
    if template is None:
        return None


    if region:
        region = (
            normalize_coordinates(region[0], region[1])[0],
            normalize_coordinates(region[0], region[1])[1],
            normalize_coordinates(region[2], region[3])[0],
            normalize_coordinates(region[2], region[3])[1]
        )

    # Capture the screenshot
    screen = capture_screen(region)
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        print(f"Found {template_path} at {max_loc} with confidence {max_val}")
        return max_loc  # Return top-left corner of the match
    else:
        print(f"{template_path} not found")
    return None

# Click at a position defined by normalized coordinates
def click_normalized(normalized_x, normalized_y):
    x, y = normalize_coordinates(normalized_x, normalized_y)
    pyautogui.moveTo(x, y, duration=0.2)
    pyautogui.click()

# Navigate to the search menu and search for 'auto' levels
def search_for_auto_levels():
    print("Navigating to the search menu from the main menu...")
    click_normalized(0.7, 0.5)  # adjust based on game UI
    time.sleep(0.2)
    print("Configuring search...")
    click_normalized(0.85, 0.75)  # adjust based on game UI
    time.sleep(0.2)
    click_normalized(0.25, 0.75)
    click_normalized(0.85, 0.75)
    time.sleep(0.2)
    print("Pressing search...")
    click_normalized(0.66, 0.1)

# Check if the level is downloaded and download if necessary
def check_and_download_level(download_icon_path, play_button_path):
    print("Checking for the download icon...")
    right_third_region = (0.66, 0.0, 1.0, 1.0)  # The right third of the screen
    download_icon_pos = locate_image_on_screen(download_icon_path, region=right_third_region)
    if download_icon_pos:
        print("Level not downloaded. Downloading now...")
        pyautogui.moveTo(download_icon_pos[0], download_icon_pos[1], duration=0.2)
        pyautogui.click()
        time.sleep(2)

        print("Checking for the play button...")
        play_button_pos = locate_image_on_screen(play_button_path, region=right_third_region)
        if play_button_pos:
            print("Starting the level...")
            pyautogui.moveTo(play_button_pos[0], play_button_pos[1], duration=0.2)
            pyautogui.click()
            time.sleep(2)
        else:
            print("Play button not found")
    else:
        print("Level already downloaded. Skipping")

# Main function to run the bot
def main():
    print("Starting bot...")
    time.sleep(3)  # Allow time to switch to the game

    search_for_auto_levels()

    while True:
        check_and_download_level(download_icon_path, play_button_path)

        print("Scrolling down...")
        for _ in range(7):
            pyautogui.scroll(-300) 
        time.sleep(2)

if __name__ == "__main__":
    main()
