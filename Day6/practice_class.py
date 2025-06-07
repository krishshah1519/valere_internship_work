
class Practice:
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def cout(self):
        print(f"Hello {self.name}, you are {self.age} year old")

    def pp(self):
        print("hi")


Student1 = Practice("krish",21)
Student1.cout()

class AgeCheck(Practice):
    def __init__(self,home):
        self.home = home

    def out(self):
        print(f" you have {self.home} home")

ss  = AgeCheck(1)

ss.pp()