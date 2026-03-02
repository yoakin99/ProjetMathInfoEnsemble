from itertools import combinations

class Ensemble:
    hashtable = {}

    def __init__(self, liste_element):
        self.hashtable = {}
        for e in liste_element:
            self.ajout_element(e)

    def __str__(self):
        return str(self.hashtable)
    
    def appartient(self, e):
        mod = hash(e) % 100
        if mod in self.hashtable:
            liste = self.hashtable[mod]
            return e in liste
        return False

    def ajout_element(self, e):
        if not self.appartient(e):
            mod = hash(e) % 100
            if mod in self.hashtable:
                self.hashtable[mod].append(e)
            else:
                self.hashtable[mod] = [e]

    def supprimer_element(self, e):
        if self.appartient(e):
            mod = hash(e) % 100
            self.hashtable[mod].remove(e)

    def union(self, ens):
        res = Ensemble([])
        for val in self.hashtable.values():
            for elem in val:
                res.ajout_element(elem)
        
        for val in ens.hashtable.values():
            for elem in val:
                res.ajout_element(elem)
        
        return res

    def intersection(self, ens):
        res = Ensemble([])
        for val in self.hashtable.values():
            for elem in val:
                if ens.appartient(elem):
                    res.ajout_element(elem)        
        return res
    
    def difference(self, ens):
        res = Ensemble([])
        for val in self.hashtable.values():
            for elem in val:
                if not ens.appartient(elem):
                    res.ajout_element(elem)

        for val in ens.hashtable.values():
            for elem in val:
                if not self.appartient(elem):
                    res.ajout_element(elem)             

        return res

    def egal(self, ens):
        if len(self.difference(ens).hashtable) == 0:
            return True
        return False

    def complementaire(self, reference):
        return self.difference(reference)

    def inclus(self, reference):
        for val in reference.hashtable.values():
            for elem in val:
                if not self.appartient(elem):
                    return False
        return True

    def compter(self):
        x = 0
        for val in self.hashtable.values():
            for elem in val:
                x += 1
        return x

    def ajout_ensemble(self, ens):
        somme = 0
        for val in self.hashtable.values():
            for elem in val:
                somme += elem
            somme = somme % 100
            if somme in self.hashtable:
                if ens.hashtable not in self.hashtable[somme]:
                    self.hashtable[somme].append(ens.hashtable)
            else:
                self.hashtable[somme] = [ens.hashtable]

    def parties(self):
        ens = Ensemble([])
        liste_valeurs = []
        for val in self.hashtable.values():
            liste_valeurs += val
        liste_combi = generer_combinaisons(liste_valeurs)
        for combi in liste_combi:
            sous_ensemble = Ensemble(combi)
            ens.ajout_element(sous_ensemble)
        return ens

def generer_combinaisons(liste):
    combinaisons = []
    for i in range(len(liste) + 1):
        combinaisons.extend(combinations(liste, i))
    return combinaisons

# Example usage
ens1 = Ensemble([0, 1, 2, 3])
ens2 = Ensemble([1, 2, 3])

print(ens1)
print(ens2)
print(ens2.inclus(ens1))

ens_un_element = Ensemble([5])
partie_un_element = ens_un_element.parties()
print("Ensemble avec un element:", ens_un_element)
print("Partie de l'ensemble avec un element:", partie_un_element)