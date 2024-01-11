#!/usr/bin/env python
#-*- coding: UTF-8 -*-
from dataclasses import dataclass
import collections

@dataclass(frozen=False,init=True)
class Cell:
    x:int
    y:int
    value:str
    is_peripheric:bool = None
    is_on_north_side:bool = None
    is_on_south_side:bool = None
    is_on_east_side:bool = None
    
    # if cell's peripheric then make offset control to avoid array bound of exception
    def _is_peripheric(self,board)->bool:
        return self.x == 1 or self.y == 1 or self.x == board.width or self.y == board.height
        
    def _is_on_north_side(self)->bool:
        return self.y == 1
    
    def _is_on_south_side(self,board)->bool:
        return self.y == board.height

    def _is_on_east_side(self,board)->bool:
        return self.x ==  board.width

    def _is_on_west_side(self)->bool:
        return self.x == 1
    
    def _get_coords(self) -> tuple:
        return (self.x,self.y)
    
    def _set_position(self,board):
        self.is_peripheric = self._is_peripheric(board)
        self.is_on_north_side = self._is_on_north_side()
        self.is_on_south_side = self._is_on_south_side(board)
        self.is_on_east_side = self._is_on_east_side(board)
        self.is_on_west_side = self._is_on_west_side()

    def _get_value(self)->str:
        return self.value

@dataclass(frozen=True,init=True)
class VectorNumber:
    origin:tuple
    digits:list[int]

    def _get_origin(self) -> tuple:
        return self.origin
    
    def _get_size(self) -> int:
        return self.digits.__len__()
        
    def _get_value_number(self) -> int:
        content = ""
        for digit in self.digits[0:]:
            content += str(digit)
        return int(content)

"""
parse les lignes du fichier d'imput 
pour construire une matrice de cellules
"""
@dataclass(frozen=False,init=True)
class Board:
    width:int
    height:int
    content:list[str]
    array_2d:dict
    array_numbers:dict

    # pour tous les nombres recuperation dans un dictionnaire des vecteurs de cellules
    # vecteur = { 
    #   origin,
    #   digits[] le nombre décomposé en chiffres int
    # }
    def _set_numbers_list(self,line,offset_height):
        if line.__len__() > 0:
            result_ligne = []
            origin_local = (1,offset_height)
            for offset_width in range(line.__len__()):
                char = line[offset_width]
                if char.isnumeric():
                    if result_ligne.__len__() == 0:
                        origin_local = (offset_width+1, offset_height)
                    result_ligne.append(int(char))
                elif (result_ligne.__len__() > 0):
                    vn = VectorNumber(digits=result_ligne.copy(),origin=origin_local)
                    self.array_numbers[vn._get_origin()] = vn
                    while (result_ligne.__len__() > 0):
                        result_ligne.pop()
                if char.isnumeric() and result_ligne.__len__() > 0:
                    # fin de ligne et numeric
                    #print(f"position fin ligne{char}")
                    vn = VectorNumber(digits=result_ligne.copy(),origin=origin_local)
                    self.array_numbers[vn._get_origin()] = vn

    # construction du board 
    def _init_board(self):
        offset_height = 1
        for line in self.content:
             self._set_board_line(offset_height,line)
             self._set_numbers_list(line,offset_height)
             offset_height += 1
    
    def _set_board_line(self, offset_height, line):
        offset_width = 1
        for char in line:
            cell = Cell(offset_width,offset_height,char)
            self.array_2d[cell._get_coords()] = cell
            offset_width +=1

    def _get_cell_on_board(self, cell_coords:tuple) -> Cell:
        return self.array_2d[cell_coords]

    def _get_adjacent_cells(self,cell:Cell)->list:
        result = []
        coords = cell._get_coords()
        # cherche si cell est sur un côté
        if cell.is_peripheric:
            if cell.is_on_east_side:
                # cherche si cell est sur un coin
                if cell.is_on_south_side:
                    # 3 adjacent_cells :
                    result.append(self._get_cell_on_board((coords[0],coords[1]-1)))
                    result.append(self._get_cell_on_board((coords[0]-1,coords[1])))
                    result.append(self._get_cell_on_board((coords[0]-1,coords[1]-1)))
                elif cell.is_on_north_side:
                    # 3 adjacent_cells :
                    result.append(self._get_cell_on_board((coords[0],coords[1]+1)))
                    result.append(self._get_cell_on_board((coords[0]-1,coords[1])))
                    result.append(self._get_cell_on_board((coords[0]-1,coords[1]+1)))
                # 5 adjacent_cells :
                else:
                    result.append(self._get_cell_on_board((coords[0],coords[1]+1)))
                    result.append(self._get_cell_on_board((coords[0],coords[1]-1)))
                    result.append(self._get_cell_on_board((coords[0]-1,coords[1])))
                    result.append(self._get_cell_on_board((coords[0]-1,coords[1]+1)))
                    result.append(self._get_cell_on_board((coords[0]-1,coords[1]-1)))
            elif cell.is_on_west_side:
                    # cherche si cell est sur un coin
                if cell.is_on_south_side:
                    # 3 adjacent_cells :
                    result.append(self._get_cell_on_board((coords[0]+1,coords[1])))
                    result.append(self._get_cell_on_board((coords[0],coords[1]-1)))
                    result.append(self._get_cell_on_board((coords[0]+1,coords[1]-1)))
                elif cell.is_on_north_side:
                    # 3 adjacent_cells :
                    result.append(self._get_cell_on_board((coords[0],coords[1]+1)))
                    result.append(self._get_cell_on_board((coords[0]+1,coords[1])))
                    result.append(self._get_cell_on_board((coords[0]+1,coords[1]+1)))
                # 5 adjacent_cells :
                else:
                    result.append(self._get_cell_on_board((coords[0],coords[1]+1)))
                    result.append(self._get_cell_on_board((coords[0],coords[1]-1)))
                    result.append(self._get_cell_on_board((coords[0]+1,coords[1])))
                    result.append(self._get_cell_on_board((coords[0]+1,coords[1]+1)))
                    result.append(self._get_cell_on_board((coords[0]+1,coords[1]-1)))
            elif cell.is_on_south_side:
                # 5 adjacent_cells :
                result.append(self._get_cell_on_board((coords[0]+1,coords[1])))
                result.append(self._get_cell_on_board((coords[0]-1,coords[1])))
                result.append(self._get_cell_on_board((coords[0]+1,coords[1]-1)))
                result.append(self._get_cell_on_board((coords[0],coords[1]-1)))
                result.append(self._get_cell_on_board((coords[0]-1,coords[1]-1)))
            elif cell.is_on_north_side:
                # 5 adjacent_cells :
                result.append(self._get_cell_on_board((coords[0]+1,coords[1])))
                result.append(self._get_cell_on_board((coords[0]-1,coords[1])))
                result.append(self._get_cell_on_board((coords[0]+1,coords[1]+1)))
                result.append(self._get_cell_on_board((coords[0],coords[1]+1)))
                result.append(self._get_cell_on_board((coords[0]-1,coords[1]+1)))
        else :
            # 8 adjacent_cells :
            result.append(self._get_cell_on_board((coords[0]+1,coords[1])))
            result.append(self._get_cell_on_board((coords[0]-1,coords[1])))
            result.append(self._get_cell_on_board((coords[0],coords[1]+1)))
            result.append(self._get_cell_on_board((coords[0]+1,coords[1]+1)))
            result.append(self._get_cell_on_board((coords[0]-1,coords[1]+1)))
            result.append(self._get_cell_on_board((coords[0]+1,coords[1]-1)))
            result.append(self._get_cell_on_board((coords[0],coords[1]-1)))
            result.append(self._get_cell_on_board((coords[0]-1,coords[1]-1)))
        return result

    def _get_board(self) -> dict:
        return self.array_2d
    
    def _print_board(self):
        for k,v in self._get_board().items():
            print(f"key {k} -> value {v}")

    def _get_numbers_list(self) -> dict:
        return self.array_numbers

    def _print_numbers_list(self):
        for k,v in self._get_numbers_list().items():
            print(f"key {k} -> value {v}")

