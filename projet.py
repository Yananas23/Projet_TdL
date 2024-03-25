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
        if id not in self.etats:
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
            if etat == transition[0] or etat == transition[2]:
                self.supprimer_transition(transition[0], transition[1], transition[2])


    def ajouter_transition(self, source, symbole, destination):
        '''Ajoute une transition à l'automate, si la transition existe déjà, les symboles sont concaténés'''
        if [source, symbole, destination] not in self.transitions:
            self.transitions.append([source, symbole, destination])
            self.nb_trans[source][0] += 1
            self.nb_trans[destination][1] += 1


    def supprimer_transition(self, source=None, symbole=None, destination=None):
        '''Supprime une transition de l'automate'''
        for transition in self.transitions:
            if source == None:
                if symbole == transition[1] and destination == transition[2]:
                    self.transitions.remove(transition)
                elif destination == transition[2]:
                    self.transitions.remove(transition)
                self.nb_trans[transition[0]][0] -= 1
                self.nb_trans[transition[2]][1] -= 1
            elif symbole == None:
                if source == transition[0] and destination == transition[2]:
                    self.transitions.remove(transition)
                elif destination == transition[2]:
                    self.transitions.remove(transition)
                self.nb_trans[transition[0]][0] -= 1
                self.nb_trans[transition[2]][1] -= 1
            elif destination == None:
                if source == transition[0] and symbole == transition[1]: 
                    self.transitions.remove(transition)
                elif source == transition[0]:
                    self.transitions.remove(transition)
                self.nb_trans[transition[0]][0] -= 1
                self.nb_trans[transition[2]][1] -= 1
            elif transition[0] == source and transition[1] == symbole and transition[2] == destination:
                self.transitions.remove(transition)
                self.nb_trans[transition[0]][0] -= 1
                self.nb_trans[transition[2]][1] -= 1


    def copie(self, aut):
        '''Retourne une copie de l'automate passé en paramètre'''
        self.alphabet = [lettre for lettre in aut.alphabet]
        self.etats = [etat for etat in aut.etats]
        self.etats_initial = [etat for etat in aut.etats_initial]
        self.etats_finaux = [etat for etat in aut.etats_finaux]
        self.transitions = [transition for transition in aut.transitions]


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


    def concatenation_transitions(self):
        '''Retourne une liste de transitions où chaque transition est concaténée en une transition par état de l'automate'''
        conca_trans = []
        for etat1 in self.etats:
            for etat2 in self.etats:  
                concac = []
                for transition in self.transitions:
                    if transition[0] == etat1 and transition[2] == etat2:
                        if transition[1] not in concac:
                            concac.append(transition[1])
                if len(concac) > 0:
                    symbole = ', '.join(concac)
                    conca_trans.append([etat1, symbole, etat2])
        return conca_trans


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
        for transition in self.concatenation_transitions():
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

        for transition in self.transitions:
            txt += transition[0] + " " + transition[1] + " " + transition[2] + "\n"

        file.write(txt)
        file.close()


    def reconstruire(self, etats):
        '''Permet de construire une liste d'états à partir d'une chaine de caractères'''
        L_etat = []
        i = 0
        etat = ''
        while i < len(etats):
            if etats[i] == '(':
                etat = '('
                while etats[i] != ')':
                    i += 1
                    etat += etats[i]
                L_etat.append(etat)
                etat = ''
            elif etats[i] not in ' \n\t':
                etat += etats[i]
            if etats[i] in ' \n\t' and etat != '':
                L_etat.append(etat)
                etat = ''
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


    def etats_accessibles(self):
        '''Retourne la liste des états accessibles depuis l'état initial'''
        etats_accessibles = set([self.etat_initial])
        etats_a_explorer = [self.etat_initial]

        while etats_a_explorer:
            etat = etats_a_explorer.pop(0)
            for transition in self.transitions:
                if transition[0] == etat and transition[1] != "ε":
                    if transition[2] not in etats_accessibles:
                        etats_accessibles.add(transition[2])
                        etats_a_explorer.append(transition[2])

        return list(etats_accessibles)


    def existe_chemin_vers_etat_final(self, etat):
        '''Retourne True s'il existe un chemin depuis l'état donné vers un état final, False sinon'''
        etats_a_explorer = [etat]
        etats_visites = []

        while etats_a_explorer:
            etat = etats_a_explorer.pop(0)
            if etat in etats_visites:
                continue
            etats_visites.append(etat)
            if etat in self.etats_finaux:
                return True
            for transition in self.transitions:
                if transition[0] == etat:
                    etats_a_explorer.append(transition[2])

        return False


    def epsilon_supprimer(self):
        '''Supprime les transitions epsilon de l'automate en appliquant la règle'''
        transitions_a_supprimer = []
        transitions_a_ajouter = []

        for transition in self.transitions:
            if transition[1] == "ε":
                p, q = transition[0], transition[2]
                for transition2 in self.transitions:
                    if transition2[2] == p and transition2[1] != "ε":
                        r, x = transition2[0], transition2[1]
                        transitions_a_ajouter.append((r, x, q))
                transitions_a_supprimer.append(transition)

        for transition in transitions_a_ajouter:
            self.ajouter_transition(transition[0], transition[1], transition[2])

        for transition in transitions_a_supprimer:
            self.supprimer_transition(transition[0], transition[1], transition[2])
            
        etats_finaux = self.etats_finaux
        etats_a_supprimer = []
        for etat in self.etats:
            if etat not in etats_finaux and not self.existe_chemin_vers_etat_final(etat):
                etats_a_supprimer.append(etat)
        for etat in etats_a_supprimer:
            self.supprimer_etat(etat)


    def synchroniser(self):
        '''réalise la suppression des epsilons transitions de l'automate'''
        self.epsilon_cloture("ε")
        self.epsilon_initial()
        self.epsilon_supprimer()


    def completer(self):
        '''Complète l'automate pour qu'il soit complet'''
        self.ajouter_etat('puit')
        for etat in self.etats:
            possede = [transition[1] for transition in self.transitions if transition[0] == etat]
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
        for transition in self.transitions:
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
        if len(ceci) > 1 and ceci[0] != '(':
            ceci = '(' + ' - '.join(ceci) + ')'
        elif len(ceci) > 1 and ceci[0] == '(':
            ceci = ceci
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
        already_done = []
        etats_finaux = self.etats_finaux
        aut.ajouter_etat(aut.concatener(self.etats_initial))

        while etats_a_traiter:
            for symbole in self.alphabet: 
                tour = []
                for transition in self.transitions:
                    if transition[0] in etats_a_traiter[0] and symbole in transition[1] and transition[2] not in tour:
                        tour.append(transition[2])

                for _ in range(len(tour)):
                    if tour not in etats_a_traiter:
                        if etats_a_traiter[0] not in already_done:
                            etats_a_traiter.append(tour)
                            aut.ajouter_etat(aut.concatener(tour))
                    if (etats_a_traiter[0], symbole, tour) not in aut.transitions:
                        depart = aut.concatener(etats_a_traiter[0])
                        arrivee = aut.concatener(tour)
                        aut.ajouter_transition(depart, symbole, arrivee)

            already_done.append(etats_a_traiter.pop(0))

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


    def find_index(self, lst, value):
        '''Retourne une liste des indexes où la valeur est présente dans la liste'''
        indexes = []
        for i, elem in enumerate(lst):
            if elem == value:
                indexes.append(i)
        return indexes


    def moore(self, partition):
        '''Realise l'algorithme de Moore pour minimiser l'automate'''
        while partition[0] != partition[-1]:
            for symbole in range(len(self.alphabet)):
                for etat in range(len(self.etats)):
                    for transition in self.transitions:
                        if transition[0] == self.etats[etat] and transition[1] == self.alphabet[symbole]:
                            partition[symbole + 1][etat] = partition[0][self.etats.index(transition[2])]

            diff_part = []
            diff = ''
            for etat in range(len(self.etats)):
                for part in range(len(partition) - 1):
                    diff = diff + partition[part][etat]
                diff_part.append(diff)
                diff = ''

            modified_indexes = [False] * len(partition[-1])
            refined = 'A'
            for part in diff_part:
                update_refine = False
                for i in self.find_index(diff_part, part):
                    if not modified_indexes[i]:
                        partition[-1][i] = refined
                        modified_indexes[i] = True
                        update_refine = True
                if update_refine:
                    refined = chr(ord(refined) + 1)

            if partition[0] == partition[-1]:
                return partition
            else: 
                partition[0] = partition[-1]
                partition[-1] = [0] * len(self.etats)


    def minimiser(self):
        '''Retourne un automate minimal équivalent à l'automate'''
        self.determiniser()
        self.completer()
        
        partition = [['A'] * len(self.etats) for _ in range(len(self.alphabet) + 2)]
        for i in range(len(self.etats)):
            if self.etats[i] in self.etats_finaux:
                partition[0][i] = 'B'
                
        self.moore(partition)
        aut = Automate()
        aut.alphabet = self.alphabet
        for i in range(len(partition[-1])):
            aut.ajouter_etat(partition[-1][i])
            if self.etats[i] in self.etats_initial:
                aut.ajouter_initial(partition[-1][i])
            if self.etats[i] in self.etats_finaux:
                aut.ajouter_final(partition[-1][i])
                
        for transition in self.transitions:
            aut.ajouter_transition(partition[-1][self.etats.index(transition[0])], transition[1], partition[-1][self.etats.index(transition[2])])
        
        self.reset()
        self.copie(aut)


    def accepte_mot(self, mot):
        '''Retourne True si le mot est accepté par l'automate, False sinon'''
        etat = self.etats_initial[0]
        for i in range(len(mot)):
            for transition in self.transitions:
                if transition[0] == etat and transition[1] == mot[i]:
                    if i < len(mot)-1 or i == len(mot)-1 and transition[2] in self.etats_finaux:
                        etat = transition[2]
                else:
                    return False
        return True


# debut des fonctions            
def union_automate(aut1, aut2):
    '''Retourne un automate qui est l'union des deux automates passés en paramètre'''
    aut3 = Automate()
    aut3.copie(aut1)
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
    aut3.copie(aut1)

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
    aut2.copie(aut)
    last_etat = str(int(aut.etats[-1]) + 1)

    aut2.ajouter_etat(last_etat, est_initial=True, est_terminal=True)

    for etat in aut.etats_finaux:
        aut2.ajouter_transition(etat, "ε", last_etat)
    for etat in aut.etats_initial:
        aut2.ajouter_transition(last_etat, "ε", etat)

    return aut2