from maxpar import *
#exemple1
X = None
Y = None
Z = None

def runT1():
        global X
        X = 1

def runT2():
        global Y
        Y = 2

def runTsomme():
        global X, Y, Z
        Z = X + Y

t1 = Task("T1", writes=["X"], run=runT1)
t2 = Task("T2", writes=["Y"], run=runT2)
tSomme = Task("somme", reads=["X", "Y"], writes=["Z"], run=runTsomme)

s1 = TaskSystem([t1, t2, tSomme], {"T1": [], "T2": [], "somme": ["T1", "T2"]})

print("========== Début de l'exécution de s1 ==========")
s1.runSeq()
print("========== Fin de l'exécution séquentielle de s1 ==========")

print("========== Début de l'exécution parallèle de s1 ==========")
s1.run()
print("========== Fin de l'exécution parallèle de s1 ==========")

print("========== Affichage du graphe de dépendances de s1 ==========")
s1.draw()

print("========== Début du test de déterminisme de s1 ==========")
print("Determinism Test Result:", s1.detTestRnd())
print("========== Fin du test de déterminisme de s1 ==========")

print("========== Calcul du coût d'exécution parallèle de s1 ==========")
s1.parCost(2)
print("========== Fin du calcul du coût d'exécution parallèle de s1 ==========")

#exemple2

# X, Y, Z = None, None, 0  # Reset variables


# def Print(value):
#         print(value)

# def run_T1():
#         global X
#         X = 5

# def run_T4():
#         global Z
#         Z = 7

# def run_T2():
#         global X,Z
#         X=X+Z

# def run_T3():
#         global Y
#         Print(Y)


# def run_T5():
#         global X,Y,Z
#         Y=X+Z

# t1 = Task(name="T1", writes=["X"], run=run_T1)
# t2 = Task(name="T2", writes=["X"],reads=["X","Z"], run=run_T2)
# t3 = Task(name="T3", reads=["Y"], run=run_T3)
# t4 = Task(name="T4", writes=["Z"], run=run_T4)
# t5= Task(name="T5", reads=["X", "Z"], writes=["Y"], run=run_T5)

# s2 = TaskSystem([t1,t2,t3,t4,t5],{"T1": [], "T2": ["T1"], "T3": ["T2"], "T4": [], "T5": ["T4"] })


# s2.run()

# print("Determinism Test Result:", s2.detTestRnd())
# s2.parCost(2)
# s2.draw()

#exemple3

"""def Print(value):
        print(value)

    def runT1():
        global X
        X = 1

    def runT2():
        global Y
        Y = 2

    def runT3():
        global X, Y, Z
        Z = X + Y

    def runT4():
        global Z
        Z += 1

    def runT5():
        global X
        X *= 2

    def runT6():
        global Y
        Y *= 3

    def runT7():
        global Z
        Z -= 2

    # Création des tâches avec les lectures et écritures appropriées
    t1 = Task(name="T1", writes=["X"], run=runT1)
    t2 = Task(name="T2", writes=["Y"], run=runT2)
    t3 = Task(name="T3", reads=["X", "Y"], writes=["Z"], run=runT3)
    t4 = Task(name="T4", reads=["Z"], run=runT4)
    t5 = Task(name="T5", writes=["X"], run=runT5)
    t6 = Task(name="T6", writes=["Y"], run=runT6)
    t7 = Task(name="T7", reads=["Z"], run=runT7)

    # Dictionnaire des dépendances
    dependency_dict = {
        "T1": [],
        "T7": ["T3"],
        "T6": ["T3"],
        "T3": ["T1"],
        "T5": ["T2"],
        "T4": ["T2"],
        "T2": ["T1"]
    }

    # Création du système de tâches

    s3 = TaskSystem([t1, t2, t3, t4, t5, t6, t7], dependency_dict)
    # Exemple d'utilisation des fonctionnalités de la bibliothèque
    s3.runSeq()  # Exécution séquentielle
    s3.run()  # Exécution parallèle
    s3.draw()  # Affichage du graphe de dépendances
   
    s3.parCost(10)  # Coût de l'exécution parallèle
    s3.detTestRnd(10)  # Test randomisé de déterminisme
"""