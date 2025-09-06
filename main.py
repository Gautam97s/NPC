# This is the main game loop for the text-based NPC game.
# It handles player movement, proximity checks, and user interaction.

import sys
from dialogues import initialize_chromadb, get_dialogue

# --- Game Entities ---
# Player class to manage state.
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.reputation = 0 # Default reputation

    def update_reputation(self, amount):
        """Updates the player's reputation based on their actions."""
        self.reputation += amount
        print(f"[STATUS] Your reputation has changed by {amount}. Your new reputation is: {self.reputation}")

# NPC is represented as a simple dictionary.
npc = {"x": 50, "y": 50, "name": "Farmer Bob"}
is_near_npc = False

# Initialize the player object.
player = Player(x=0, y=0)

# Define reputation changes for different actions.
REPUTATION_CHANGES = {
    "greeting": 1,
    "trade": 2,
    "small_talk": 1,
    "quests": 5,
    "farewell": 1,
    "damaged_crops": -10,
    "stealing": -15,
    "mocking": -5,
    "helped": 10,
    "lost_battle": 0
}

# --- Game Functions ---
def check_proximity():
    """Simulates checking if the player is near the NPC."""
    global is_near_npc
    distance = ((player.x - npc['x'])**2 + (player.y - npc['y'])**2)**0.5
    if distance < 10:
        if not is_near_npc:
            print(f"You have approached {npc['name']}!")
            is_near_npc = True
    else:
        is_near_npc = False

# --- Main Game Loop ---
def main():
    print("Welcome to the text-based NPC game.")
    print(f"You are at coordinates ({player.x}, {player.y}). Farmer Bob is at ({npc['x']}, {npc['y']}).")
    print("Type 'move [direction]' (e.g., 'move north') or 'interact' to begin.")
    print("---")
    
    # Initialize the ChromaDB collection
    dialogue_collection = initialize_chromadb()

    while True:
        check_proximity()
        user_input = input("> ").strip().lower().split()
        
        command = user_input[0] if user_input else ""
        
        if command == "move":
            direction = user_input[1] if len(user_input) > 1 else ""
            if direction == "north": player.y += 5
            elif direction == "south": player.y -= 5
            elif direction == "east": player.x += 5
            elif direction == "west": player.x -= 5
            print(f"You moved. Your new position is ({player.x}, {player.y}).")
            
        elif command == "interact":
            if is_near_npc:
                print(f"You start a conversation with {npc['name']}.")
                print("Choose an interaction:")
                print("1. Greet (e.g., 'greeting')")
                print("2. Trade (e.g., 'trade')")
                print("3. Small Talk (e.g., 'small_talk')")
                print("4. Quests (e.g., 'quests')")
                print("5. Farewell (e.g., 'farewell')")
                print("6. Special Interaction (e.g., 'lost_battle' or 'damaged_crops')")
                
                choice = input("Your choice: ").strip().lower()

                # Get the dialogue from the dialogue module
                response = get_dialogue(dialogue_collection, choice)
                print(f"{npc['name']}: {response}")

                # Update player reputation after the interaction
                if choice in REPUTATION_CHANGES:
                    player.update_reputation(REPUTATION_CHANGES[choice])
                
            else:
                print("You are not close enough to anyone to interact.")

        elif command == "status":
            print(f"Your current position is ({player.x}, {player.y}).")
            print(f"Your current reputation is: {player.reputation}")

        elif command == "exit":
            print("Thanks for playing!")
            sys.exit(0)
        
        else:
            print("Invalid command. Try 'move [direction]', 'interact', or 'status'.")

if __name__ == "__main__":
    main()
