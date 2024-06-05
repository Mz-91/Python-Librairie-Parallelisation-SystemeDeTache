from maxpar import *
from globalVar import *
initial_state = globals().copy()

# Définition des fonctions de tâches, simulant des opérations et des dépendances entre elles
def runT1():
    print("tache T1 lancée")  
    global M1, M2, M3
    M3 = M1 + M2 
    sleep(0.5)
    print("tache T1 terminée")
def runT2():
    print("tache T2 lancée")
    global M1, M4
    M4 = M1 / 2
    sleep(0.5)
    print("tache T2 terminée")
def runT3():
    print("tache T3 lancée")
    global M1, M3, M4
    M1 = M3 - M4
    sleep(1)
    print("tache T3 terminée")
def runT4():
    print("tache T4 lancée")
    global M3, M4, M5
    M5 = M3 - (2 * M4)
    sleep(1)
    print("tache T4 terminée")
def runT5():
    print("tache T5 lancée")
    global M2, M4
    M2 = M4 + 6            
    sleep(1)
    print("tache T5 terminée")
def runT6():
    print("tache T6 lancée")
    global M5
    M5 = M5 + 1
    sleep(0.2)
    print("tache T6 terminée")
def runT7():
    print("tache T7 lancée")
    global M1, M2, M4
    M4 = M1 + M2 - (M4 * 1/2)
    sleep(0.2)
    print("tache T7 terminée")
def runT8():
    print("tache T8 lancée")
    global M1, M3, M5, initial_state
    M5 = (2 * M1) - M3
    sleep(0.1)
    print("tache T8 terminée")
    print(f'résultat final = {M5}')
    globals().update(initial_state)
   
# Création des instances de tâches avec leurs dépendances et fonctions d'exécution associées
t1 = Task("T1", reads=["M1", "M2"], writes=["M3"], run=runT1)
t2 = Task("T2", reads=["M1"], writes=["M4"], run=runT2)
t3 = Task("T3", reads=["M3", "M4"], writes=["M1"],run=runT3)
t4 = Task("T4", reads=["M3", "M4"], writes=["M5"], run=runT4)
t5 = Task("T5", reads=["M4"], writes=["M2"],run=runT5)
t6 = Task("T6", reads=["M5"], writes=["M5"],run=runT6)
t7 = Task("T7", reads=["M1", "M2", "M4"], writes=["M4"],run=runT7)
t8 = Task("T8", reads=["M1", "M3"], writes=["M1", "M2", "M3", "M4", "M5"],run=runT8)


tasks = [t1, t2, t3, t4, t5, t6, t7, t8]
 # Liste de toutes les tâches à gérer
precedences = {'T1': [], 'T2': ['T1'], 'T3': ['T1', 'T2'], 'T4': ['T1','T2','T3'], 'T5': ['T1','T2','T3','T4'], 'T6': ['T1','T2','T3','T4','T5'], 'T7': ['T1','T2','T3','T4','T5','T6'], 'T8': ['T1','T2','T3','T4','T5','T6','T7']}
 # Définition des précédences entre tâches, indiquant l'ordre d'exécution
s2 = TaskSystem(tasks, precedences)
s2.draw()
# print(s2.graphmaxpar())
s2.parCost()

# t1 = Task("T1", reads=["M1"], writes=["M2"], run=runT1)
# t2 = Task("T2", reads=["M2"], writes=["M3"], run=runT2)
# t3 = Task("T3", reads=["M3"], writes=["M4"], run=runT3)
# t4 = Task("T4", reads=["M4"], writes=["M5"], run=runT4)
# t5 = Task("T5", reads=["M5"], writes=["M6"], run=runT5)
# t6 = Task("T6", reads=["M5"], writes=["M6"], run=runT6)
# t7 = Task("T7", reads=["M5"], writes=["M6"], run=runT7)
# t8 = Task("T8", reads=["M5"], writes=["M6"], run=runT8)

# tasks = [t1, t2, t3, t4, t5, t6, t7, t8]
# precedences = {'T1': [], 'T2': ['T1'], 'T3': ['T1', 'T2'], 'T4': ['T1','T2','T3'], 'T5': ['T1','T2','T3','T4'], 'T6': ['T1','T2','T3','T4','T5'],'T7': ['T1','T2','T3','T4','T5','T6'], 'T8': ['T1','T2','T3','T4','T5','T6','T7']}
# s2 = TaskSystem(tasks, precedences)
# s2.draw()
# s2.parCost()