import random
import firebase_admin
from firebase_admin import credentials, db
import os
import sys

# Initialize Firebase
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS  # Path PyInstaller extracts files to in EXE
else:
    base_path = os.path.dirname(__file__)

cred_path = r'C:\Users\Xiwen\Downloads\project-game-76739-firebase-adminsdk-fbsvc-cf4832ac27.json'
cred = credentials.Certificate(cred_path)

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://project-game-76739-default-rtdb.firebaseio.com/'
})

coins = 0
range1 = 1
range2 = 10
mecn = 1

# Function to upload stats automatically
def upload_stats():
    data = {
        "coins": coins,
        "mecn": mecn,
        "range1": range1,
        "range2": range2
    }
    player_ref.set(data)

# Ask for player username and handle new/existing users
while True:
    player_name = input("Enter your player name or your old username: ")
    player_ref = db.reference(f"players/{player_name}")

    existing_data = player_ref.get()

    if isinstance(existing_data, dict):
        coins = existing_data.get("coins", 0)
        mecn = existing_data.get("mecn", 1)
        range1 = existing_data.get("range1", 1)
        range2 = existing_data.get("range2", 10)
        print(f"Welcome back, {player_name}!")
        break
    elif existing_data is None:
        print(f"Welcome, {player_name}! (new player)")
        upload_stats()  # Create player in Firebase immediately
        break
    else:
        print("Username exists but data is invalid. Please choose a different username.")

# Main loop
while True:
    getcoins = random.randint(range1, range2)
    choice = input('Enter your choice of getting coins (c), upgrade (u), or stats (s): ')

    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen

    if choice == 'c':  # Get coins function
        coins += getcoins
        upload_stats()
        print(f'You got {getcoins} coins. (Stats auto-uploaded!)')

    elif choice == 'u':  # Upgrade function
        cost = mecn * 10
        print(f'More Coins (mecn) Cost: {cost}')
        upgrade = input("Enter upgrade: ").lower()
        if upgrade == 'mecn' and coins >= cost:
            mecn += 1
            coins -= cost
            range1 += 2
            range2 += 2
            upload_stats()
            print("Upgrade applied! (Stats auto-uploaded!)")
        else:
            print("Not enough coins!")

    elif choice == 's':
        print(f'Coins: {coins}, Upgrade Level: {mecn}')

    else:
        print("Invalid choice!")
