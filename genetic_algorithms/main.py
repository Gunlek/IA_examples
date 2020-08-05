import pygame, sys, os
from datetime import datetime
import random as rd

sys.path.append(os.path.abspath('.'))
from cell.cell import Cell

pygame.init()

screen_size = width, height = 720, 480

# Color definitions
bg_color = 10, 61, 98
fg_color = 250, 211, 144
target_color = 229, 80, 57
blue = 130, 204, 221

frame_cap = 30                        # Max FPS
physic_refresh_rate = 0.3             # Refresh rate for physic in seconds, can be float
display_refresh_rate = 1/frame_cap    # Refresh rate for screen in seconds, can be float

# Creation of initial cell
target_radius = 10
# target_cell = Cell(width / 2, height / 2, 10)
target_cell = Cell(rd.randrange(target_radius, width - target_radius), rd.randrange(target_radius, height - target_radius), 10)
print("Target position: ", target_cell.getPos())
target_cell.setColor(target_color)
# target_cell.enableFriction(True, 0.3)
# target_cell.addForce((1000, 0))

# Cell group, all cells must be in
cells = []
cells.append(target_cell)

screen = pygame.display.set_mode(screen_size)

# Store last update timestamp
last_physic_update = -1
last_display_update = -1

run = True

last_fps_print = -1
frame_count = 0

FPS_font = pygame.font.Font(None, 36)
FPS_text = FPS_font.render("FPS: --", 1, fg_color)
FPS_pos = FPS_text.get_rect(centerx=int(FPS_text.get_rect().size[0]/2))

while run:

    timestamp = datetime.now().timestamp()

    # Physic refresh
    if timestamp - last_physic_update >= physic_refresh_rate:
        for cell in cells:
            cell.updateFixed(physic_refresh_rate)
        last_physic_update = timestamp

    # Display refresh
    if timestamp - last_display_update >= display_refresh_rate:
        screen.fill(bg_color)

        for cell in cells:
            cell.update(display_refresh_rate)
            cell.draw(screen)

        screen.blit(FPS_text, FPS_pos)
        pygame.display.flip()

        frame_count += 1
        last_display_update = timestamp
    
    # FPS computing
    if timestamp - last_fps_print >= 1:
        FPS_text = FPS_font.render("FPS: " + str(frame_count), 1, fg_color)
        FPS_pos = FPS_text.get_rect(centerx=int(FPS_text.get_rect().size[0]/2))

        last_fps_print = timestamp
        frame_count = 0

    # Event handler
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            run = False
