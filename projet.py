import graphviz as gv

class Automate:
    
    def __init__(self):
        self.alphabet = []
        self.etats = []
        self.etat_initial = []
        self.etats_finaux = []
        self.transitions = []
        
    def Automate(self, alphabet):
        self.alphabet = alphabet
        
    def ajouter_etat(self, id, est_initial=False, est_terminal=False) :
        self.etats.append(id)
        if est_initial:
            self.etat_initial.append(id)
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
        result += "Etats initiaux: " + str(sorted(self.etat_initial)) + "\n"
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
            if etat in self.etat_initial:
                initial = "__" + str(etat) + "__"
                dot.node(initial, shape='point')
                dot.node(str(etat), shape='circle')
                dot.edge(initial, str(etat))
            if etat in self.etats_finaux:
                dot.node(str(etat), shape='doublecircle')
            dot.node(str(etat), shape='circle')
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
        
        for etat in self.etat_initial:
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
        self.etat_initial = lines[2].split()
        self.etats_finaux = lines[3].split()
        
        for transition in lines[4:]:
            transition = transition.split()
            self.ajouter_transition(transition[0], transition[1], transition[2])
    
        
automate = Automate()
automate.charger("automate.txt")
# automate.Automate(['a', 'b', 'c', 'd'])
# automate.ajouter_etat('1', est_initial=True)
# automate.ajouter_etat('2')
# automate.ajouter_etat('3', est_terminal=True)
# automate.ajouter_etat('4')
# automate.ajouter_transition('1', 'a', '2')
# automate.ajouter_transition('1', 'b', '4')
# automate.ajouter_transition('2', 'a', '2')
# automate.ajouter_transition('2', 'b', '2')
# automate.ajouter_transition('2', 'c', '3')
# automate.ajouter_transition('2', 'd', '3')
# automate.ajouter_transition('4', 'c', '3')
# automate.ajouter_transition('4', 'd', '3')
automate.to_png()

# automate.sauvegarder("automate.txt")
