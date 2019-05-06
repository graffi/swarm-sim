black = 1
gray = 2
red = 3
green = 4
blue = 5
yellow = 6
orange = 7
cyan = 8
violett = 9


def scenario(sim):
    draw_terrain(sim)

    # Particles TopLeft
    # sim.add_particle(-9.5, 11, color=blue)
    # sim.add_particle(-10, 10, color=black)
    # sim.add_particle(-9, 10, color=red)
    # sim.add_particle(-8.5, 11, color=green)
    # sim.add_particle(-10.5, 11, color=yellow)
    # sim.add_particle(-11, 10, color=violett)

    # Particles TopRight
    sim.add_particle(9.5, 11.0)
    sim.add_particle(10.5, 11.0)
    # sim.add_particle(11.0, 10.0)
    # sim.add_particle(10.0, 10.0)
    # sim.add_particle(10.5, 9.0)
    # sim.add_particle(9.0, 10.0)

    # Particles BottomLeft
    # sim.add_particle(-10.5, -11.0)
    # sim.add_particle(-9.5, -11.0)
    # sim.add_particle(-10.0, -10.0)
    # sim.add_particle(-11.0, -10.0)
    # sim.add_particle(-10.5, -9.0)
    # sim.add_particle(-9.0, -10.0)

    # Particles BottomRight
    # sim.add_particle(10.5, -11.0)
    # sim.add_particle(11.0, -10.0)
    # sim.add_particle(9.5, -11.0)
    # sim.add_particle(10.0, -10.0)
    # sim.add_particle(10.5, -9.0)
    # sim.add_particle(9.0, -10.0)

    # Particles Random1
    # sim.add_particle(-6.5, 5.0)
    # sim.add_particle(-7.0, 4.0)
    # sim.add_particle(-6.0, 4.0)
    # sim.add_particle(-5.5, 3.0)
    # sim.add_particle(-6.5, 3.0)
    # sim.add_particle(-6.0, 2.0)

    # Particles Random2
    # sim.add_particle(10.5, 1.0)
    # sim.add_particle(11.0, 0.0)
    # sim.add_particle(10.5, -1.0)
    # sim.add_particle(9.5, -1.0)
    # sim.add_particle(10.0, 0.0)
    # sim.add_particle(9.0, -0.0)


def draw_terrain(sim):
    # Left Border
    sim.add_location(-12, 12)
    sim.add_location(-11.5, 11)
    sim.add_location(-12, 10)
    sim.add_location(-11.5, 9)
    sim.add_location(-12, 8)
    sim.add_location(-11.5, 7)
    sim.add_location(-12, 6)
    sim.add_location(-11.5, 5)
    sim.add_location(-12, 4)
    sim.add_location(-11.5, 3)
    sim.add_location(-12, 2)
    sim.add_location(-11.5, 1)
    sim.add_location(-12, 0)
    sim.add_location(-12, -12)
    sim.add_location(-11.5, -11)
    sim.add_location(-12, -10)
    sim.add_location(-11.5, -9)
    sim.add_location(-12, -8)
    sim.add_location(-11.5, -7)
    sim.add_location(-12, -6)
    sim.add_location(-11.5, -5)
    sim.add_location(-12, -4)
    sim.add_location(-11.5, -3)
    sim.add_location(-12, -2)
    sim.add_location(-11.5, -1)

    # Right Border
    sim.add_location(12, 12)
    sim.add_location(11.5, 11)
    sim.add_location(12, 10)
    sim.add_location(11.5, 9)
    sim.add_location(12, 8)
    sim.add_location(11.5, 7)
    sim.add_location(12, 6)
    sim.add_location(11.5, 5)
    sim.add_location(12, 4)
    sim.add_location(11.5, 3)
    sim.add_location(12, 2)
    sim.add_location(11.5, 1)
    sim.add_location(12, 0)
    sim.add_location(12, -12)
    sim.add_location(11.5, -11)
    sim.add_location(12, -10)
    sim.add_location(11.5, -9)
    sim.add_location(12, -8)
    sim.add_location(11.5, -7)
    sim.add_location(12, -6)
    sim.add_location(11.5, -5)
    sim.add_location(12, -4)
    sim.add_location(11.5, -3)
    sim.add_location(12, -2)
    sim.add_location(11.5, -1)

    sim.add_location(-11.0, 12.0)
    sim.add_location(-10.0, 12.0)
    sim.add_location(-9.0, 12.0)
    sim.add_location(-8.0, 12.0)
    sim.add_location(-7.0, 12.0)
    sim.add_location(-6.0, 12.0)
    sim.add_location(-5.5, 11.0)
    sim.add_location(-5.0, 10.0)
    sim.add_location(-4.5, 9.0)
    sim.add_location(-4.0, 8.0)
    sim.add_location(-3.5, 7.0)
    sim.add_location(-3.0, 6.0)
    sim.add_location(-2.5, 5.0)
    sim.add_location(-2.0, 4.0)
    sim.add_location(-1.5, 3.0)
    sim.add_location(-1.0, 2.0)
    sim.add_location(-0.5, 1.0)
    sim.add_location(0.5, 1.0)
    sim.add_location(1.0, 2.0)
    sim.add_location(1.5, 3.0)
    sim.add_location(2.0, 4.0)
    sim.add_location(2.5, 5.0)
    sim.add_location(3.0, 6.0)
    sim.add_location(3.5, 7.0)
    sim.add_location(4.0, 8.0)
    sim.add_location(4.5, 9.0)
    sim.add_location(5.0, 10.0)
    sim.add_location(5.5, 11.0)
    sim.add_location(6.0, 12.0)
    sim.add_location(7.0, 12.0)
    sim.add_location(8.0, 12.0)
    sim.add_location(9.0, 12.0)
    sim.add_location(10.0, 12.0)
    sim.add_location(11.0, 12.0)
    sim.add_location(-11.0, -12.0)
    sim.add_location(-10.0, -12.0)
    sim.add_location(-9.0, -12.0)
    sim.add_location(-8.0, -12.0)
    sim.add_location(-7.0, -12.0)
    sim.add_location(-6.0, -12.0)
    sim.add_location(-5.5, -11.0)
    sim.add_location(-5.0, -10.0)
    sim.add_location(-4.5, -9.0)
    sim.add_location(-4.0, -8.0)
    sim.add_location(-3.5, -7.0)
    sim.add_location(-3.0, -6.0)
    sim.add_location(-2.5, -5.0)
    sim.add_location(-2.0, -4.0)
    sim.add_location(-1.5, -3.0)
    sim.add_location(-1.0, -2.0)
    sim.add_location(-0.5, -1.0)
    sim.add_location(0.5, -1.0)
    sim.add_location(1.0, -2.0)
    sim.add_location(1.5, -3.0)
    sim.add_location(2.0, -4.0)
    sim.add_location(2.5, -5.0)
    sim.add_location(3.0, -6.0)
    sim.add_location(3.5, -7.0)
    sim.add_location(4.0, -8.0)
    sim.add_location(4.5, -9.0)
    sim.add_location(5.0, -10.0)
    sim.add_location(5.5, -11.0)
    sim.add_location(6.0, -12.0)
    sim.add_location(7.0, -12.0)
    sim.add_location(8.0, -12.0)
    sim.add_location(9.0, -12.0)
    sim.add_location(10.0, -12.0)
    sim.add_location(11.0, -12.0)



