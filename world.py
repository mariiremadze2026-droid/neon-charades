from utils import Colors
import random

class Location:
    def __init__(self, name, description, danger_level=0, has_shop=False, is_safe=False):
        self.name = name
        self.description = description
        self.danger_level = danger_level      # 0-10
        self.has_shop = has_shop
        self.is_safe = is_safe
        self.visited = False


class World:
    def __init__(self):
        self.locations = {
            "სოფელი გორისფერი": Location(
                name="სოფელი გორისფერი",
                description="მშვიდი მთის სოფელი. აქ არის შენი სახლი, სასტუმრო და მცირე ბაზარი.",
                danger_level=0,
                has_shop=True,
                is_safe=True
            ),
            
            "მუქი ტყე": Location(
                name="მუქი ტყე",
                description="სქელი ხეები ბლოკავს მზის შუქს. ყველგან გრძნობ უცნაურ სიმშვიდეს...",
                danger_level=5
            ),
            
            "მთის კალთები": Location(
                name="მთის კალთები",
                description="ციცაბო ბილიკები და ძველი ქვის ნანგრევები. ძალიან ციოდა.",
                danger_level=6
            ),
            
            "ძველი გამოქვაბული": Location(
                name="ძველი გამოქვაბული",
                description="ბნელი და სველი გამოქვაბული. კედლებზე უცნაური სიმბოლოებია.",
                danger_level=8
            ),
            
            "წყევლილი ციხე": Location(
                name="წყევლილი ციხე",
                description="ძველი, დანგრეული ციხე-სიმაგრე. აქედან იგრძნობა სიბნელის ძალა.",
                danger_level=9
            ),
            
            "სიბნელის ტაძარი": Location(
                name="სიბნელის ტაძარი",
                description="საშინელი ადგილი, სადაც ყველაფერი დაიწყო...",
                danger_level=10
            )
        }

        # რუკის კავშირები (სად შეგიძლია გადასვლა)
        self.connections = {
            "სოფელი გორისფერი": ["მუქი ტყე", "მთის კალთები"],
            "მუქი ტყე": ["სოფელი გორისფერი", "მთის კალთები", "ძველი გამოქვაბული"],
            "მთის კალთები": ["სოფელი გორისფერი", "მუქი ტყე", "წყევლილი ციხე"],
            "ძველი გამოქვაბული": ["მუქი ტყე"],
            "წყევლილი ციხე": ["მთის კალთები", "სიბნელის ტაძარი"],
            "სიბნელის ტაძარი": ["წყევლილი ციხე"]
        }

    def show_current_location(self, player):
        loc = self.locations[player.position]
        print(f"\n{Colors.BOLD}{Colors.CYAN}📍 შენ ახლა ხარ: {loc.name}{Colors.RESET}")
        print(loc.description)
        
        if loc.is_safe:
            print(f"{Colors.GREEN}🛡️  ეს უსაფრთხო ადგილია.{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}⚠️ საფრთხის დონე: {loc.danger_level}/10{Colors.RESET}")

    def move(self, player, destination):
        current = player.position
        
        if destination in self.connections.get(current, []):
            player.position = destination
            loc = self.locations[destination]
            if not loc.visited:
                print(f"\n{Colors.BOLD}🌄 აღმოაჩინე ახალი ლოკაცია: {destination}{Colors.RESET}")
                loc.visited = True
            return True
        else:
            print(f"{Colors.RED}❌ იქედან ვერ წახვალ.{Colors.RESET}")
            return False

    def get_available_moves(self, player):
        return self.connections.get(player.position, [])

    def random_event(self, player):
        """რენდომული მოვლენები ლოკაციაში"""
        if random.random() < 0.25:   # 25% შანსი
            events = [
                f"{Colors.YELLOW}იპოვე მიტოვებული ჩანთა. +30 ოქრო!{Colors.RESET}",
                f"{Colors.GREEN}იპოვე სამკურნალო მცენარე. +20 HP{Colors.RESET}",
                f"{Colors.RED}ხაფანგი! დაკარგე 15 HP{Colors.RESET}",
            ]
            print(random.choice(events))
            # აქ შეგვიძლია მოგვიანებით დავამატოთ ეფექტები
