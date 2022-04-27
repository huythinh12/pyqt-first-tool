class A():
    def __init__(self):
        pass

class B():
    def __init__(self):
        self.point = 1;
        self.clone = C()

class C():
    def __init__(self):
        self.name = "pin";
        
instanceB = B()
print(instanceB.clone.name)