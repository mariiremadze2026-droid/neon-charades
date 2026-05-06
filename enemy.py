import random
from utils import Colors

class Enemy:
    def __init__(self, name: str, level: int, hp: int, damage: int, armor: int = 0, 
                 exp_reward: int = 0, gold_reward: int = 0):
        self.name = name
        self.level = level
        self.max_hp = hp
        self.hp = hp
        self.damage = damage
        self.armor = armor
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
        self.is_alive = True
        self.distance = random.randint(40, 160)   # მეტრები PUBG სტილში

    def take_damage(self, damage: int, is_headshot: bool = False) -> int:
        actual_damage = damage
        
        if is_headshot:
            actual_damage = int(damage * 1.85)
            print(f"{Colors.RED}💥 **HEADSHOT!**{Colors.RESET}")
        
        # მტრის ჯავშანი
        if self.armor > 0:
            reduction = min(self.armor, actual_damage // 3)
            actual_damage -= reduction
            self.armor = max(0, self.armor - 10)
        
        self.hp -= actual_damage
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
            print(f"{Colors.GREEN}✅ {self.name} დამარცხებულია!{Colors.RESET}")
        
        return actual_damage

    def attack(self, player) -> int:
        base_damage = random.randint(self.damage - 6, self.damage + 10)
        
        # მანძილის გავლენა
        if self.distance > 110:
            base_damage = int(base_damage * 0.65)
        elif self.distance < 50:
            base_damage = int(base_damage * 1.3)
        
        print(f"{Colors.RED}⚔️ {self.name} თავს გესხმის და აყენებს {base_damage} დაზიანებას!{Colors.RESET}")
        return base_damage

    def get_loot(self):
        loot = []
        
        loot.append(("ოქრო", random.randint(10, 35)))
        
        if random.random() < 0.7:
            loot.append(("ტყვია", random.randint(15, 40)))
        
        if random.random() < 0.45:
            loot.append(("სამკურნალო ჩანთა", 1))
        
        if random.random() < 0.25:
            loot.append(("ჯავშანი", 1))
        
        if random.random() < 0.15:
            loot.append(("იშვიათი ნივთი", 1))
            
        return loot

    def status(self):
        return f"{self.name} (Lv.{self.level}) | HP: {self.hp}/{self.max_hp} | მანძილი: {self.distance}m"


# ==================== მტრების მონაცემთა ბაზა ====================
enemies_db = {
    "მგელი": lambda lvl: Enemy("ველური მგელი", lvl, hp=55 + lvl*10, damage=14 + lvl*2, exp_reward=30, gold_reward=8),
    "გაურკვეველი": lambda lvl: Enemy("გაურკვეველი არსება", lvl, hp=70 + lvl*14, damage=20 + lvl*3, armor=10, exp_reward=45, gold_reward=15),
    "მონადირე": lambda lvl: Enemy("შავი მონადირე", lvl, hp=85 + lvl*12, damage=26 + lvl*4, armor=25, exp_reward=60, gold_reward=20),
    "გამარჯვებული": lambda lvl: Enemy("გამარჯვებული მეკვდარი", lvl, hp=110 + lvl*18, damage=30 + lvl*5, armor=40, exp_reward=85, gold_reward=28),
    "ჯავშანმანქანის მძღოლი": lambda lvl: Enemy("ჯავშანმანქანის მძღოლი", lvl, hp=130 + lvl*22, damage=38 + lvl*6, armor=55, exp_reward=110, gold_reward=45),
    "სიბნელის მცველი": lambda lvl: Enemy("სიბნელის მცველი", lvl, hp=180 + lvl*30, damage=48 + lvl*8, armor=70, exp_reward=180, gold_reward=80),
}


def spawn_enemy(location: str, player_level: int):
    """რენდომულად ქმნის მტერს"""
    if location == "სოფელი გორისფერი":
        return None

    spawn_rate = {
        "მუქი ტყე": 0.78,
        "მთის კალთები": 0.88,
        "გამოქვაბული": 0.95,
        "წყევლილი ციხე": 1.0,
        "სიბნელის ტაძარი": 1.0
    }.get(location, 0.65)

    if random.random() > spawn_rate:
        return None

    # ლოკაციის მიხედვით შესაძლო მტრები
    if location in ["სოფელი გორისფერი", "მუქი ტყე"]:
        pool = ["მგელი", "გაურკვეველი"]
    elif location in ["მთის კალთები"]:
        pool = ["გაურკვეველი", "მონადირე"]
    else:
        pool = ["მონადირე", "გამარჯვებული", "ჯავშანმანქანის მძღოლი"]

    if player_level >= 8:
        pool.append("სიბნელის მცველი")

    enemy_name = random.choice(pool)
    enemy_level = max(1, player_level + random.randint(-2, 3))
    
    return enemies_db[enemy_name](enemy_level)
