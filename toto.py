class a:
    def __init__(self):
        self.toto = "lol"

    def __call__(self):
        print("CALLLLL")
        return self.toto

    def __repr__(self):
        return "repr"

    def __str__(self):
        return "dsdfg"


lol = a()
toto = "lol" + lol
