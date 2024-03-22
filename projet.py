import graphviz as gv

class Automate:
    '''Classe représentant un automate'''

    def __init__(self):
        '''Initialise un automate vide'''
        self.alphabet = []
        self.etats = []
        self.etats_initial = []
        self.etats_finaux = []
        self.transitions = []
        self.nb_trans = {}


    def Automate(self, alphabet):
        '''Défini l'alphabet de l'automate'''
        self.alphabet = alphabet


    def ajouter_etat(self, id, est_initial=False, est_terminal=False) :
        '''Ajoute un état à l'automate, est défini si il est initial ou terminal'''
        self.etats.append(id)
        if est_initial:
            self.etats_initial.append(id)
        if est_terminal:
            self.etats_finaux.append(id)
        self.nb_trans[id] = [0,0]


    def ajouter_initial(self, etat):
        '''Ajoute un état initial à l'automate'''
        if etat not in self.etats:
            self.ajouter_etat(etat, est_initial=True)
        elif etat not in self.etats_initial:
            self.etats_initial.append(etat)


    def ajouter_final(self, etat):
        '''Ajoute un état final à l'automate'''
        if etat not in self.etats:
            self.ajouter_etat(etat, est_terminal=True)
        elif etat not in self.etats_finaux:
            self.etats_finaux.append(etat)

            
    def supprimer_etat(self, etat):
        '''Supprime un état de l'automate'''
        if etat in self.etats:
            self.etats.remove(etat)
        if etat in self.etats_initial:
            self.etats_initial.remove(etat)
        if etat in self.etats_finaux:
            self.etats_finaux.remove(etat)
        for transition in self.transitions:
            if transition[0] == etat or transition[2] == etat:
                self.transitions.remove(transition)


    def ajouter_transition(self, source, symbole, destination):
        '''Ajoute une transition à l'automate, si la transition existe déjà, les symboles sont concaténés'''
        for transition in self.transitions:
            if transition[0] == source and transition[2] == destination:
                if symbole in transition[1]:
                    return
                else:
                    symbole = transition[1] + ', ' + symbole
                    self.transitions.remove(transition)
        self.transitions.append([source, symbole, destination])
        self.nb_trans[source][0] += 1
        self.nb_trans[destination][1] += 1


    def supprimer_transition(self, source, symbole, destination):
        '''Supprime une transition de l'automate'''
        for transition in self.transitions:
            if transition[0] == source and transition[1] == symbole and transition[2] == destination:
                self.transitions.remove(transition)
                self.nb_trans[source][0] -= 1
                self.nb_trans[destination][1] -= 1
            for etat in self.etats:
                if self.nb_trans[etat][1] == 0:
                    self.supprimer_etat(etat)


    def __str__(self):
        '''Retourne une représentation de l'automate sous forme de chaine de caractères'''
        result = "Alphabet: " + str(sorted(self.alphabet)) + "\n"
        result += "Etats: " + str(sorted(self.etats)) + "\n"
        result += "Etats initiaux: " + str(sorted(self.etats_initial)) + "\n"
        result += "Etats terminaux: " + str(sorted(self.etats_finaux)) + "\n"
        result += "Transitions:\n"
        for transition in self.transitions:
            result += f"{transition[0]} --({transition[1]})--> {transition[2]}\n"
        return result


    def demonte(self):
        '''Retourne une liste de transitions où chaque transition est décomposée en une transition par symbole de l'alphabet'''
        demonte = []
        for transition in self.transitions:
            if len(transition[1]) == 1:
                demonte.append(transition)
            else:
                for symbole in transition[1].split(', '):
                    demonte.append([transition[0], symbole, transition[2]])
        return demonte


    def to_dot(self):
        '''Retourne une représentation graphique de l'automate sous forme de graphe avec la librairie graphviz'''
        dot = gv.Digraph()
        dot.attr(rankdir='LR')
        for etat in self.etats:
            dot.node(str(etat), shape='circle')
            if etat in self.etats_initial:
                initial = "__" + str(etat) + "__"
                dot.node(initial, shape='point')
                dot.node(str(etat), shape='circle')
                dot.edge(initial, str(etat))
            if etat in self.etats_finaux:
                dot.node(str(etat), shape='doublecircle')
        for transition in self.transitions:
            dot.edge(str(transition[0]), str(transition[2]), label=transition[1], shape='circle')
        return dot


    def to_png(self, file_name):
        '''Retourne une représentation graphique de l'automate sous forme d'image au format png'''
        return self.to_dot().render(filename=file_name, format='png')


    def sauvegarder(self, file_name):
        '''Sauvegarde l'automate dans un fichier texte avec une structure prédéfinie'''
        txt = ""
        file = open(file_name, "w", encoding="UTF-8")

        for etat in self.etats:
            txt += etat + " "
        txt += "\n"

        for lettre in self.alphabet:
            txt += lettre + " "
        txt += "\n"

        for etat in self.etats_initial:
            txt += etat + " "
        txt += "\n"

        for etat in self.etats_finaux:
            txt += etat + " "
        txt += "\n"

        for transition in self.demonte():
            txt += transition[0] + " " + transition[1] + " " + transition[2] + "\n"

        file.write(txt)
        file.close()


    def reconstruire(self, etats):
        '''Permet de construire une liste d'états à partir d'une chaine de caractères'''
        L_etat = []
        i = 0
        while i < len(etats):
            if etats[i] == ' ' or etats[i] == '\n' or etats[i] == '\t':
                pass
            elif etats[i][0] == '(':
                multi_etat = '('
                while etats[i] != ')':
                    i += 1
                    multi_etat = multi_etat + etats[i]
                L_etat.append(multi_etat)
            else:    
                L_etat.append(etats[i])
            i += 1
        return L_etat


    def charger(self, file_name):
        '''Charge un automate depuis un fichier texte avec une structure prédéfinie'''
        file = open(file_name, "r", encoding="UTF-8")
        lines = file.readlines()
        file.close()

        etat = self.reconstruire(lines[0])
        for i in range(len(etat)):
            self.ajouter_etat(etat[i])

        self.alphabet = lines[1].split()

        initial = self.reconstruire(lines[2])
        for i in range(len(initial)):
            self.etats_initial.append(initial[i])

        final = self.reconstruire(lines[3])
        for i in range(len(final)):
            self.etats_finaux.append(final[i])

        for transition in lines[4:]:
            transition = self.reconstruire(transition)
            self.ajouter_transition(transition[0], transition[1], transition[2])


    def reset(self):
        '''Réinitialise l'automate'''
        self.alphabet = []
        self.etats = []
        self.etats_initial = []
        self.etats_finaux = []
        self.transitions = [] 
        
        
    def rec_transition(self, depart, arrivee, symbole):
        '''Retourne True et créé une transition si une transition est possible entre deux états, False sinon'''
        if depart == arrivee:
            return True
    
        for transition in self.transitions:
            if transition[1] == "ε" and transition[0] == depart:
                if self.rec_transition(transition[2], arrivee, symbole):
                    self.ajouter_transition(arrivee, symbole, depart)
                    return True
        return False


    def epsilon_cloture(self, symbole):
        '''Retourne la cloture transitive de l'automate'''
        suite = []
        for transition in self.transitions:
            if transition[1] == symbole:
                depart = transition[0]
                suite.append(transition[2])
                while suite:
                    for transition2 in self.transitions:
                        if transition2[0] == suite[0] and transition2[1] == "ε":
                            suite.append(transition2[2])
                        else:
                            self.ajouter_transition(depart, symbole, suite[0])
                    suite.pop(0)


    def epsilon_initial(self):
        '''Ajoute les états accessibles par epsilon aux états initiaux de l'automate'''
        for etat in self.etats_initial:
            for transition in self.transitions:
                if transition[0] == etat and transition[1] == "ε":
                    self.ajouter_initial(transition[2])


    def epsilon_supprimer(self):
        '''Supprime les transitions epsilon de l'automate'''
        for etat in self.etats:
            for etat2 in self.etats:
                for transition in self.transitions:
                    for transition2 in self.transitions:
                        if (transition[0] == etat and transition[1] != "ε" and transition[2] == etat2) and (transition2[0] == etat2 and transition2[1] == "ε" and transition2[2] == etat):
                            transition2[1] = transition[1]
        
        for transition in self.transitions:
            self.rec_transition(transition[2], transition[0], transition[1])
        
        suppresseur = []
        for transition in self.transitions:
            if transition[1] == "ε":
                suppresseur.append(transition)
        for transition in suppresseur:
            self.supprimer_transition(transition[0], transition[1], transition[2])


    def synchroniser(self):
        '''réalise la suppression des epsilons transitions de l'automate'''
        self.epsilon_cloture("ε")
        self.epsilon_initial()
        self.epsilon_supprimer()


    def completer(self):
        '''Complète l'automate pour qu'il soit complet'''
        self.ajouter_etat('puit')
        for etat in self.etats:
            possede = [transition[1] for transition in self.demonte() if transition[0] == etat]
            for symbole in self.alphabet:
                if symbole not in possede:
                    self.ajouter_transition(etat, symbole, 'puit')


    def supprimer_puit(self):
        '''Supprime l'état puit de l'automate'''
        if 'puit' in self.etats:
            while self.transitions[-1][2] == 'puit':
                self.transitions.pop()
            self.etats.remove('puit')


    def table_transition(self):
        '''Retourne la table de transition de l'automate'''
        table = {}
        for etat in self.etats:
            table[etat] = {}
            for symbole in self.alphabet:
                table[etat][symbole] = [' ']
            table[etat]['ε'] = [' ']
        for transition in self.demonte():
            if table[transition[0]][transition[1]][0] != ' ':
                table[transition[0]][transition[1]].append(transition[2])
            else:
                table[transition[0]][transition[1]][0] = transition[2]
        return table


    def afficher_table_transition(self):
        '''Affiche la table de transition de l'automate'''
        table = self.table_transition()
        alphabet = self.alphabet + ['ε']
        for etat in self.etats:
            print(etat, end=' ')
            if etat in self.etats_initial:
                print("I", end=' ')
            else:
                print(" ", end=' ')
            if etat in self.etats_finaux:
                print("F", end=' ')
            else:
                print(" ", end=' ')
            for symbole in alphabet:
                print(symbole, table[etat][symbole], end=' ')
            print()


    def est_deterministe(self):
        '''Retourne True si l'automate est déterministe, False sinon'''
        if len(self.etats_initial) > 1:
            return False
        table = self.table_transition()
        for etat in self.etats:
            for symbole in self.alphabet:
                if len(table[etat][symbole]) > 1:
                    return False
        return True


    def concatener(self, ceci):
        '''Retourne une chaine de caractères concaténée à partir d'une liste de caractères'''
        if len(ceci) > 1:
            ceci = '(' + ' - '.join(ceci) + ')'
        else:
            ceci = ceci[0]
        return ceci


    def determiniser(self):
        '''Retourne un automate déterministe équivalent à l'automate'''
        aut = Automate()
        self.supprimer_puit()
        self.synchroniser()
        aut.alphabet = self.alphabet
        etats_a_traiter = [self.etats_initial]
        etats_finaux = self.etats_finaux
        aut.ajouter_etat(self.etats_initial)

        while etats_a_traiter:
            for symbole in self.alphabet: 
                tour = []
                for transition in self.transitions:
                    if transition[0] in etats_a_traiter[0] and symbole in transition[1] and transition[2] not in tour:
                        tour.append(transition[2])

                for _ in range(len(tour)):
                    if tour not in etats_a_traiter:
                        etats_a_traiter.append(tour)
                        aut.ajouter_etat(tour)
                    if (etats_a_traiter[0], symbole, tour) not in aut.transitions:
                        aut.ajouter_transition(etats_a_traiter[0], symbole, tour)

            etats_a_traiter.pop(0)

        self.reset()
        self.alphabet = aut.alphabet

        initial = True
        for etat in aut.etats:
            terminal = False
            etat = aut.concatener(etat)
            for finaux in etats_finaux:
                if finaux in etat:
                    terminal = True
            self.ajouter_etat(etat, est_initial=initial, est_terminal=terminal)
            if initial:
                initial = False

        for transition in aut.transitions:
            transition[0] = aut.concatener(transition[0])
            transition[2] = aut.concatener(transition[2])            
            self.ajouter_transition(transition[0], transition[1], transition[2])





