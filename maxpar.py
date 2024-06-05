from globalVar import *
from random import randint
from streamlit import graphviz_chart
from graphviz import Digraph
from threading import Thread
from time import sleep, time
from timeit import timeit


class Task:
# Cette classe définit une structure de base pour une tâche, avec des attributs pour son nom, les données qu'elle lit et écrit et une méthode "run" pour éxecuter la tâche.

    name = ""
    reads = []
    writes = []
    run = None


    def __init__(self, name, reads = [], writes = [], run = None):
        self.name = name
        self.reads = reads
        self.writes = writes
        self.run = run

class TaskSystem:
# Définit le systeme de tâches avec une liste de tâches à executer, des précedences entre elles, 
# un graphe de parallelisation et une estimation de temps d'exécution séquentielle et parallele

    listTasks = list
    precedences = dict
    graphPar = {}
    seq_time = None
    par_time = None


    def __init__(self, listTasks, precedences):
    # Initialise une instance avec une liste de tâches et un dictionnaire de précédences après avoir vérifié avec les méthodes verificationListe et verificationDictionnaire
        
        self.listTasks = self.verificationListe(listTasks)
        self.precedences = self.verificationDictionnaire(precedences)
        # Création du système de tâche parallèlisé
        self.grapPar = self.graphMaxPar()


    def verificationListe(self, liste):
    # Parcours une liste de tâches pour vérifier qu'il n'y a pas de doublons de noms, s'il y en à, renvoie les noms, sinon, renvoie la liste originale
        valide = True
        for i in range(len(liste)):
            for j in range(i+1,len(liste)):
                if liste[i].name == liste[j].name:
                    print("Les tâches", i, "et", j, "ont le même nom :", liste[i].name)
                    valide = False

        if valide == False:
            exit()

        return liste
    

    def verificationDictionnaire(self, dic):
    # Valide le dictionnaire de précedence pour une liste de tâches
        # pour avoir le tableau avec le nom des taches
        nom_taches = []
        for obj in self.listTasks:
            nom_taches.append(obj.name)

        valide = True

        # test si les taches ont une clé dans le dictionniaire
        for tache in nom_taches:
            if tache not in dic:
                print("La tache '", tache, "' n'a pas de clé dans le dictionnaire")
                valide = False

        for cle, valeur in dic.items():

            # test si il y a des clés inutiles
            if cle not in nom_taches :
               print("La tache '", cle, "' du dictionnaire est inexistantes dans la liste des taches")
               valide = False

            # test si dans le dictionnaire la tableau retourné par une clé n'a pas de tache qui n'existe pas
            for nom in valeur:
                if nom not in nom_taches:
                    print("Pour la clé : '", cle, "' le tableau associé a la tache '", nom, "' qui n'est pas dans la liste des taches")
                    valide = False

        if valide == False:
            exit()

        return dic


    def testInterference(self, t1, t2): 
    # Cette fonction verifie et teste les conditions de Bernstein entre des tâches. Renvoie False si aucune condition est remplie et indique donc que 
    # les tâches sont non-interferentes et qu'elles respectent les conditions de Bernstein
                                        
        # on vérifie que les tâches ne sont pas les memes
        if (t1 != t2):
            # on test chaques conditions de Bernstein
            # et on renvoie True si l'une d'entre elles n'est pas respectées 
            for read in t1.reads:
                if read in t2.writes:
                    return True
                
            for read in t2.reads:
                if read in t1.writes:
                    return True
   
            for write in t1.writes:
                if write in t2.writes:
                    return True
            # on retourne False si toute les conditions de Bernstein sont respectées
            # et donc que les tâches T1 et T2 sont non-interférentes.
            return False
        else:
            return False
        

    def graphMaxPar(self):
    # Construit un graphe de parallelisme maximal en éliminant les redondance.
        graphMaxPar = {}

        # création du graphique avec éventuelles redondances
        for t1 in self.listTasks:
            for t2 in self.listTasks:
                if(self.testInterference(t1, t2)):
                    if(len(self.getDependencies(t1.name))<len(self.getDependencies(t2.name))):
                        if t2.name in graphMaxPar:
                            graphMaxPar[t2.name].append(t1.name)
                        else:
                            graphMaxPar[t2.name] = [t1.name]
        
        # suppression des arc redondants
        # on parcours les valeur du dictionnaire
        for followingTasks in graphMaxPar.values():
            # on parcours chaques paire de tache dans la liste (valeur du dictionnaire)
            # task et otherTask sont des taches dans cette liste
            taskToRemove = []
            for task in followingTasks:
                for otherTask in followingTasks:
                    # fonction pour savoir si depuis otherTask on peut remonter à task
                    if(task != otherTask and self.isCommingFrom(graphMaxPar, task, otherTask)):
                        # on ajoute task aux tâches à supprimer
                        taskToRemove.append(task)
            # on supprime les tasks redondantes
            for task in taskToRemove: 
                if task in followingTasks: followingTasks.remove(task)

        # on retourne le graphique sans redondance sous forme de dictionnaire
        self.graphPar = graphMaxPar
        print(graphMaxPar)
        # return graphMaxPar


    def isCommingFrom(self, graph, ftask1, ftask2):
        # On parcours en profondeur le tableau pour trouver un chemin depuis ftask2 vers ftask1
        # en utilisant la recusivité on test tous les chemins possible
        # on s'arrète quand on est au bout d'un chemin
        if(graph.get(ftask2)):
            for task in graph.get(ftask2):
                # on test si ftask2 mène vers ftask1
                if(task == ftask1):
                    # si c'est le cas on retourne VRAI
                    return True
                else:
                    # sinon on relance la fonction pour tester plus en profondeur dans le chemin
                    if(self.isCommingFrom(graph, ftask1, task)):
                        return True
        return False


    def getDependencies(self, nomTache):
        # on recupere le dictionnaire de precedence du taskSystemn
        # et on recupere la valeur correspondant a la clé "nomTache"
        return self.precedences.get(nomTache)
    

    def runSeq(self):
    # Execute les taches du système de faaçon séquentielle en respectant l'ordre imposé par la relation de précédence.

        # Sauvegarder l'état initial des variables globales
        initial_state = globals().copy()
        
        for i in range(len(self.listTasks)):
            for task in self.listTasks:
                if len(self.getDependencies(task.name)) == i:
                    task.run()
                    break
        
        # Restaurer l'état initial des variables globales
        globals().update(initial_state)


    def run(self):
    # Initialisation des listes pou
        # Sauvegarder l'état initial des variables globales
        initial_state = globals().copy()
        # Créer un dictionnaire pour garder une trace de l'état d'exécution de chaque tâche
        tasksTodo = self.listTasks.copy()
        tasksToRun = []
        tasksRunning = []
        tasksEnded = []

        # Définir la fonction à exécuter par chaque thread
        def execute_task(task):
        # Lance une tache, la marque comme terminée et la retire des tâches en cours
            task.run()
            tasksEnded.append(task.name)
            tasksRunning.remove(task.name)

        # Créer et démarrer les threads pour chaque tâche
        threads = []

        
        while(tasksTodo):
        # Tant qu'il reste des tâches a faire    
            for task in tasksTodo.copy():
            # Vérifie les tâches prêtes à être exécutée
                if((self.graphPar.get(task.name) == None) or all(elem in tasksEnded for elem in self.graphPar.get(task.name))):
                # Si une tâche n'a pas de dépendances ou si toutes ses dépendances sont terminées
                    tasksToRun.append(task) # Ajoute la tache à être executée
                    tasksTodo.remove(task)  # Retire la tache des taches en cours
            
            if(tasksToRun):
            # Execute les taches pretes en parallele en demarrant un thread pour chaque tache dans tasksoRun
            # puis reinitialise la liste pour la prochaine itération
                for task in tasksToRun:    
                    thread = Thread(target=execute_task, args=(task,))
                    thread.start()
                    threads.append(thread)
                    tasksRunning.append(task.name)
                tasksToRun = []

        # Attendre la fin de tous les threads
        for thread in threads:
            thread.join()
        
        # Restaurer l'état initial des variables globales
        globals().update(initial_state)


    def parCost(self, occ=10):
        # Calule du temps d'execution séquentiel pour "occ" occurence de runSeq()
        timeSeq = timeit(lambda: self.runSeq(), number=occ)
        # Calule du temps d'execution parallèle pour "occ" occurence de run()
        timePar = timeit(lambda: self.run(), number=occ)
        # affichage des temps moyens en divisant le total par le nombre d'occurence
        print('Temps d\'execution séquentielle :', timeSeq/occ, '\nTemps d\'execution parallèle :', timePar/occ)


    def detTestRnd(self, occ=10): ######################################################## A COMMENTER
        if __name__ == "__main__":
            # Générer des variables aléatoires pour chaque variable globale
            global M1, M2, M3, M4, M5
            M1 = randint(1,100)
            M2 = randint(1,100)
            M3 = randint(1,100)
            M4 = randint(1,100)
            M5 = randint(1,100)
            res = None
            for _ in range(occ):
                self.run()
                if(res and res != M5):
                    print('Le système de tâche n\'est pas déterministe !')
                    break
                res = M5


        else:
            print('La fonction detTestRnd() n\'est pas utilisable.')
        
        
    def draw(self):

        # Création d'un objet Digraph
        dot = Digraph()

        # Ajout des nœuds pour chaque tâche
        for task in self.graphPar:
            dot.node(task)

        # Ajout des arêtes pour chaque dépendance
        for task, followingTasks in self.graphPar.items():
            for ftask in followingTasks:
                # dot.edge(task, ftask)
                dot.edge(ftask, task)

        # Génération du fichier graphique (format PDF par défaut)
        # dot.render('task_system_graph')

        # Affichage du graphe
        print(dot) # console
        graphviz_chart(dot) # streamlit (web)


