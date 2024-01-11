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

    """ return la somme des bornes
        inferieures par couleur et 
        pour le set en cours """
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

    def _set_degree_plus_one(self)->int:
            self.degree += 1

    def _set_degree_moins_one(self)->int:
            self.degree -= 1

    def _get_degree(self)->int:
         return self.degree

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


def _recurrent_algo(id,result:int,tour:AwkLikeLine,game_tour)->int:
        if (tour._my_numbers_list_length() > 0 and tour._win_numbers_list_length() > 0) :
            tour_val_recurrence = tour._get_winning_game()
            print(f"TOUR : id card {id} comporte {tour_val_recurrence} numeros gagnants")
            if tour_val_recurrence > 0:
                #le tour qui vient d'etre évalué comporte des numéros gagnants on les comptabilise
                result += tour_val_recurrence
                # on ajoute des degree autant qu'il y des numeros gagant 1 à chaque  Card (tour) située après dans le dico
                for i in range(tour_val_recurrence):
                    id_tour_next = int(id+i+1)
                    game_tour._get_line_by_id(id_tour_next)._set_degree_plus_one()
                    print(f"id card {id_tour_next} dont on augmente le degre de 1 et qui devient {game_tour._get_line_by_id(id_tour_next)._get_degree()}")
            if tour._get_degree() > 1 :
                tour._set_degree_moins_one()
                return _recurrent_algo(id,result,tour,game_tour)
            else :
                return result


def getseq(filename):
    with open(filename, "r") as reffile:
        content = reffile.read().splitlines()
        result = 0
        game_tour = FileLine(tour_dico={})
        for line in content:
            game = line.split(":")
            id_game = int(game[0].split()[1])
            game_usefull_datas = game[1]
            tour = AwkLikeLine(id=id_game, content=game_usefull_datas, degree=1)
            game_tour._add_line(tour)
        reffile.close()
        """
            tant que toutes les lignes ne sont pas lues
            appelle la fonction de calcul par recurrence 
        """
        for id,tour in game_tour._get_tour_dico().items():
            result+= _recurrent_algo(id,1,tour,game_tour)
        return result

sys.setrecursionlimit(4000)
s2 = sys.getrecursionlimit()
print(f"Resultat :{s2}")

s1 = getseq("fichierInput.txt")
print(f"Resultat :{s1}")