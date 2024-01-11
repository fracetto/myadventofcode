#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import sys

def getseq(filename):
    visited_lines : int = 0
    with open(filename, "r") as reffile:
        for line in reffile:
            result_ligne = [];
            if line.__len__() > 0:
                for car in line[0:]:
                    if car.isnumeric():
                        result_ligne.append(car)
                if result_ligne.__len__() > 0:
                    visited_lines+= int(result_ligne[0] + result_ligne[result_ligne.__len__()-1])
    reffile.close()
    # return la somme du premier et dernier chiffre dans chaque ligne du fichier 
    return visited_lines

s1 = getseq("fichierInput.txt")
print(f"Resultat :{s1}")