# debut des fonctions            

def copie(aut):
    '''Retourne une copie de l'automate passé en paramètre'''
    aut2 = Automate()
    aut2.alphabet = [lettre for lettre in aut.alphabet]
    aut2.etats = [etat for etat in aut.etats]
    aut2.etats_initial = [etat for etat in aut.etats_initial]
    aut2.etats_finaux = [etat for etat in aut.etats_finaux]
    aut2.transitions = [transition for transition in aut.transitions]
    return aut2


def union_automate(aut1, aut2):
    '''Retourne un automate qui est l'union des deux automates passés en paramètre'''
    aut3 = Automate()
    aut3 = copie(aut1)
    aut3.etats_initial = []
    aut3.ajouter_etat('0', est_initial=True)

    for lettre in aut2.alphabet:
        if lettre not in aut3.alphabet:
            aut3.alphabet.append(lettre)

    for etat in aut3.etats:
        if etat != '0':
            etat = str(int(etat) + 1)

    last_etat = str(int(aut1.etats[-1]) + 1)

    for etat in aut2.etats:
        aut3.ajouter_etat(str(int(etat) + int(last_etat)))

    for transition in aut2.transitions:
        aut3.ajouter_transition(str(int(transition[0]) + int(last_etat)), transition[1], str(int(transition[2]) + int(last_etat)))

    for etat in aut2.etats_finaux:
        aut3.etats_finaux.append(str(int(etat) + int(last_etat)))

    for etat in aut1.etats_initial:
        aut3.ajouter_transition('0', "ε", etat)
    for etat in aut2.etats_initial:
        aut3.ajouter_transition('0', "ε", str(int(etat) + int(last_etat)))

    return aut3


