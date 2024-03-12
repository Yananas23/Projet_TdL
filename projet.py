import graphviz as gv

class Automate:
    
    def __init__(self):
        self.alphabet = []
        self.etats = []
        self.etats_initial = []
        self.etats_finaux = []
        self.transitions = []
        
        
    def Automate(self, alphabet):
        self.alphabet = alphabet
        
        
    def ajouter_etat(self, id, est_initial=False, est_terminal=False) :
        self.etats.append(id)
        if est_initial:
            self.etats_initial.append(id)
        if est_terminal:
            self.etats_finaux.append(id)
         
            
    def ajouter_transition(self, source, symbole, destination):
        for transition in self.transitions:
            if transition[0] == source and transition[2] == destination:
                self.transitions.append((source, transition[1] + ', ' + symbole, destination))
                self.transitions.remove(transition)
                return
        self.transitions.append((source, symbole, destination))
        
        
    def __str__(self):
        result = "Alphabet: " + str(sorted(self.alphabet)) + "\n"
        result += "Etats: " + str(sorted(self.etats)) + "\n"
        result += "Etats initiaux: " + str(sorted(self.etats_initial)) + "\n"
        result += "Etats terminaux: " + str(sorted(self.etats_finaux)) + "\n"
        result += "Transitions:\n"
        for transition in self.transitions:
            result += f"{transition[0]} --({transition[1]})--> {transition[2]}\n"
        return result
    
    
    def demonte(self):
        demonte = []
        for transition in self.transitions:
            if len(transition[1]) == 1:
                demonte.append(transition)
            else:
                for symbole in transition[1].split(', '):
                    demonte.append((transition[0], symbole, transition[2]))
        return demonte
            
    
    def to_dot(self):
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
    
    def to_png(self):
        return self.to_dot().render(format='png')
    
    
    def sauvegarder(self, file_name):
        txt = ""
        file = open(file_name, "w")
        
        for lettre in self.alphabet:
            txt += lettre + " "
        txt += "\n"
        
        for etat in self.etats:
            txt += etat + " "
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
    
    
    def charger(self, file_name):
        file = open(file_name, "r")
        lines = file.readlines()
        file.close()
        
        self.alphabet = lines[0].split()
        self.etats = lines[1].split()
        self.etats_initial = lines[2].split()
        self.etats_finaux = lines[3].split()
        
        for transition in lines[4:]:
            transition = transition.split()
            self.ajouter_transition(transition[0], transition[1], transition[2])
            
         
# debut des fonctions            
            
def copie(aut):
    aut2 = Automate()
    aut2.alphabet = [lettre for lettre in aut.alphabet]
    aut2.etats = [etat for etat in aut.etats]
    aut2.etats_initial = [etat for etat in aut.etats_initial]
    aut2.etats_finaux = [etat for etat in aut.etats_finaux]
    aut2.transitions = [transition for transition in aut.transitions]
    return aut2


def union(aut1, aut2):
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
        
    aut3.etats_finaux = [str(int(etat) + int(last_etat)) for etat in aut2.etats_finaux]
    
    for etat in aut1.etats_initial:
        aut3.ajouter_transition('0', "epsilon", etat)
    for etat in aut2.etats_initial:
        aut3.ajouter_transition('0', "epsilon", str(int(etat) + int(last_etat)))
            
    return aut3


def concatenation(aut1, aut2):
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
        aut3.ajouter_transition(etat, "epsilon", last_etat)
    for etat in aut2.etat_initial:
        aut3.ajouter_transition(last_etat, "epsilon", str(int(etat) + int(last_etat)))
    
    return aut3


def duplication(aut):
    aut2 = Automate()
    aut2 = copie(aut)
    last_etat = str(int(aut.etats[-1]) + 1)
    
    aut2.ajouter_etat(last_etat, est_initial=True, est_terminal=True)
    
    for etat in aut.etats_finaux:
        aut2.ajouter_transition(etat, "epsilon", last_etat)
    for etat in aut.etat_initial:
        aut2.ajouter_transition(last_etat, "epsilon", etat)
  
    return aut2


aut1 = Automate()
aut1.charger("automate1.txt")
aut2 = Automate()
aut2.charger("automate2.txt")

# aut3 = concatenation(aut1, aut2)
# aut3.sauvegarder("automate3.txt")
# aut3.to_png()

# aut5 = Automate()
# aut5.charger("automate5.txt")
# aut4 = duplication(aut5)
# aut4.sauvegarder("automate4.txt")
# aut4.to_png()

aut6 = Automate()
aut6 = union(aut1, aut2)
aut6.sauvegarder("automate6.txt")
aut6.to_png()