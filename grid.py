import pygame
import numpy as np
import sys
from playertile import Player_tile
from lifetile import Life_Tiles

class Grid:
    def __init__(self, width: int, height: int, grid_spacing: int) -> None:
        self._start_pygame = pygame.init()
        self.window = None
        self._width: int = width
        self._height: int = height
        self.width_counter: int = 0
        self.height_counter: int = 0
        self.life_grid_array = None
        self.grid_spacing: int = grid_spacing
        self._running = True
        self._mode_paused = True
        self.player_tile = Player_tile(self.grid_spacing, self._width, self._height)
        self.clock = pygame.time.Clock()
        self.life_tiles = None

    
    def _spawn_window(self):
        # This method handles the window configuration
        self.window = pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption("Welcome to the Grid")

    def _precalculate_grid(self):
        # This counts the grid before it's drawn and creates an array for other
        # classes to access
        # Also spawn in the class that will use the array once it's ready
        dead_space = self.grid_spacing * 2
        for y in range(dead_space, (self._height - dead_space) + 1):
            if y % self.grid_spacing == 0:
                self.height_counter += 1
        for x in range(dead_space, (self._width - dead_space) + 1):
            if x % self.grid_spacing == 0:
                self.width_counter += 1

        self.life_grid_array = np.zeros((self.width_counter, self.height_counter), dtype=int)
        
        # Create life tiles now that life_grid_array has been created
        self.life_tiles = Life_Tiles(self.life_grid_array, self.grid_spacing)  


    def _draw_grid(self):
        # This method provides the grid within the window
        # ensuring some dead space between the edges of the window 
        # and the edges of the grid
        dead_space: int = self.grid_spacing * 2
        LINE_WIDTH: int = 1

        for y in range(dead_space, (self._height - dead_space) + 1):
            if y % self.grid_spacing == 0:
                pygame.draw.line(self.window, (255,255,255), (dead_space, y), (self._width - dead_space, y), LINE_WIDTH)
        
        for x in range(dead_space, (self._width - dead_space) + 1):
            if x % self.grid_spacing == 0:
                pygame.draw.line(self.window, (255,255,255), (x, dead_space), (x, self._height - dead_space), LINE_WIDTH)

        
        


    def _handle_events(self):
        # This method handles events
        # Only letting the move player events happen
        # when the game is paused
        keys = pygame.key.get_pressed()   
        if self._mode_paused == True:
            if keys[pygame.K_LEFT]:
                self.player_tile.move(-self.grid_spacing, 0)
            if keys[pygame.K_RIGHT]:
                self.player_tile.move(self.grid_spacing, 0)
            if keys[pygame.K_UP]:
                self.player_tile.move(0, -self.grid_spacing)
            if keys[pygame.K_DOWN]:
                self.player_tile.move(0, self.grid_spacing)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Pause and unpause the game
                if event.key == pygame.K_SPACE:
                    if self._mode_paused == True:
                        self._mode_paused = False
                    elif self._mode_paused == False:
                        self._mode_paused = True
                # toggle life on and off on player square
                if self._mode_paused == True:
                    if event.key == pygame.K_LCTRL:
                        self.life_tiles.toggle_life(self.player_tile)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


    def _run(self):
        # This method firstly creates the window, then it
        # handles the event loop (key presses) and draws everything
        # to the window, over and over again in a loop
        self._spawn_window()
        self._precalculate_grid()

        while self._running:
            
            # Here is where key presses are handled
            self._handle_events()

            # Draw stuff to the window each frame
            # If game mode is paused, let the player be drawn and move around
            # If the game  is played let the life play out
            self.window.fill((0, 0, 0))
            self._draw_grid()
            if self._mode_paused == True:
                self.life_tiles.draw_life(self.window)
                self.player_tile.draw_player(self.window)
            if self._mode_paused == False:
                self.life_tiles.draw_life_living(self.window)
                
            
                
            
            pygame.display.flip()
            
            self.clock.tick(10)




        