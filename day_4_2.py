#!/usr/bin/env python
#-*- coding: UTF-8 -*-
from dataclasses import dataclass
import sys

"""Class for keeping track line
 TODO sortir du fichier"""
@dataclass(frozen=False,init=True)
class AwkLikeLine: 
    content: str
    id: int
    degree:int
    is_wining_card:bool = False
    level:int = 0

    def _set_winning_nummers_level(self)-> int:
        self.level = self._get_winning_game()
        if(self.level > 0):
             self._set_is_winning_card()

    def _to_win_numbers(self) -> list[int]:
        return self.content.split("|")[0].split()
    
    def _to_my_numbers(self) -> list[int]:
        return self.content.split("|")[1].split()

    def _get_my_number_by_offset(self,offset) -> str:
        return self._to_my_numbers().copy().pop(offset)
    
    def _get_win_number_by_offset(self,offset) -> str:
        return self._to_win_numbers().copy().pop(offset)
    
    def _my_numbers_list_length(self) -> int:
        return self._to_my_numbers().__len__()

    def _win_numbers_list_length(self) -> int:
        return self._to_win_numbers().__len__()

    """ 
        return la somme des bornes
        inferieures par couleur et 
        pour le set en cours
    """
    def _get_winning_game(self) -> int:
        # somme des max dans le set by colors
        winning_tour = 0
        for offset in range(self._win_numbers_list_length()) :
            win_number = self._get_win_number_by_offset(offset)
            if(win_number != None):              
                for my_number in self._to_my_numbers():
                    if(my_number == win_number):
                        winning_tour+=1
        return winning_tour

    def _set_degree_plus_one(self):
            self.degree += 1

    def _set_degree_moins_one(self):
            self.degree = self.degree - 1

    def _get_degree(self)->int:
         return self.degree
    
    def _set_is_winning_card(self):
        self.is_wining_card = True

    def _is_winning_card(self)->bool:
        return self.is_wining_card

"""Class for keeping track line
 TODO sortir du fichier"""
@dataclass(frozen=True,init=True)
class FileLine:
    tour_dico:dict
   
    def _get_tour_dico(self)->dict:
        return self.tour_dico

    def _get_line_by_id(self,id)->AwkLikeLine:
         return self.tour_dico[id]
    
    def _add_line(self,line:AwkLikeLine):
         self.tour_dico[line.id] = line


def _winning_card(id,result:int,tour:AwkLikeLine):
    tour._set_winning_nummers_level()
    if tour._is_winning_card():
        result += tour.level
    return result


def getseq(filename):
    with open(filename, "r") as reffile:
        content = reffile.read().splitlines()# parcorurs les instances
        game_tour = FileLine(tour_dico={})
        somme_degres_cartes_gangantes:int =0
        for line in content:
            game = line.split(":")
            id_game = int(game[0].split()[1])
            game_usefull_datas = game[1]
            tour = AwkLikeLine(id=id_game, content=game_usefull_datas, degree=1)
            game_tour._add_line(tour)
        reffile.close()
    for id,tour in game_tour._get_tour_dico().items():
        degree:int = tour._get_degree()
        while(degree >= 1):
            level :int = 0
            # parcours toutes les instances
            level = _winning_card(tour=tour,id=id,result=0)
                # on ajoute des degree autant qu'il y des numeros gagant 1 à chaque  Card (tour) située après dans le dico
            if(level > 0):
                for i in range(level):
                    id_tour_next = int(id+i+1)
                    game_tour._get_line_by_id(id_tour_next)._set_degree_plus_one()
            degree -=1
    # calcul du nombre de cartes gagnantes = ssomme des degres des cartes ganantes  
    for id,tour in game_tour._get_tour_dico().items():
        somme_degres_cartes_gangantes += tour._get_degree()
    return somme_degres_cartes_gangantes
"""
sys.setrecursionlimit(4000)
s2 = sys.getrecursionlimit()
print(f"Resultat :{s2}")
"""

s1 = getseq("fichierInput.txt")
print(f"Resultat :{s1}")