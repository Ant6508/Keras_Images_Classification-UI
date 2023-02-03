n = 10
h =10

def initialisation():
    s = []
    for i in range(n):
        s.append(1)
    return s

def initialisation_anti():
    s = []
    for i in range(h):
        sens=1
        if i % 2 != 0:
            sens=-1
        m = initialisation()
        m = [x*sens for x in m]
        s.append(m)
    return s
print(initialisation_anti())
