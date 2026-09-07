
class A:
    def __init__(self, val):
        self.a = val

    def greetings(self):
        return f'Hello, {self.a}!'


x1 = A(1)
x2 = A(2)

print(A.__dict__)

print(x.greetings())








