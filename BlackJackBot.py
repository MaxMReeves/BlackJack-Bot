import pytesseract
import pyautogui
from PIL import Image
import time

# Define coordinates for game actions
play_button_coords = (962, 688)
hit_button_coords = (830, 608)
stand_button_coords = (973, 604)
two_x_bet_button_coords = (960, 632)
textbox_coords = (932, 586)
insurance_no_coords = (997, 647)  # "No" button for insurance

# Define the coordinates for the card regions
enemy_coords = (790, 285, 150, 60)
your_coords = (790, 740, 150, 60)

# Function to extract card number from image
def extract_card_number(image):
    image = image.convert('L')  # Convert the image to grayscale for better OCR results
    card_text = pytesseract.image_to_string(image, config='--psm 6')
    card_text = ''.join([char for char in card_text if char.isdigit() or char == ','])  # Keep digits and commas
    print(f"Extracted card text: {card_text}")
    return card_text

# Function to capture the region, preprocess the image, and get text using OCR
def get_card_numbers_from_region(coords):
    screenshot = pyautogui.screenshot(region=coords)
    card_text = extract_card_number(screenshot)
    try:
        card_number = int(card_text.replace(',', ''))  # Convert to integer after removing commas
    except ValueError:
        card_number = None
    return card_number

# Function to reset the bet to 1
def reset_bet():
    pyautogui.click(textbox_coords)
    time.sleep(2)
    pyautogui.typewrite("1")
    print("Bet reset to 1.")

# Function to double the bet
def double_bet():
    pyautogui.click(two_x_bet_button_coords)
    print("Bet doubled.")

# Function to decide whether to hit or stand
def make_decision(player_number):
    if player_number >= 21:
        print("Player's number is 21 or greater, stopping hits.")
        return "stand"
    if player_number < 17:
        return "hit"
    return "stand"

# Function to handle insurance prompt
def handle_insurance(enemy_number):
    if enemy_number in [1, 11]:  # Ace is represented as 1 or 11
        print("Insurance prompt detected. Clicking 'No'.")
        pyautogui.click(insurance_no_coords)
        time.sleep(2)

# Main game loop
for game in range(100):  # Play 20 games
    print(f"Game {game + 1} started.")
    pyautogui.click(play_button_coords)  # Start the game
    print("Clicked Play button.")
    time.sleep(3)

    # Capture the enemy's and player's numbers
    enemy_number = get_card_numbers_from_region(enemy_coords)
    handle_insurance(enemy_number)
    your_number = get_card_numbers_from_region(your_coords)

    if enemy_number is None or your_number is None:
        print("Failed to detect numbers, defaulting to Stand.")
        pyautogui.click(stand_button_coords)
        time.sleep(3)
        continue

    print(f"Enemy's number: {enemy_number}, Your number: {your_number}")

    # Start betting logic
    while your_number is not None and your_number < 21:
        decision = make_decision(your_number)
        if decision == "hit":
            pyautogui.click(hit_button_coords)
            print("Clicked Hit button.")
            time.sleep(3)
            your_number = get_card_numbers_from_region(your_coords)
            print(f"New Your number: {your_number}")
        elif decision == "stand":
            pyautogui.click(stand_button_coords)
            print("Clicked Stand button.")
            break

    # Handle bust or invalid hand
    if your_number is None or your_number > 21:
        print("Standing due to invalid or bust hand.")
        pyautogui.click(stand_button_coords)
        time.sleep(3)

    # Determine the result
    print("Waiting for the dealer to complete their turn...")
    time.sleep(5)  # Wait for the dealer's turn to finish

    enemy_number = get_card_numbers_from_region(enemy_coords)
    print(f"Dealer's final number: {enemy_number}")

    if enemy_number is None:
        print("Unable to determine enemy's final number.")
    elif your_number > 21:
        print("You busted. Loss.")
        double_bet()  # Double the bet on loss
    elif enemy_number > 21 or your_number > enemy_number:
        print("You won!")
        reset_bet()  # Reset the bet on win
    elif your_number == enemy_number:
        print("It's a tie!")
    else:
        print("You lost!")
        double_bet()  # Double the bet on loss

    print(f"End of Game {game + 1}.")
    time.sleep(3)  # Pause before the next game