########################### CODE INTERNE A LA LIBRAIRIE NON EXECUTE DEPUIS L'EXTERIEUR ###########################
############################################### A DES FINS DE TEST ###############################################
##################################################################################################################

if __name__ == "__main__":
    # Permet de test la méthode detTestRnd()
    M1 = None
    M2 = None
    M3 = None
    M4 = None
    M5 = None

    def runT1():
        print("tache T1 lancée")  
        global M1, M2, M3
        M3 = M1 + M2 
        sleep(0.2)
        print("tache T1 terminée")
    def runT2():
        print("tache T2 lancée")
        global M1, M4
        M4 = M1 / 2
        sleep(0.2)
        print("tache T2 terminée")
    def runT3():
        print("tache T3 lancée")
        global M1, M3, M4
        M1 = M3 - M4
        sleep(0.2)
        print("tache T3 terminée")
    def runT4():
        print("tache T4 lancée")
        global M3, M4, M5
        M5 = M3 - (2 * M4)
        sleep(0.2)
        print("tache T4 terminée")
    def runT5():
        print("tache T5 lancée")
        global M2, M4
        M2 = M4 + 6            
        sleep(0.2)
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
        global M1, M2, M3, M4, M5
        M5 = (2 * M1) - M3
        sleep(0.2)
        print("tache T8 terminée")
        print(f'résultat final = {M5}')
    

    t1 = Task("T1", reads=["M1", "M2"], writes=["M3"], run=runT1)
    t2 = Task("T2", reads=["M1"], writes=["M4"], run=runT2)
    t3 = Task("T3", reads=["M3", "M4"], writes=["M1"],run=runT3)
    t4 = Task("T4", reads=["M3", "M4"], writes=["M5"], run=runT4)
    t5 = Task("T5", reads=["M4"], writes=["M2"],run=runT5)
    t6 = Task("T6", reads=["M5"], writes=["M5"],run=runT6)
    t7 = Task("T7", reads=["M1", "M2", "M4"], writes=["M4"],run=runT7)
    t8 = Task("T8", reads=["M1", "M3"], writes=["M5"],run=runT8)


    tasks = [t1, t2, t3, t4, t5, t6, t7, t8]
    precedences = {'T1': [], 'T2': ['T1'], 'T3': ['T1', 'T2'], 'T4': ['T1','T2','T3'], 'T5': ['T1','T2','T3','T4'], 'T6': ['T1','T2','T3','T4','T5'], 'T7': ['T1','T2','T3','T4','T5','T6'], 'T8': ['T1','T2','T3','T4','T5','T6','T7']}
    s2 = TaskSystem(tasks, precedences)
    s2.detTestRnd()

    ##################################################################################################################
    ##################################################################################################################
    ##################################################################################################################