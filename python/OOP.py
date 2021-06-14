class Pet():
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f'name : {self.name}, age : {self.age}'

    def show(self):
        print(f'I am {self.name} and I am {self.age} years old')

    def speak(self):
        print("I don't know what I say")

my_pet = Pet('Happy', 1)
print(my_pet)