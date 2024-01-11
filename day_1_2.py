#!/usr/bin/env python
import sys
#-*- coding: UTF-8 -*-

# TODO supprimer les print
# return la premiere occurrence qui est un chiffre depuis le début
def getseq_debut(line: str, pattern):
    debut_value : str
    concat_ligne : str = ""
    if line.__len__() > 0:
        for car in line[0:]:
            if car.isnumeric():
                debut_value = car
                print(f"debut value numeric --- {debut_value}")
                return debut_value
            else:
                concat_ligne+=car
                for k, v in pattern.items():
                    if(concat_ligne.find(k) > -1):
                        debut_value = v
                        print(f"debut value text --- {debut_value}")
                        return debut_value
                    
    
# TODO supprimer les print
#Recupere la derniere occurrence qui est un chiffre depuis la fin
def getseq_fin(line: str, pattern):
    fin_value : str
    concat_ligne : str = ""
    if line.__len__() > 0:
        #garde le même dictionnaire en parcourant depuis la fin
        for car in _reverse(line):
            if car.isnumeric():
                fin_value = car
                print(f"fin value numeric --- {fin_value}")
                return fin_value
            else:
                concat_ligne+=car
                for k, v in pattern.items():
                    #inverse la sequence pour comparer
                    reverse_line = _reverse(concat_ligne)
                    if(reverse_line.find(k) > -1):
                        fin_value = v
                        print(f"fin value text --- {fin_value}")
                        return fin_value
    

def _reverse(x):
  return x[::-1]


# TODO supprimer les print
def lines_matcher(filename):
    visited_lines : int = 0
    
    pattern = {"one" : "1", "two" : "2", "three" : "3", "four" : "4","five" : "5", "six" : "6", "seven" : "7" ,"eight" : "8", "nine" : "9"}
    with open(filename, "r") as reffile:
        for line in reffile:
            result_ligne = [];
            if line.__len__() > 0:
                first_digit = getseq_debut(line, pattern)
                if (first_digit != None):
                    result_ligne.append(first_digit)
                # optimisation on recherche la deuxieme SSI il y a au moins une occurrence
                if result_ligne.__len__() > 0:
                    last_digit = getseq_fin(line, pattern)
                    if (last_digit != None):
                        result_ligne.append(last_digit)
            # additionne SSI il y a 2 valeurs car l'algorithme nécessite 
            # analyse de la ligne 2 fois donc 2 valeurs sont stockées meême identiques (algo != day_1_1.py)
            if result_ligne.__len__() == 2:
                visited_lines+= int(result_ligne[0] + result_ligne[1])
                print(f"result : {result_ligne[0]} {result_ligne[1]}")
    reffile.close()
    return visited_lines


s1 = lines_matcher("fichierInput.txt")
print(f"Resultat :{s1}")