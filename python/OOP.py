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

class Cat(Pet):
    # 상속받는 클래스의 메서드를 그대로 복붙해도 되지만 이렇게 구현해줄 수 있습니다.
    # 복붙하는 것과 같은 동작은 아닙니다.
    # 1. 복붙할 경우(self.name = name, self.age = age), Cat의 attribute로 name과 age가 생겨 대입됩니다.
    # 2. super()로 부모 메서드를 사용할 경우 Pet의 attribute로 name과 age가 생겨 대입됩니다.
    def __init__(self, name, age, color):
        super().__init__(name, age)
        self.color = color

    def speak(self):
        print("Meow")

    def show(self):
        print(f"I am {self.name} and I am {self.age} and I am {self.color}")

    def __str__(self):
        return f'이름 : {self.name}, 나이 : {self.age}, 색깔 : {self.color}'
  
class Dog(Pet):
    def speak(self):
        print("Bark")
      
my_pet = Pet('Happy', 1)
print(my_pet)
# name : Happy, age : 1

kitty = Cat("kitty", 10, 'yellow')
print(kitty)
# 이름 : kitty, 나이 : 10, 색깔 : yellow