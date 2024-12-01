import pygame

class Maze:
    def __init__(self, screen_width=800, screen_height=600, cell_size=25):
        self.cell_size = cell_size
        self.cols = screen_width // cell_size  # Should be 32 for an 800-pixel width
        self.rows = screen_height // cell_size  # Should be 24 for a 600-pixel height
        
        self.walls = []
        self.pellets = []

        # Define a more complex layout that exactly fits 32 columns and 24 rows
        # This layout will fully occupy the screen dimensions
        self.layout = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
            [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 3, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 3, 3, 3, 3, 3, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 2, 1],
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
            [1, 1, 2, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1],
            [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]



        self.generate_maze()  # Generate walls and pellets based on layout

    def generate_maze(self):
        """
        Generate walls and pellets based on the layout.
        """
        self.pellets.clear()
        self.walls.clear()
        for row_idx, row in enumerate(self.layout):
            for col_idx, cell in enumerate(row):
                x = col_idx * self.cell_size
                y = row_idx * self.cell_size

                if cell == 1:  # Wall
                    self.walls.append(pygame.Rect(x, y, self.cell_size, self.cell_size))
                elif cell == 0:  # Pathway with normal pellet
                    pellet_x = x + self.cell_size // 2
                    pellet_y = y + self.cell_size // 2
                    self.pellets.append((pellet_x, pellet_y))
                elif cell == 2: # Super-pellet
                    pellet_x = x + self.cell_size // 2
                    pellet_y = y + self.cell_size // 2
                    self.pellets.append((pellet_x, pellet_y))

    def get_layout(self):
        """
        Return Maze layout array.
        """
        return self.layout

    def draw(self, screen):
        """
        Draw the maze onto the provided screen, including walls, normal pellets, and super-pellets.
        """
        # Draw all walls
        for wall in self.walls:
            pygame.draw.rect(screen, (0, 0, 255), wall)  # Blue walls

        # Draw all pellets
        for pellet in self.pellets:
            # Check if the pellet is a super-pellet (layout value = 2)
            col_idx = (pellet[0] - self.cell_size // 2) // self.cell_size
            row_idx = (pellet[1] - self.cell_size // 2) // self.cell_size

            if self.layout[row_idx][col_idx] == 2:
                # Draw a super-pellet (larger and distinct color)
                pygame.draw.circle(screen, (255, 0, 0), pellet, 8)  # Red, larger pellet
            else:
                # Draw a normal pellet
                pygame.draw.circle(screen, (255, 255, 0), pellet, 5)  # Yellow, smaller pellet


    def all_pellets_collected(self):
        """
        Check if all pellets have been collected.
        """
        return len(self.pellets) == 0
