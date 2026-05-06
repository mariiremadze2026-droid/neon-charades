import random

class Vehicle:
    def __init__(self, name, speed, armor, fuel_max):
        self.name = name
        self.speed = speed          # კმ/საათში (ტექსტურად)
        self.armor = armor
        self.fuel_max = fuel_max
        self.fuel = fuel_max
        self.health = 100

    def drive(self, distance):
        fuel_use = distance * 0.7
        if self.fuel < fuel_use:
            print("⛽ საწვავი არ კმარა!")
            return False
        self.fuel -= fuel_use
        print(f"🚗 {self.name}-ით გადაადგილდი {distance} კმ.")
        return True

    def take_damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            print(f"💥 {self.name} განადგურდა!")
            return True
        return False

    def refuel(self, amount):
        self.fuel = min(self.fuel_max, self.fuel + amount)
        print(f"⛽ საწვავი შევსებულია ({self.fuel}/{self.fuel_max})")


vehicles_db = {
    "ცხენი": Vehicle("ცხენი", 12, 25, 999),
    "მოტოციკლი": Vehicle("მოტოციკლი", 25, 35, 30),
    "ჯიპი": Vehicle("ჯიპი", 18, 70, 55),
    "სატვირთო": Vehicle("სატვირთო", 14, 85, 80),
}
