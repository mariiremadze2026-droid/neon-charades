import os
import json
import random
from time import sleep

# ფერები კონსოლისთვის
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def slow_print(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        sleep(delay)
    print()


def save_game(player, filename="save.json"):
    data = {
        "name": player.name,
        "hp": player.hp,
        "level": player.level,
        "exp": player.exp,
        "gold": player.gold,
        "position": player.position,
        "inventory": player.inventory
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"{Colors.GREEN}✓ თამაში შენახულია!{Colors.RESET}")


def load_game(filename="save.json"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return None
