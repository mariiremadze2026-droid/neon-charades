from utils import clear, Colors, slow_print
from player import Player
from world import World
from combat import Combat

def main():
    clear()
    print(f"{Colors.BOLD}{Colors.CYAN}")
    slow_print("======================================")
    slow_print("       მთის წყევლა")
    slow_print("       სიბნელის გული")
    slow_print("======================================")
    print(f"{Colors.RESET}")

    # თამაშის დაწყება
    name = input("შენი სახელი: ").strip()
    if not name:
        name = "მეომარი"

    player = Player(name)
    world = World()

    print(f"\n{Colors.GREEN}მოგესალმებით, {player.name}!{Colors.RESET}")
    slow_print("სიბნელის წყევლა გავრცელდა მთელ მთიანეთზე...")
    slow_print("შენი მიზანია — იპოვო და გაანადგურო სიბნელის გული.\n")

    input("დააჭირე Enter-ს დასაწყებად...")

    # მთავარი თამაშის 루პი
    while True:
        clear()
        player.status()
        world.show_current_location(player)

        print(f"\n{Colors.BOLD}რას გააკეთებ?{Colors.RESET}")
        print("1. გადასვლა სხვა ლოკაციაში")
        print("2. ბრძოლის ძებნა")
        print("3. ინვენტარის ნახვა")
        print("4. დასვენება / განკურნება (უსაფრთხო ადგილზე)")
        print("5. ვაჰიკლის არჩევა")
        print("6. შენახვა")
        print("7. გამოსვლა")

        choice = input(f"\n{Colors.CYAN}არჩევანი (1-7): {Colors.RESET}")

        if choice == "1":
            moves = world.get_available_moves(player)
            print(f"\nშესაძლო მიმართულებები:")
            for i, loc in enumerate(moves, 1):
                print(f"{i}. {loc}")

            try:
                sel = int(input("\nარჩევანი: ")) - 1
                if 0 <= sel < len(moves):
                    world.move(player, moves[sel])
                    world.random_event(player)
            except:
                print("არასწორი არჩევანი.")

        elif choice == "2":
            combat = Combat(player, world)
            combat.start_combat()

        elif choice == "3":
            player.show_inventory()
            input("\nდააჭირე Enter-ს გასაგრძელებლად...")

        elif choice == "4":
            if world.locations[player.position].is_safe:
                player.heal(30)
                print("შენ დაისვენე და განიკურნე.")
            else:
                print("აქ უსაფრთხოდ დასვენება შეუძლებელია!")

        elif choice == "5":
            print("\n dost ხელმისაწვდომი ვაჰიკლები:")
            for i, v in enumerate(["ცხენი", "მოტოციკლი", "ჯიპი", "სატვირთო"], 1):
                print(f"{i}. {v}")
            try:
                sel = int(input("\nარჩევანი: ")) - 1
                vehicles = ["ცხენი", "მოტოციკლი", "ჯიპი", "სატვირთო"]
                if 0 <= sel < len(vehicles):
                    player.equip_vehicle(vehicles[sel])
            except:
                print("არასწორი არჩევანი.")

        elif choice == "6":
            from utils import save_game
            save_game(player)

        elif choice == "7":
            confirm = input("ნამდვილად გინდა გამოსვლა? (დიახ/არა): ")
            if confirm.lower() in ["დიახ", "დ", "yes", "y"]:
                print("ნახვამდის!")
                break

        # თამაშის დასასრული თუ HP 0-ზე დაეცა
        if player.hp <= 0:
            print(f"{Colors.RED}{Colors.BOLD}თამაში დასრულდა...{Colors.RESET}")
            break

        input(f"\n{Colors.BOLD}დააჭირე Enter-ს გასაგრძელებლად...{Colors.RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}თამაში შეწყდა.{Colors.RESET}")
