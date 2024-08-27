import pygame
import numpy as np

class Player_tile: 
    def __init__(self, grid_spacing, window_width, window_height) -> None:
        self._grid_spacing: int = grid_spacing
        self._window_width: int = window_width
        self._window_height: int = window_height
        self.current_grid_x: int = 0
        self.current_grid_y: int = 0
        self._width: float = grid_spacing - 0.5
        self._height: float = grid_spacing - 0.5
        self.x_pos: int = (grid_spacing * 2 + 1)
        self.y_pos: int = (grid_spacing * 2 + 1)
        self._tile_colour: tuple[int, int, int] = (255, 0, 0)
    
    def draw_player(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self._tile_colour, (self.x_pos, self.y_pos, self._width, self._height))

    def move(self, dx: int, dy: int):

        dead_space = self._grid_spacing * 2
        new_x_pos = self.x_pos + dx
        new_y_pos = self.y_pos + dy

        # Check for boundaries and don't move beyond them
        if dead_space <= new_x_pos <= self._window_width - dead_space:
            self.x_pos = new_x_pos
        if dead_space <= new_y_pos <= self._window_height - dead_space:
            self.y_pos = new_y_pos

    def get_grid_position(self):
        dead_space = self._grid_spacing * 2

        self.current_grid_x = round((self.x_pos - dead_space) / self._grid_spacing)
        self.current_grid_y = round((self.y_pos - dead_space) / self._grid_spacing)
        
        