def getseq(filename):
    with open(filename, "r") as reffile:
        content = reffile.read().splitlines()
        result = 0
        coords_symbol = {}
        # 1 parse le fichier 
        # permet de récupérer tous les nombres dans un dictionnaire avec 
        # un tableau qui contient les cellules constitutives du nombre
        line_lenght = content[0].__len__()
        board = Board(width=line_lenght, height=content.__len__(), content=content,array_2d={},array_numbers={})
        board._init_board()
        # 2 constuire la matrice des inputs sur le Board
        # cellule par cellule en stockant dans la cellule le caractère sur le board
        reffile.close()
        for origin, vector_number in board._get_numbers_list().items():
            cell_origin : Cell = board._get_cell_on_board(origin)
            cell_origin._set_position(board)
            adjacent_cells = board._get_adjacent_cells(cell_origin)
            if vector_number._get_size() > 1:
                for i in range(1,vector_number._get_size()):
                    cell_offset_x : Cell =   board._get_cell_on_board((origin[0]+i,origin[1]))
                    cell_offset_x._set_position(board)
                    adjacent_cell_vector = board._get_adjacent_cells(cell_offset_x)
                    #TODO optimisation pour eviter les doublons 
                    #adjacent_cells = list(set(adjacent_cells).union(set(adjacent_cell_vector)))    
                    adjacent_cells = list(adjacent_cells + adjacent_cell_vector)
            adjacent_cells_marked = False
            found_symbol = False
            while (not adjacent_cells_marked and not found_symbol):
                for adj_cell in adjacent_cells:
                    found_symbol = adj_cell.value == "*"
                    if found_symbol:
                        # stocker dans dico la position du symbol et le nombre associé
                        # dict {vector : coords_symbol(x,y)}
                        coords_symbol[vector_number._get_origin()] = adj_cell._get_coords()
                        break
                adjacent_cells_marked = True   
        coords_symbol_copy = coords_symbol.copy()
        for vector_origin,symbol_coords in coords_symbol.items():
                 # supprimer element à rechercher dans la copie 
                coords_symbol_copy.pop(vector_origin)
                # recherche un autre element en doublon avec dans voisinage immediat
                searched_doublon_list = list(coords_symbol_copy.values())
                if searched_doublon_list.__contains__(symbol_coords):
                    for vector_voisin, symbol_coords_value in coords_symbol_copy.items():
                        list_prox_vector = []
                        if symbol_coords_value == symbol_coords:
                            if abs(vector_voisin[1] - vector_origin[1]) <= 2 :
                                list_prox_vector.append((vector_origin,vector_voisin))
                        if list_prox_vector.__len__() == 1:
                            result+= board._get_numbers_list().get(list_prox_vector[0][0])._get_value_number()*board._get_numbers_list().get(list_prox_vector[0][1])._get_value_number()

        return result

s1 = getseq("fichierInput.txt")
print(f"Resultat :{s1}")