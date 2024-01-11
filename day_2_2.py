#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import math
from dataclasses import dataclass

"""
    parse les lignes du fichier d'imput 
    pour construire un dico dans lequel pour 
    chaque jeu on a les mains correspondantes 
    avec le nombre de cubes de chaque couleur
"""

# TODO supprimer les print
"""Class for keeping track line
 TODO sortir du fichier"""
@dataclass(frozen=True,init=True)
class AwkLikeLine: 
    content: str
    nr: int
    def _to_list(self) -> list[any]:
        return self.content.split(";")

    def _get_offset(self,offset) -> str:
        return self._to_list().copy().pop(offset)

    """ return la somme des bornes
        inferieures par couleur et 
        pour le set en cours """
    def _val_good_set(self) -> list:
        # somme des max dans le set by colors
        values_dico = {"red" : [], "green" : [], "blue" : []}
        max_by_colors = []
        for offset in range(self._list_length()) :
            if(self._get_offset(offset) != None):
                datas = self._get_offset(offset).split(",")
                i = 0
                while(i < datas.__len__()) :
                    color_dico = self._get_datas_in_content(datas[i])
                    self._collect_values_by_color(values_dico,color_dico[0],color_dico[1])
                    i=i+1
        for list_bycolor in values_dico.values():
            sorted_list_bycolor = sorted(list_bycolor, reverse=True)
            max_by_colors.append(sorted_list_bycolor[0])
        return max_by_colors
    
    def _collect_values_by_color(self,values_dico,col_value:int,color:str) -> dict:
        for k, v in values_dico.items():
            if(color == k):
                v.append(int(col_value))

    def _get_datas_in_content(self,datas:str) -> tuple:
        if(datas != None):
            data = datas.split()
        return (data[0], data[1])

    def _list_length(self) -> int:
        return self._to_list().__len__()

def getseq(filename):
    with open(filename, "r") as reffile:
        content = reffile.read().splitlines()
        result = 0
        for line in content:
            game = line.split(":")
            id_game = int(game[0].split()[1])
            game_usefull_datas = game[1]
            e = AwkLikeLine(nr=id_game, content=game_usefull_datas)
            if (e._list_length() > 0) :
                result_temp = 1
                val = e._val_good_set()
                for max in val:
                    result_temp = result_temp * max
                result += result_temp
        reffile.close()
        return result

s1 = getseq("fichierInput.txt")
print(f"Resultat :{s1}")