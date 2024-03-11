import graphviz as gv

class Automate:
    
    def __init__(self, alphabet, etats, etat_initial, etats_finaux, transitions):
        self.alphabet = alphabet
        self.etats = etats
        self.etat_initial = etat_initial
        self.etats_finaux = etats_finaux
        self.transitions = transitions
        
    def ajouter_etat(self, id, est_initial=False, est_terminal=False) :
        self.etats.append(id)
        if est_initial:
            self.etat_initial.append(id)
        if est_terminal:
            self.etats_finaux.append(id)
            
    def ajouter_transition(self, source, symbole, destination):
        self.transitions.append((source, symbole, destination))
        
    def __str__(self):
        result = "Alphabet: " + str(sorted(self.alphabet)) + "\n"
        result += "Etats: " + str(sorted(self.etats)) + "\n"
        result += "Etats initiaux: " + str(sorted(self.etat_initial)) + "\n"
        result += "Etats terminaux: " + str(sorted(self.etats_finaux)) + "\n"
        result += "Transitions:\n"
        for transition in self.transitions:
            result += f"{transition[0]} --({transition[1]})--> {transition[2]}\n"
        return result
    
    def to_dot(self):
        dot = gv.Digraph(format='png')
        for etat in self.etats:
            if etat in self.etat_initial:
                dot.node(str(etat), shape='point')
            if etat in self.etats_finaux:
                dot.node(str(etat), shape='doublecircle')
            dot.node(str(etat))
        for transition in self.transitions:
            dot.edge(str(transition[0]), str(transition[2]), label=transition[1])
        return dot
    
    
        


test = Automate(['a', 'b'], [0, 1, 2], [0], [2], [(0, 'a', 1), (1, 'b', 2)])
test.to_dot()
print(test)