#!/usr/bin/env python
#-*- coding: UTF-8 -*-
from dataclasses import dataclass

"""Class for keeping track line
 TODO sortir du fichier"""
@dataclass(frozen=True,init=True)
class AwkLikeLine: 
    content: str
    nr: int
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
    def _get_winning_game(self) -> list:
        # somme des max dans le set by colors
        winning_tour = []
        for offset in range(self._win_numbers_list_length()) :
            win_number = self._get_win_number_by_offset(offset)
            if(win_number != None):              
                for my_number in self._to_my_numbers():
                    if(my_number == win_number):
                        winning_tour.append(2)
        return winning_tour



def getseq(filename):
    with open(filename, "r") as reffile:
        content = reffile.read().splitlines()
        result = 0
        for line in content:
            game = line.split(":")
            id_game = int(game[0].split()[1])
            game_usefull_datas = game[1]
            tour = AwkLikeLine(nr=id_game, content=game_usefull_datas)
            result_temp = 0
            if (tour._my_numbers_list_length() > 0 and tour._win_numbers_list_length() > 0) :
                val_tour = tour._get_winning_game()
                if(val_tour.__len__() == 1):
                    result_temp +=1
                elif (val_tour.__len__() > 1):
                    result_temp +=1
                    for max in val_tour[1:]:
                        result_temp = result_temp * max
            result += result_temp
        reffile.close()
        return result

s1 = getseq("fichierInput.txt")
print(f"Resultat :{s1}")