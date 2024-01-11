#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import collections, sys
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

    def _is_good_set(self) -> bool:
            result = True
            for offset in range(self._list_length()) :
                if(self._get_offset(offset) != None):
                    datas = self._get_offset(offset).split(",")
                    i = 0
                    while(result and i < datas.__len__()) : 
                        color_dico = self._get_datas_in_content(datas[i])
                        result = self._valid_color_by_rules(color_dico[0],color_dico[1])
                        i=i+1
            return result
    
    def _valid_color_by_rules(self,col_value:int,color:str) -> bool:
        pattern = {"red" : 12, "green" : 13, "blue" : 14 }
        for k, v in pattern.items():
            if(color == k):
                return int(col_value) <= v
            
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
            if (e._list_length() > 0 and e._is_good_set()):
                result += e.nr
    reffile.close()
    return result

s1 = getseq("fichierInput.txt")
print(f"Resultat :{s1}")