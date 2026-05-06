from vehicle import vehicles_db
from utils import Colors

class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.armor = 25
        self.level = 1
        self.exp = 0
        self.exp_to_next = 100
        self.gold = 200
        
        self.position = "სოფელი გორისფერი"
        self.current_vehicle = None
        self.inventory = ["სამკურნალო ჩანთა", "ტყვია", "ტყვია"]  # საწყისი ინვენტარი
        
        # სტატისტიკა
        self.damage_bonus = 0
        self.crit_chance = 15   # პროცენტი

    def level_up(self):
        self.level += 1
        self.max_hp += 25
        self.hp = self.max_hp
        self.damage_bonus += 5
        self.exp_to_next = int(self.exp_to_next * 1.5)
        print(f"\n{Colors.GREEN}🎉 ლეველი ავიდა! ახლა ხარ ლეველი {self.level}{Colors.RESET}")

    def gain_exp(self, amount):
        self.exp += amount
        print(f"{Colors.CYAN}+{amount} EXP{Colors.RESET}")
        
        while self.exp >= self.exp_to_next:
            self.exp -= self.exp_to_next
            self.level_up()

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)
        print(f"{Colors.GREEN}❤️ განიკურნე +{amount} HP (ახლა {self.hp}/{self.max_hp}){Colors.RESET}")

    def take_damage(self, damage):
        actual_damage = damage
        
        # ჯავშნის შემცირება
        if self.armor > 0:
            reduction = min(self.armor, damage // 3)
            actual_damage -= reduction
            self.armor = max(0, self.armor - 8)
        
        self.hp -= actual_damage
        print(f"{Colors.RED}💥 მიიღე {actual_damage} დაზიანება! (HP: {self.hp}){Colors.RESET}")
        
        if self.hp <= 0:
            print(f"{Colors.RED}{Colors.BOLD}☠️ შენ მოკვდი... თამაში დასრულდა.{Colors.RESET}")
            return True  # თამაშის დასასრული
        return False

    def equip_vehicle(self, vehicle_name):
        if vehicle_name in vehicles_db:
            self.current_vehicle = vehicles_db[vehicle_name]
            print(f"{Colors.YELLOW}🚙 ახლა მართავ {vehicle_name}-ს!{Colors.RESET}")
        else:
            print("❌ ასეთი ვაჰიკლი არ მოიძებნა.")

    def status(self):
        veh = self.current_vehicle.name if self.current_vehicle else "ფეხით"
        print(f"""
{Colors.BOLD}=== {self.name} ===
HP: {self.hp}/{self.max_hp}    ჯავშანი: {self.armor}
ლეველი: {self.level}     EXP: {self.exp}/{self.exp_to_next}
ოქრო: {self.gold}     ვაჰიკლი: {veh}
მდებარეობა: {self.position}
============================{Colors.RESET}
""")

    def show_inventory(self):
        print(f"\n{Colors.BOLD}🎒 ინვენტარი:{Colors.RESET}")
        if not self.inventory:
            print("ცარიელია...")
        else:
            from collections import Counter
            count = Counter(self.inventory)
            for item, qty in count.items():
                print(f"   • {item} ×{qty}")
