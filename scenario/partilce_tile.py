import copy
import random
E = 0
SE = 1
SW = 2
W = 3
NW = 4
NE = 5
S = 6  # S for stop and not south

direction = [E, SE, SW, W, NW, NE]

max=100
def scenario(sim):
    # sim.add_tile(0.0, 2.0)
    # sim.add_tile(3.0, 2.0)
    # sim.add_tile(0.5, 3.0)
    # sim.add_tile(1.5, 3.0)
    # sim.add_tile(2.5, 3.0)
    # sim.add_tile(3.5, 1.0)
    # sim.add_tile(3.0, 0.0)
    sim.add_tile(0.0, 0.0)
    #sim.add_tile(-0.5, 1.0)


    for i in range(0, max):
        x = random.randrange(-sim.get_sim_x_size(), sim.get_sim_x_size())
        y = random.randrange(-sim.get_sim_y_size(), sim.get_sim_y_size())
        if (x,y) not in sim.tile_map_coords:
            sim.add_particle(x, y)
        else:
            print (" x and y ", (x,y))
    print ("Max Size of created Particle", len(sim.particles))

    # sim.add_particle (1.0, 0.0)
    # sim.add_particle  (1.5, 1.0)
    # sim.add_particle  (2.0, 0.0)
    # sim.add_particle  (2.5, 1.0)
    # sim.add_particle  (3.0, -0.0)
    # # sim.add_particle  (3.5, 1.0)
    # sim.add_particle  (10.0, 20.0)
    # sim.add_particle(-10.0, 20.0)
    # sim.add_particle(-10.0, -20.0)
    # sim.add_particle(10.0, -20.0)
    #
    # sim.add_particle(10, 0.0)
    #
    # sim.add_particle(-10, 0.0)
    #
    # sim.add_particle(0, -20.0)
    # sim.add_particle(0, 20.0)

    # sim.add_particle(1.5, 1.0)
    # sim.add_particle(0.5, 1.0)
    # sim.add_particle(1.0, -0.0)
    # sim.add_particle(0.5, -1.0)
    # sim.add_particle(1.5, -1.0)
    # sim.add_particle(2.0, 0.0)
    # sim.add_particle(2.5, 1.0)
    # sim.add_particle(2.5, -1.0)
