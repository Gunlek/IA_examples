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
cell_color = 120, 224, 143
best_color = 183, 21, 64
target_color = 229, 80, 57
blue = 130, 204, 221

frame_cap = 30                        # Max FPS
physic_refresh_rate = 0.3             # Refresh rate for physic in seconds, can be float
display_refresh_rate = 1/frame_cap    # Refresh rate for screen in seconds, can be float

# Creation of initial cell
target_radius = 10
target_cell = Cell(width / 2, height / 2, 10)
# target_cell = Cell(rd.randrange(target_radius, width - target_radius), rd.randrange(target_radius, height - target_radius), target_radius)
print("Target position: ", target_cell.getPos())
target_cell.setColor(target_color)
# target_cell.enableFriction(True, 0.3)
# target_cell.addForce((1000, 1000))

# Cell group, all cells must be in
cells = []

screen = pygame.display.set_mode(screen_size )

# Store last update timestamp
last_physic_update = -1
last_display_update = -1

run = True

last_fps_print = -1
frame_count = 0

FPS_font = pygame.font.Font(None, 36)
FPS_text = FPS_font.render("FPS: --", 1, fg_color)
FPS_pos = FPS_text.get_rect(centerx=int(FPS_text.get_rect().size[0]/2))

########################
## START OF ADDITIONS ##
########################
import math

min_force = -20
max_force = 40
mutation_probability = 0.3

def populate(n=10, m=10):
    new_cells = []
    forces = []
    for k in range(n):
        new = Cell(rd.randrange(target_radius, width - target_radius), rd.randrange(target_radius, height - target_radius), target_radius)
        new.setColor(cell_color)
        new_cells.append(new)
        force = []
        for i in range(m):
            force.append((rd.randrange(min_force, max_force), rd.randrange(min_force, max_force)))
        forces.append(force)
    
    return new_cells, forces

def apply_forces(force_index, forces, cells):
    for k in range(0, len(cells) - 1):
        force = forces[k][force_index]
        cells[k+1].addForce([force[0], force[1]])
    
    force_index += 1
    return force_index, cells

def merge(A, B):
    if A == []:
        return B
    elif B == []:
        return A
    elif A[0][1] <= B[0][1]:
        return [A[0]] + merge(A[1::], B)
    else:
        return [B[0]] + merge(A, B[1::])

def merge_sort(A):
    if len(A) <= 1:
        return A
    else:
        return merge(merge_sort(A[:len(A)//2]), merge_sort(A[len(A)//2:]))

def evaluate(cells, target, forces):
    dist_list = []
    for k in range(1, len(cells)):
        target_pos = target.getPos()
        cell_pos = cells[k].getPos()
        distance = math.sqrt((target_pos[0] - cell_pos[0])**2 + (target_pos[1] - cell_pos[1])**2)
        cells[k].setColor(cell_color)
        dist_list.append([cells[k], distance, forces])
    
    return dist_list

def avg(A, B):
    return ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)

def reproduce(distances):
    new_forces_list = []
    new_cells = []

    forces = distances[0][2]

    for k in range(0, len(distances)):
        new_cells.append(distances[k][0])
        new_forces_list.append(forces[k])

    for k in range(0, len(distances), 2):
        cell_1_forces = forces[k]
        cell_2_forces = forces[k+1]

        new_forces = []
        for i in range(len(cell_1_forces)):
            new_forces.append(avg(cell_1_forces[i], cell_2_forces[i]))
        
        cell = distances[k][0]
        new_forces_list.append(new_forces)
        new_cells.append(cell.copy())
    
    cell_1_forces = forces[0]
    cell_2_forces = forces[-1]
    new_forces = []
    for i in range(len(cell_1_forces)):
        new_forces.append(avg(cell_1_forces[i], cell_2_forces[i]))
    cell = distances[0][0]
    new_forces_list.append(new_forces)
    new_cells.append(cell)
    
    return new_cells, new_forces_list

def mutate(forces):
    for k in range(len(cells)):
        for i in range(len(forces[k])):
            if rd.random() <= mutation_probability:
                forces[k][i] = (rd.randrange(min_force, max_force), rd.randrange(min_force, max_force))
    return forces

population, forces = populate()
cells = [target_cell] + population
generation = 0
force_index = 0
force_refresh = 0.5
last_force_refresh = -1

######################
## END OF ADDITIONS ##
######################


while run:

    timestamp = datetime.now().timestamp()

    ########################
    ## START OF ADDITIONS ##
    ########################

    if timestamp - last_force_refresh >= force_refresh:
        force_index, cells = apply_forces(force_index, forces, cells)
        last_force_refresh = timestamp
    
    if force_index == len(forces[0]):
        distances = evaluate(cells, target_cell, forces)
        sort_dist = merge_sort(distances)
        sort_dist = sort_dist[:math.ceil(len(sort_dist)/2)]
        sort_dist[0][0].setColor(best_color)
        cells, forces = reproduce(sort_dist)
        forces = mutate(forces)

        for k in range(len(cells)):
            cells[k].reset()
        cells = [target_cell] + cells

        generation += 1
        force_index = 0

        print(forces[0])

        print("Génération: ", generation)

    ######################
    ## END OF ADDITIONS ##
    ######################

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
