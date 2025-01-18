import time


"""

- Features of a Virtual -

1. Name Your Pet: Let the user give their pet a name.
2. Pet Stats: Track stats like hunger, happiness, and energy.
3. Actions for the Pet: Allow the user to feed, play with, or let the pet rest.
4. Health Monitoring: Decrease stats over time if the user doesn't take care of the pet.
5. Endgame: Display messages when the pet becomes too unhappy or starves.

"""


class VirtualPet:
    
    def __init__(self,name):
        self.name = name
        self.hunger = 30
        self.energy = 30
        self.happiness = 30
        
    def feed(self):
        self.hunger = max(0, self.hunger - 10)
        print(f"You have fed {self.name}. Hunger is now {self.hunger}")
        
    def play(self):
        # increases happiness
        self.happiness = min(100, self.happiness + 10)
        self.energy = max(0, self.energy-10)
        print(f"You have made {self.name}. Happiness is at {self.happiness}, and energy is at now {self.energy}")
        
    def rest(self):
        # gain energy
        self.energy = min(100,self.energy + 10)
        print(f"You have rested {self.name}. Energy is now at {self.energy}")
        
    def check_status(self):
        return self.happiness == 0 or self.energy == 0 or self.hunger == 100
        
    def tick(self):
        self.energy -= 1
        self.happiness -= 1
        self.hunger += 1

        print(f"\nHunger at {self.hunger} \n Energy at {self.energy} \n Happiness at {self.happiness}")
        
        
#  simulation loop
def main():
    pet_name = input("What would you like to name your virtual pet? ")
    pet = VirtualPet(pet_name)
    print(f"\nMeet {pet.name}. Take care of this adorable little one")
    
    while True:
        print(f"\n Here are the options \n 1. Feed \n 2. Play \n 3. Rest \n 4. Check status \n 5. Quit")
        
        choice = input("What would you like to do now? ")
        
        if choice == '1':
            pet.feed()
        elif choice == '2':
            pet.play()
        elif choice == '3':
            pet.rest()
        elif choice == '4':
            pet.check_status()
        elif choice == '5':
            print("Goodbye!")
            break
            
        pet.tick()
        
        if pet.check_status():
            print("Pet can't continue now")
            break
        
        time.sleep(1)        
main()
    
    
    
    
    
    