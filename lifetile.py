import numpy as np
import pygame
from playertile import Player_tile



class Life_Tiles:
    def __init__(self, grid_array: np.array, grid_spacing: int) -> None:
        self.grid_array: np.array = grid_array
        self.grid_spacing: int = grid_spacing
        self._internal_grid_width: float = grid_spacing - 0.5
        self._internal_grid_height: float = grid_spacing - 0.5 
        self._dead_space: int = grid_spacing * 2
        self._life_colour: tuple[int, int, int] = (255, 255, 255)
        self._no_life_colour: tuple[int, int, int] = (0, 0, 0)
    
    def _update_grid(self):
        # Take one pass of the grid and update a copy of the grid based on what is found
        LIFE: int = 1
        NO_LIFE: int = 0
        new_grid: np.array = self.grid_array.copy()

        for row in range(len(self.grid_array) - 1):
            for column in range(len(self.grid_array[row]) - 1):
                adjacent_life_counter = self._count_live_neighbours(row, column)

                if self.grid_array[row, column] == LIFE:
                    if adjacent_life_counter < 2 or adjacent_life_counter > 3:
                        new_grid[row, column] = NO_LIFE
                elif self.grid_array[row, column] == NO_LIFE and adjacent_life_counter == 3:
                    new_grid[row, column] = LIFE

        self.grid_array = new_grid

    def _count_live_neighbours(self, row, column):
        # Look in adjacent rows for any living neighbours
        LIFE: int = 1
        adjacent_life_counter: int = 0

        for i in range(max(0, row - 1), min(row + 2, len(self.grid_array))):
            for j in range(max(0, column - 1), min(column + 2, len(self.grid_array[0]))):
                if (i != row or j != column) and self.grid_array[i, j] == LIFE:
                    adjacent_life_counter += 1

        return adjacent_life_counter                       
                        

    def draw_life_living(self, surface: pygame.Surface):
        # Play the rules for life and drawing the outcome of those rules to the window
        LIFE: int = 1
        NO_LIFE: int = 0
        self._update_grid()
        
        
        for row in range(len(self.grid_array) - 1):
            for column in range(len(self.grid_array[row]) - 1):
                if self.grid_array[row, column] == LIFE:
                    x_pos, y_pos = self._find_position_from_grid_array(row, column)
                    pygame.draw.rect(surface, self._life_colour, (x_pos, y_pos, self._internal_grid_width, self._internal_grid_height))
                elif self.grid_array[row, column] == NO_LIFE:
                    x_pos, y_pos = self._find_position_from_grid_array(row, column)
                    pygame.draw.rect(surface, self._no_life_colour, (x_pos, y_pos, self._internal_grid_width, self._internal_grid_height))
    

        

    def toggle_life(self, player_tile: Player_tile):
        # When the player presses the 'life' key, a new life is made at the players position
        # or if a life exists, it is killed
        player_tile.get_grid_position()
        self._life_array_update(player_tile.current_grid_x, player_tile.current_grid_y)

    def draw_life(self, surface: pygame.Surface):
        # Make sure that when life is "paused" that player can draw life and it's visible
        # also makes sure any current life on the screen remains visible when life is "paused"
        LIFE = 1
        NO_LIFE = 0
        for row in range(len(self.grid_array) - 1):
            for column in range(len(self.grid_array[row] - 1)):
                if self.grid_array[row, column] == LIFE:
                    # Passing waiting for find position array to be written
                    x_pos, y_pos = self._find_position_from_grid_array(row, column)
                    pygame.draw.rect(surface, self._life_colour, (x_pos, y_pos, self._internal_grid_width, self._internal_grid_height))
                elif self.grid_array[row, column] == NO_LIFE:
                    # Passing waiting for find position array to be written
                    x_pos, y_pos = self._find_position_from_grid_array(row, column)
                    pygame.draw.rect(surface, self._no_life_colour, (x_pos, y_pos, self._internal_grid_width, self._internal_grid_height))
                    

    def _find_position_from_grid_array(self, row, column):

        LINE_WIDTH: int = 1
        x_pos = (self._dead_space + LINE_WIDTH) + (self.grid_spacing * row)
        y_pos = (self._dead_space + LINE_WIDTH) + (self.grid_spacing * column)

        return x_pos, y_pos
       

    def _life_array_update(self, grid_x_pos: int, grid_y_pos: int):
        LIFE = 1
        NO_LIFE = 0
        if self.grid_array[grid_x_pos, grid_y_pos] == NO_LIFE:
            self.grid_array[grid_x_pos, grid_y_pos] = LIFE
        elif self.grid_array[grid_x_pos, grid_y_pos] == LIFE:
            self.grid_array[grid_x_pos, grid_y_pos] = NO_LIFE
