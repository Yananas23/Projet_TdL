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
         
            
    def ajouter_transition(self, source, symbole, destination):
        '''Ajoute une transition à l'automate, si la transition existe déjà, les symboles sont concaténés'''
        for transition in self.transitions:
            if transition[0] == source and transition[2] == destination:
                if symbole in transition[1]:
                    return
                else:
                    symbole = transition[1] + ', ' + symbole
                    self.transitions.remove(transition)
        self.transitions.append((source, symbole, destination))
        
        
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
                    demonte.append((transition[0], symbole, transition[2]))
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
        file = open(file_name, "w")
        
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
                multi_etat = ''
                while etats[i] != ')':
                    multi_etat = multi_etat + etats[i]
                    i += 1
                L_etat.append(multi_etat)
            elif etats[i][0] == 'E':
                L_etat.append('Epsilon')
                i += 6
            else:
                L_etat.append(etats[i])
            i += 1
        return L_etat
 
    
    def charger(self, file_name):
        '''Charge un automate depuis un fichier texte avec une structure prédéfinie'''
        file = open(file_name, "r")
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
        for transition in self.demonte():
            if table[transition[0]][transition[1]][0] != ' ':
                table[transition[0]][transition[1]].append(transition[2])
            else:
                table[transition[0]][transition[1]][0] = transition[2]
        return table


    def afficher_table_transition(self):
        '''Affiche la table de transition de l'automate'''
        table = self.table_transition()
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
            for symbole in self.alphabet:
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


    def determiniser(self):
        '''Retourne un automate déterministe équivalent à l'automate'''
        aut = Automate()
        self.supprimer_puit()
        aut.alphabet = self.alphabet
        table = self.table_transition()
        print(table)
        # for t in table:
        #     print(t, end=' ')
        terminal = []
        etats_a_traiter = [self.etats_initial]
        if len(self.etats_initial) > 1:
            aut.ajouter_etat('(' + ' - '.join(self.etats_initial) +')', est_initial=True)
        else:
            aut.ajouter_etat(self.etats_initial[0], est_initial=True)
        
        while etats_a_traiter:
            for symbole in self.alphabet: 
                tour = []
                for etat in etats_a_traiter[0]:
                    if etat in self.etats_finaux and etats_a_traiter[0] not in terminal:
                        terminal.append(etats_a_traiter[0])
                    for i in range(len(table[etat][symbole])):
                        if table[etat][symbole][0] != ' ' and table[etat][symbole][i] not in tour:
                            tour.append(table[etat][symbole][i])

                for _ in range(len(tour)):
                    if tour not in etats_a_traiter:
                        etats_a_traiter.append(tour)

                    if len(etats_a_traiter[0]) > 1:
                        depart = '(' + ' - '.join(etats_a_traiter[0]) + ')'
                    else:
                        depart = etats_a_traiter[0][0]
                    if depart not in aut.etats:
                        aut.ajouter_etat(depart)

                    if len(tour) > 1:
                        arrive = '(' + ' - '.join(tour) + ')'
                    else:
                        arrive = tour[0]
                    if arrive not in aut.etats:
                        aut.ajouter_etat(arrive)

                    if (depart, symbole, arrive) not in aut.transitions:
                        aut.ajouter_transition(depart, symbole, arrive)
                        
            etats_a_traiter.pop(0)
            
        for etat in terminal:
            if len(etat) > 1:
                etat = '(' + ' - '.join(etat) + ')'
            else:
                etat = etat[0]
            if etat in aut.etats:
                aut.etats_finaux.append(etat)
        
        self.etats = aut.etats
        self.etats_initial = aut.etats_initial
        self.etats_finaux = aut.etats_finaux
        self.transitions = aut.transitions





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





aut1 = Automate()
aut1.charger("automate1.txt")
aut2 = Automate()
aut2.charger("automate2.txt")

aut3 = concatenation_automate(aut1, aut2)
# aut3.sauvegarder("automate3.txt")
aut3.to_png('aut3')

# aut5 = Automate()
# aut5.charger("automate5.txt")
# aut5.determiniser()
# aut5.to_png('aut5')

# aut4 = duplication_automate(aut5)
# aut4.sauvegarder("automate4.txt")
# aut4.to_png('aut4')

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