def concatenation_automate(aut1, aut2):
    '''Retourne un automate qui est la concaténation des deux automates passés en paramètre'''
    aut3 = Automate()
    last_etat = str(int(aut1.etats[-1]) + 1)
    aut3 = copie(aut1)

    for lettre in aut2.alphabet:
        if lettre not in aut3.alphabet:
            aut3.alphabet.append(lettre)

    aut3.ajouter_etat(last_etat)
    for etat in aut2.etats:
        aut3.etats.append(str(int(etat) + int(last_etat)))

    for transition in aut2.transitions:
        aut3.ajouter_transition(str(int(transition[0]) + int(last_etat)), transition[1], str(int(transition[2]) + int(last_etat)))

    aut3.etats_finaux = [str(int(etat) + int(last_etat)) for etat in aut2.etats_finaux]

    for etat in aut1.etats_finaux:
        aut3.ajouter_transition(etat, "ε", last_etat)
    for etat in aut2.etats_initial:
        aut3.ajouter_transition(last_etat, "ε", str(int(etat) + int(last_etat)))

    return aut3


def duplication_automate(aut):
    '''Retourne un automate qui est la duplication de l'automate passé en paramètre'''
    aut2 = Automate()
    aut2 = copie(aut)
    last_etat = str(int(aut.etats[-1]) + 1)

    aut2.ajouter_etat(last_etat, est_initial=True, est_terminal=True)

    for etat in aut.etats_finaux:
        aut2.ajouter_transition(etat, "ε", last_etat)
    for etat in aut.etats_initial:
        aut2.ajouter_transition(last_etat, "ε", etat)

    return aut2





# aut1 = Automate()
# aut1.charger("automate1.txt")
# aut2 = Automate()
# aut2.charger("automate2.txt")

# aut3 = concatenation_automate(aut1, aut2)
# aut3.sauvegarder("automate3.txt")
# aut3.to_png('aut3')

# aut5 = Automate()
# aut5.charger("automate5.txt")
# aut5.determiniser()
# aut5.to_png('aut5')

# aut4 = duplication_automate(aut5)
aut4 = Automate()
aut4.charger("automate4.txt")
aut4.synchroniser()
aut4.sauvegarder("automate4.txt")
aut4.to_png('aut4')

# aut6 = Automate()
# aut6.charger("automate6.txt")
# aut6 = union_automate(aut1, aut2)
# aut6.completer()
# aut6.determiniser()
# aut6.sauvegarder("automate6.txt")
# aut6.to_png('aut6')


# aut7 = Automate()
# aut7.charger("automate7.txt")
# aut7.determiniser()
# aut7.to_png('aut7')
# aut7.sauvegarder("automate7.txt")