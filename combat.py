import random
from utils import Colors
from enemy import spawn_enemy

class Combat:
    def __init__(self, player, world):
        self.player = player
        self.world = world
        self.enemy = None

    def start_combat(self):
        self.enemy = spawn_enemy(self.player.position, self.player.level)
        
        if not self.enemy:
            print(f"{Colors.GREEN}აქ ახლა მშვიდია...{Colors.RESET}")
            return False

        print(f"\n{Colors.RED}{Colors.BOLD}⚔️ ბრძოლა დაიწყო!{Colors.RESET}")
        print(f"მტერი: {self.enemy.name} (ლევ.{self.enemy.level})")

        while self.enemy.is_alive and self.player.hp > 0:
            self.show_combat_status()
            self.player_action()
            
            if not self.enemy.is_alive:
                self.victory()
                break
                
            if self.player.hp <= 0:
                break

            # მტრის შეტევა
            self.enemy.attack(self.player)
            if self.player.take_damage(self.enemy.attack(self.player)):
                return False  # მოთამაშე მოკვდა

        return True

    def show_combat_status(self):
        print(f"\n{Colors.BOLD}--- ბრძოლის სტატუსი ---{Colors.RESET}")
        print(f"👤 შენ: HP {self.player.hp}/{self.player.max_hp} | ჯავშანი {self.player.armor}")
        print(f"👹 მტერი: {self.enemy.status()}")
        if self.player.current_vehicle:
            print(f"🚗 ვაჰიკლი: {self.player.current_vehicle.name} ({self.player.current_vehicle.health}% )")

    def player_action(self):
        print(f"\n{Colors.BOLD}რას გააკეთებ?{Colors.RESET}")
        print("1. სროლა")
        print("2. Headshot-ის მცდელობა (რისკიანი)")
        print("3. დამალვა / პოზიციის შეცვლა")
        print("4. გამოყენება (სამკურნალო ჩანთა)")
        if self.player.current_vehicle:
            print("5. მანქანით დავარდნა (Ram Attack)")
        print("6. გაქცევა")

        choice = input(f"\n{Colors.CYAN}არჩევანი (1-6): {Colors.RESET}")

        if choice == "1":
            self.shoot(normal=True)
        elif choice == "2":
            self.shoot(normal=False, headshot_attempt=True)
        elif choice == "3":
            self.change_position()
        elif choice == "4":
            self.use_heal()
        elif choice == "5" and self.player.current_vehicle:
            self.ram_attack()
        elif choice == "6":
            if self.try_escape():
                return
        else:
            print("არასწორი არჩევანი, სცადე თავიდან.")
            self.player_action()

    def shoot(self, normal=True, headshot_attempt=False):
        base_damage = 25 + self.player.damage_bonus + random.randint(5, 20)
        
        if headshot_attempt:
            if random.random() < (self.player.crit_chance / 100):
                self.enemy.take_damage(base_damage, is_headshot=True)
            else:
                print(f"{Colors.YELLOW} промахнулись по голове...{Colors.RESET}")
                self.enemy.take_damage(base_damage // 2)
        else:
            self.enemy.take_damage(base_damage)

    def change_position(self):
        self.enemy.distance += random.randint(-30, 40)
        self.enemy.distance = max(30, min(180, self.enemy.distance))
        print(f"📍 პოზიცია შეცვლილი. ახლანდელი მანძილი: {self.enemy.distance} მეტრი")

    def use_heal(self):
        if "სამკურნალო ჩანთა" in self.player.inventory:
            self.player.inventory.remove("სამკურნალო ჩანთა")
            self.player.heal(40)
        else:
            print("არ გაქვს სამკურნალო ჩანთა!")

    def ram_attack(self):
        if self.player.current_vehicle:
            damage = 45 + self.player.current_vehicle.armor // 2
            print(f"🚗 მანქანით დაეჯახე მტერს!")
            self.enemy.take_damage(damage)
            self.player.current_vehicle.take_damage(15)

    def try_escape(self):
        if random.random() < 0.6:
            print(f"{Colors.GREEN}✅ წარმატებით გაიქეცი!{Colors.RESET}")
            return True
        else:
            print(f"{Colors.RED}გაქცევა ვერ მოხერხდა!{Colors.RESET}")
            return False

    def victory(self):
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 გამარჯვება!{Colors.RESET}")
        loot = self.enemy.get_loot()
        
        print(f"+ {self.enemy.exp_reward} EXP  |  + {self.enemy.gold_reward} ოქრო")
        self.player.gain_exp(self.enemy.exp_reward)
        self.player.gold += self.enemy.gold_reward

        for item, qty in loot:
            if item == "ოქრო":
                self.player.gold += qty
            else:
                for _ in range(qty):
                    self.player.inventory.append(item)
            print(f"   + {qty} × {item}")
