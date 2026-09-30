class Dog:
    # __init__ runs when you create an instance (the "constructor").
    # self = the instance being created. Always the first parameter.
    def __init__(self, name, age):
        self.name = name      # attribute: stored ON the instance
        self.age = age

    # A method — a function that belongs to the class.
    def bark(self):
        return f"{self.name} says WOOF!"

    def birthday(self):
        self.age += 1         # methods can modify the instance's attributes

class Puppy(Dog):
    def bark(self):
        return f"{self.name} says yip! yip!"
# Creating instances:
rex = Dog("Rex", 3)
bella = Dog("Bella", 5)
max = Puppy("Max", 1)

print(rex.name)        # Rex
print(rex.bark())      # Rex says WOOF!
rex.birthday()
print(rex.age)         # 4

print(max.bark())
