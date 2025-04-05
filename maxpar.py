import threading
import networkx as nx
import matplotlib.pyplot as plt
import time
import random

X=None
Y=None 
Z=None 

# Définition de la classe Task
class Task:
    def __init__(self, name="", reads=None, writes=None, run=None):
        self.name = name
        self.reads = reads if reads is not None else []
        self.writes = writes if writes is not None else []
        self.run = run

# Définition du système de tâches
class TaskSystem:
    #definition du constructeur qui prendera en parametre les noms des taches et le dictionnaire de preferance de precedance 
    def __init__(self, liste_taches, preferance_precedence):
        self.liste_taches = liste_taches
        self.precedence = preferance_precedence
        #declarer un dictionaire de contrainte que le systeme definira lui meme avec une fonction defineDependencies qui utilisera la liste des reads et writes pour les definir
        self.dictionnaire_contraintes = self.defineDependencies()
        if not self.validateInputs():
            # Si les entrées ne sont pas valides, ne continuez pas avec l'initialisation
            return


    #la fonction pour retourner un dictionnaire de contrainte et cela en analysant la liste des writes et des reads

    def defineDependencies(self):
        dictionnaire_contraintes = {}
        for task in self.liste_taches:
            dependencies = set()
            #comparer la liste des reads de chaque tache avec la liste de writes des autres tache 
            #si la tache lit dans une variable qu une autre tache ecrit alors y'a forcement une dependances les deux "dependance"
            for task2 in self.liste_taches:
                if task2 != task:
                    if any(var in task2.writes for var in task.reads):
                        dependencies.add(task2.name)
            dictionnaire_contraintes[task.name] = list(dependencies)
       
        # Supprimer les redandances de dependances
        for dependencies in dictionnaire_contraintes.values():
            for dep_task in list(dependencies):
                if any(dep_task in dep_task2 for dep_task2 in dictionnaire_contraintes.values() if dependencies != dep_task2):
                    dependencies.remove(dep_task)
        return dictionnaire_contraintes

    #si la tache existe dans la liste de prefernece de precedance il l a recupere sinon il recupere les dependances dans le dictionnaire contraintes
    def getDependencies(self, nomTache):
        if nomTache in self.dictionnaire_contraintes:
            return self.dictionnaire_contraintes[nomTache]
        elif nomTache in self.precedence:
            return self.precedence[nomTache]
        else:
            return []

    def validateInputs(self):
        #vérifier les doublons
        task_names = {task.name for task in self.liste_taches} 
        #utiliser un ensemble qui contiendera les noms des taches et comparer la longeur de la liste et du set qui n accepte pas de doublons
        #si y a un doublons donc la longeur du set ssera plus petite "differente" de la longeur de la liste
        if len(self.liste_taches) != len(task_names):
            print("erreur les noms de tâches dupliqués")
            return False
        #Vérifier si le dictionnaire de précédence contient des noms de tâches qui n existent pas
        #recupere la liste des valeurs du dictionnaire et verifie que la dependance fait partie de la liste des taches d entrée 
        for dependencies in self.dictionnaire_contraintes.values():
            for dep in dependencies:
                if dep not in task_names:
                    print(f"erreur la tâche '{dep}' dans le dictionnaire de précédence n'existe pas")
                    return False
               
        return True

    def draw(self):
        G = nx.DiGraph()#pour creer le graphe
        taches = set(self.dictionnaire_contraintes.keys())
        taches.update(self.precedence.keys())
        
        for task in taches:#parcourir chaque tache et recuperer ses dependances
            dependencies = self.getDependencies(task)
            for dep_task in dependencies:
                G.add_edge(dep_task, task) #ajouter un arc dépendance à la tâche actuelle 
       
        if len(G) > 0:#verifier que le graphe n est pas vide
            nx.draw(G, with_labels=True, node_color='skyblue', node_size=2000, arrowsize=20)#dessiner le graphe
            plt.title("Graphe")#donner un titre
            plt.show()#affichage du graphe
        else:
            print("Le graphe est vide.")

    def runSeq(self):
        #implementer un dictionnaire comme reference de l etat des taches
        #aura comme clé les noms des taches et comme valeur une valeur booleene dectant si la tache est executé ou pas encore
        dictionnaire_etat = {task.name: False for task in self.liste_taches}
        for current_task in self.liste_taches:
                #si une tache n est pas encore executé alors elle doit etre executé
                if not dictionnaire_etat[current_task.name]:
                    #et pour l executer il faut bien verifier que les taches dont elle depend sont executé
                    #on recupere la liste des dependances de la tache avec getDependencies
                    dependencies = self.getDependencies(current_task.name)
                    #on verifie que toute les dependances ont été exécuté avec all qui retourne true seulement si toutes les dependances sont execute
                    #cad leurs valeurs dans etat_taches est a true
                    dependencies_completed = all(dictionnaire_etat[dep] for dep in dependencies)
                    #si les dependances sont toutes exécuté alors on a le droit d executer notre tache
                    if dependencies_completed:
                        current_task.run()
                        print(f"Tâche {current_task.name} exécutée")
                        dictionnaire_etat[current_task.name] = True #une fois executé l etat d execution change a true
 


    #Execution en parallele
    def run(self):
        #on utilise le meme principe d execution sequentiel un dictionnaire d etat
        dictionnaire_etat = {task.name: False for task in self.liste_taches}
        semaphore = threading.Semaphore(value=2)  # Limiter à 2 threads actifs simultanimant
        
        #on definie une fonction qu on utilisera pour executer une tache
        def execute_task(task):
            dependencies = self.getDependencies(task.name)
            # vérifier que dépendances pour la tâche actuelle sont executé
            verif_dependance = all(dictionnaire_etat[dep] for dep in dependencies)
            if verif_dependance:#si oui alore on peut l executer

                print("Début de l'exécution de la tâche", task.name)
                semaphore.acquire()# acquirire une sémaphore pour demarer l execution
                task.run()# exécute la tâche
                semaphore.release()# liberer semaphore
                dictionnaire_etat[task.name] = True
                print("Fin de l'exécution de la tâche", task.name)

         # tq toutes les taches sont pas execute continuer l execution
        while not all(dictionnaire_etat.values()):
            for current_task in self.liste_taches:
                 # si la tâche n est pas exécutée l executer
                if not dictionnaire_etat[current_task.name]:
                    execute_task(current_task)

        #création des threads pour exécuter les tâches de manière concurrente
        threads = []
        for current_task in self.liste_taches:
            # création d un thread pour chaque tâche avec la fonction execute_task comme cible
            thread = threading.Thread(target=execute_task, args=(current_task,))
            threads.append(thread)
            thread.start()# Démarrage du thread pour exécuter la tâche

        for thread in threads:
            thread.join() # attendre la fin de tous les threads


   

    def detTestRnd(self, nbrtests=10):
        for _ in range(nbrtests):
            random.seed()
            val_initiale = {var: random.randint(1, 100) for var in self.get_all_variables() if var in globals()}# Générer des valeurs initiales aléatoires pour les variables globales existantes
            self.run()
            # récupérer les valeurs des variables globales après l'exécution parallèle
            result_par = {var: globals()[var] for var in self.get_all_variables() if var in globals()}
            globals().update(val_initiale)  # restaurer les valeurs initiales des variables globales
            self.runSeq()
            # récupérer les valeurs des variables globales après l'exécution séquentielle
            result_seq = {var: globals()[var] for var in self.get_all_variables() if var in globals()}
            if result_par != result_seq: # Vérifier si les résultats des exécutions parallèle et séquentielle sont identiques
                return False
        return True


    def get_all_variables(self):# obtenir l'ensemble de toutes les variables lues et écrites par les tâches
        var = set()
        for task in self.liste_taches:
            var.update(task.reads)
            var.update(task.writes)
        return var

    def parCost(self, nbr_execution):
        total_seq_time = 0
        total_par_time = 0

        # Exécuter le système pour un certain nombre d'exécutions et récupérer les temps d'exécution
        for _ in range(nbr_execution):
            start_seq = time.time()  # Début d'exécution séquentielle
            self.runSeq()
            end_seq = time.time()  # Fin d'exécution séquentielle
            seq_t = end_seq - start_seq
            total_seq_time += seq_t

            start_par = time.time()  # Début d'exécution parallèle
            self.run()
            end_par = time.time()  # Fin d'exécution parallèle
            par_t = end_par - start_par
            total_par_time += par_t

            print(f"Exécution séquentielle : {seq_t:.6f} secondes")
            print(f"Exécution parallèle : {par_t:.6f} secondes")

        # Calculer les moyennes
        moy_seq = total_seq_time / nbr_execution
        moy_par = total_par_time / nbr_execution

        print(f"\nTemps moyen d'exécution séquentielle : {moy_seq:.6f} secondes")
        print(f"Temps moyen d'exécution parallèle : {moy_par:.6f} secondes")

        # Comparer les temps
        if moy_seq < moy_par:
            print("L'exécution séquentielle est plus rapide en moyenne.")
        elif moy_seq > moy_par:
            print("L'exécution parallèle est plus rapide en moyenne.")
        else:
            print("Les deux modes d'exécution ont des temps moyens identiques.")
