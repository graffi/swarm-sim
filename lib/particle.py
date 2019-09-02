"""
.. module:: particle
   :platform: Unix, Windows
   :synopsis: This module provides the interfaces of the robotics particle

.. moduleauthor:: Ahmad Reza Cheraghi

TODO: Erase Memory

"""

import logging, math
from lib import csv_generator, matter
from lib.header import *

particle_counter=0


class Particle(matter.Matter):
    """In the classe marker all the methods for the characterstic of a marker is included"""
    def __init__(self, world, x, y, color=black, alpha=1, particle_counter = particle_counter):
        """Initializing the marker constructor"""
        super().__init__( world, (x, y), color, alpha,
                          type="particle", mm_size=world.config_data.particle_mm_size)
        self.number = particle_counter
        self.__isCarried = False
        self.carried_tile = None
        self.carried_particle = None
        self.steps = 0
        self.csv_particle_writer = csv_generator.CsvParticleData( self.get_id(), self.number)

    def has_tile(self):
        if self.carried_tile == None:
            return False
        else:
            return True

    def has_particle(self):
        if self.carried_particle == None:
            return False
        else:
            return True

    def get_carried_status(self):
        """
        Get the status if it is taken or not

        :return: Tiles status
        """
        return self.__isCarried

    def check_on_tile(self):
        """
        Checks if the particle is on a tile

        :return: True: On a tile; False: Not on a Tile
        """
        if self.coords in self.world.tile_map_coords:
            return True
        else:
            return False

    def check_on_particle(self):
        """
        Checks if the particle is on a particle

        :return: True: On a particle; False: Not on a particle
        """
        if self.coords in self.world.particle_map_coords:
            return True
        else:
            return False

    def check_on_marker(self):
        """
        Checks if the particle is on a marker

        :return: True: On a marker; False: Not on a marker
        """
        if self.coords in self.world.marker_map_coords:
            return True
        else:
            return False

    def move_to(self, dir):
        """
        Moves the particle to the given direction

        :param dir: The direction must be either: E, SE, SW, W, NW, or NE
        :return: True: Success Moving;  False: Non moving
        """
        dir_coord = self.world.get_coords_in_dir(self.coords, dir)
        dir, dir_coord = self.check_within_border(dir, dir_coord)
        if check_coords(dir_coord[0], dir_coord[1]):

            if self.coords in self.world.particle_map_coords:
                del self.world.particle_map_coords[self.coords]

            if not dir_coord in self.world.particle_map_coords:
                self.coords = dir_coord
                self.world.particle_map_coords[self.coords] = self
                logging.info("particle %s successfully moved to %s", str(self.get_id()), dir)
                self.world.csv_round.update_metrics( steps=1)
                self.csv_particle_writer.write_particle(steps=1)
                self.touch()
                self.check_for_carried_tile_or_particle()
                return True
        return False

    def check_for_carried_tile_or_particle(self):
        if self.carried_tile is not None:
            self.carried_tile.coords = self.coords
            self.carried_tile.touch()
        elif self.carried_particle is not None:
            self.carried_particle.coords = self.coords
            self.carried_particle.touch()

    def check_within_border(self, dir, dir_coord):
        if self.world.config_data.border == 1 and \
                (abs(dir_coord[0]) > self.world.get_sim_x_size() or abs(dir_coord[1]) > self.world.get_sim_y_size()):
            dir = dir - 3 if dir > 2 else dir + 3
            dir_coord = self.world.get_coords_in_dir(self.coords, dir)
        return dir, dir_coord

    def move_to_in_bounds(self, dir):
        """
            Moves the particle to the given direction if it would remain in bounds.

            :param dir: The direction must be either: E, SE, SW, W, NW, or NE
            :return: True: Success Moving;  False: Non moving
        """
        dir_coord = self.world.get_coords_in_dir(self.coords, dir)
        sim_coord = coords_to_sim(dir_coord)
        if self.world.get_sim_x_size() >=  abs(sim_coord[0]) and \
                        self.world.get_sim_y_size() >=  abs(sim_coord[1]):
            return self.move_to(dir)
        else:
            # 'bounce' off the wall
            n_dir = dir - 3 if dir > 2 else dir + 3
            self.move_to(n_dir)

    def read_from_with(self, matter, key=None):
        """
        Read the memories from the matters (paricle, tile, or marker object) memories with a given keyword

        :param matter: The matter can be either a particle, tile, or marker
        :param key: A string keyword to searcg for the data in the memory
        :return: The matters memory; None
        """
        if key != None:
            tmp_memory = matter.read_memory_with(key)
        else:
            tmp_memory =  matter.read_whole_memory()

        if tmp_memory != None and len(tmp_memory) > 0 :
            if matter.type == "particle":
                self.world.csv_round.update_metrics( particle_read=1)
                self.csv_particle_writer.write_particle(particle_read=1)
            elif matter.type == "tile":
                self.world.csv_round.update_metrics( tile_read=1)
                self.csv_particle_writer.write_particle(tile_read=1)
            elif matter.type == "marker":
                self.world.csv_round.update_metrics( marker_read=1)
                self.csv_particle_writer.write_particle(marker_read=1)
            return tmp_memory
        else:
            return None

    def matter_in(self, dir=E):
        """
        :param dir: the direction to check if a matter is there
        :return: True: if a matter is there, False: if not
        """
        if  self.world.get_coords_in_dir(self.coords, dir) in self.world.get_tile_map_coords() \
            or self.world.get_coords_in_dir(self.coords, dir) in self.world.get_particle_map_coords() \
            or self.world.get_coords_in_dir(self.coords, dir) in self.world.get_marker_map_coords():
            return True
        else:
            return False

    def tile_in(self, dir=E):
        """
        :param dir: the direction to check if a tile is there
        :return: True: if a tile is there, False: if not
        """
        if self.world.get_coords_in_dir(self.coords, dir) in self.world.get_tile_map_coords():
            return True
        else:
            return False

    def particle_in(self, dir=E):
        """
        :param dir: the direction to check if a particle is there
        :return: True: if a particle is there, False: if not
        """
        if self.world.get_coords_in_dir(self.coords, dir) in self.world.get_particle_map_coords():
            return True
        else:
            return False

    def marker_in(self, dir=E):
        """
        :param dir: the direction to check if a marker is there
        :return: True: if a marker is there, False: if not
        """
        if self.world.get_coords_in_dir(self.coords, dir) in self.world.get_marker_map_coords():
            return True
        else:
            return False

    def get_matter_in(self, dir=E):
        if self.world.get_coords_in_dir(self.coords, dir) in self.world.get_tile_map_coords():
            return self.world.get_tile_map_coords()[self.world.get_coords_in_dir(self.coords, dir)]
        elif self.world.get_coords_in_dir(self.coords, dir) in self.world.get_particle_map_coords():
            return self.world.get_particle_map_coords()[self.world.get_coords_in_dir(self.coords, dir)]
        elif self.world.get_coords_in_dir(self.coords, dir) in self.world.get_marker_map_coords():
            return self.world.get_marker_map_coords()[self.world.get_coords_in_dir(self.coords, dir)]
        else:
            return False

    def get_tile_in(self, dir=E):
        if self.world.get_coords_in_dir(self.coords, dir) in self.world.get_tile_map_coords():
            return self.world.get_tile_map_coords()[self.world.get_coords_in_dir(self.coords, dir)]
        else:
            return False

    def get_particle_in(self, dir=E):
        if self.world.get_coords_in_dir(self.coords, dir) in self.world.get_particle_map_coords():
            return self.world.get_particle_map_coords()[self.world.get_coords_in_dir(self.coords, dir)]
        else:
            return False

    def get_marker_in(self, dir=E):
        if self.world.get_coords_in_dir(self.coords, dir) in self.world.get_marker_map_coords():
            return self.world.get_marker_map_coords()[self.world.get_coords_in_dir(self.coords, dir)]
        else:
            return False

    def get_marker(self):
        if self.coords in self.world.marker_map_coords:
            return self.world.get_marker_map_coords()[self.coords]
        else:
            return False

    def get_tile(self):
        if self.self.coords in self.world.get_tile_map_coords():
            return self.world.get_tile_map_coords()[self.coords]
        else:
            return False

    def write_to_with(self, matter, key=None, data=None):
        """
        Writes data with given a keyword directly on the matters (paricle, tile, or marker object) memory

        :param matter: The matter can be either a particle, tile, or marker
        :param key: A string keyword so to order the data that is written into the memory
        :param data: The data that should be stored into the memory
        :return: True: Successful written into the memory; False: Unsuccessful
        """
        wrote=False
        if data != None:
            wrote=False
            if key==None:
                wrote=matter.write_memory(data)
            else:
                wrote= matter.write_memory_with(key, data)
            if  wrote==True:
                if matter.type == "particle":
                    self.world.csv_round.update_metrics( particle_write=1)
                    self.csv_particle_writer.write_particle(particle_write=1)
                elif matter.type == "tile":
                    self.world.csv_round.update_metrics( tile_write=1)
                    self.csv_particle_writer.write_particle(tile_write=1)
                elif matter.type == "marker":
                    self.world.csv_round.update_metrics( marker_write=1)
                    self.csv_particle_writer.write_particle(marker_write=1)
                return True
            else:
                return False
        else:
            return False

    def scan_for_matters_within(self, matter='all', hop=1):
        """
        Scans for particles, tiles, or marker on a given hop distance and all the matters within the hop distance

        :todo: If nothing then everything should be scanned

        :param matter: For what matter this method should scan for. Can be either particles, tiles, markers, or (default)all
        :param hop: The hop distance from the actual position of the scanning particle
        :return: A list of the founded matters
        """

        within_hop_list = []
        for i in range(1, hop + 1):
            in_list = self.scan_for_matters_in(matter, i)
            if in_list is not None:
                within_hop_list.extend(in_list)
        if len(within_hop_list) != 0:
            return within_hop_list
        else:
            return None

    def scan_for_matters_in(self, matter='all', hop=1):
        """
         Scanning for particles, tiles, or marker on a given hop distance

         :param matter: For what matter this method should scan for. Can be either particles, tiles, markers, or (default)all
         :param hop: The hop distance from thee actual position of the scanning particle
         :return: A list of the founded matters
         """
        starting_x = self.coords[0]
        starting_y = self.coords[1]
        scanned_list = []
        logging.info("particle on %s is scanning for %s in %i hops", str(self.coords), matter, hop)

        if matter == "particles":
            scanned_list = scan(self.world.particle_map_coords, hop, starting_x, starting_y)
        elif matter == "tiles":
            scanned_list = scan(self.world.tile_map_coords, hop, starting_x, starting_y)
        elif matter == "markers":
            scanned_list = scan(self.world.marker_map_coords, hop, starting_x, starting_y)
        else:
            scanned_list = scan(self.world.particle_map_coords, hop, starting_x, starting_y)
            if scanned_list is not None:
                scanned_list.extend(scan(self.world.tile_map_coords, hop, starting_x, starting_y))
                scanned_list.extend(scan(self.world.marker_map_coords, hop, starting_x, starting_y))
            else:
                scanned_list = scan(self.world.tile_map_coords, hop, starting_x, starting_y)
                if scanned_list is not None:
                    scanned_list.extend(scan(self.world.marker_map_coords, hop, starting_x, starting_y))
                else:
                    scanned_list = scan(self.world.marker_map_coords, hop, starting_x, starting_y)
        if scanned_list is not None:
            return scanned_list
        else:
            return None

    def scan_for_particles_within(self, hop=1):
        """
        Scans for particles, tiles, or marker on a given hop distance and all the matters within the hop distance

        :todo: If nothing then everything should be scanned

        :param matter: For what matter this method should scan for. Can be either particles, tiles, markers, or (default)all
        :param hop: The hop distance from the actual position of the scanning particle
        :return: A list of the founded matters
        """

        within_hop_list = []
        for i in range(1, hop + 1):
            in_list = self.scan_for_particles_in(hop=i)
            if in_list is not None:
                within_hop_list.extend(in_list)
        if len(within_hop_list) != 0:
            return within_hop_list
        else:
            return None

    def scan_for_particles_in(self, hop=1):
        """
        Scanning for particles, tiles, or marker on a given hop distance

        :param matter: For what matter this method should scan for. Can be either particles, tiles, markers, or (default)all
        :param hop: The hop distance from thee actual position of the scanning particle
        :return: A list of the founded matters
        """

        scanned_list = self.scan_for_matters_in(matter='particles', hop=hop)
        return scanned_list

    def scan_for_tiles_within(self,  hop=1):
        """
        Scans for particles, tiles, or marker on a given hop distance and all the matters within the hop distance

        :todo: If nothing then everything should be scanned

        :param matter: For what matter this method should scan for. Can be either particles, tiles, markers, or (default)all
        :param hop: The hop distance from the actual position of the scanning particle
        :return: A list of the founded matters
        """

        within_hop_list = []
        for i in range(1, hop + 1):
            in_list = self.scan_for_tiles_in( hop=i)
            if in_list is not None:
                within_hop_list.extend(in_list)
        if len(within_hop_list) != 0:
            return within_hop_list
        else:
            return None

    def scan_for_tiles_in(self, hop=1):
        """
        Scanning for particles, tiles, or marker on a given hop distance

        :param matter: For what matter this method should scan for. Can be either particles, tiles, markers, or (default)all
        :param hop: The hop distance from thee actual position of the scanning particle
        :return: A list of the founded matters
        """
        scanned_list = self.scan_for_matters_in(matter='tiles', hop=hop)
        return scanned_list

    def scan_for_markers_within(self, hop=1):
        """
        Scans for particles, tiles, or marker on a given hop distance and all the matters within the hop distance

        :todo: If nothing then everything should be scanned

        :param matter: For what matter this method should scan for. Can be either particles, tiles, markers, or (default)all
        :param hop: The hop distance from the actual position of the scanning particle
        :return: A list of the founded matters
        """

        within_hop_list = []
        for i in range(1, hop + 1):
            in_list = self.scan_for_markers_in(hop=i)
            if in_list is not None:
                within_hop_list.extend(in_list)
        if len(within_hop_list) != 0:
            return within_hop_list
        else:
            return None

    def scan_for_markers_in(self, hop=1):
        """
        Scanning for particles, tiles, or marker on a given hop distance

        :param matter: For what matter this method should scan for. Can be either particles, tiles, markers, or (default)all
        :param hop: The hop distance from thee actual position of the scanning particle
        :return: A list of the founded matters
        """
        scanned_list = self.scan_for_matters_in(matter='markers', hop=hop)
        return scanned_list

    def take_me(self, coords=0):
        """
        The particle is getting taken from the the other particle on the given coordinate

        :param coords: Coordination of particle that should be taken
        :return: True: Successful taken; False: Cannot be taken or wrong Coordinates
        """

        if not self.__isCarried:
            if self.coords in self.world.particle_map_coords:
                del self.world.particle_map_coords[self.coords]
            self.__isCarried = True
            self.coords = coords
            self.set_alpha(0.5)
            self.touch()
            return True
        else:
            return False

    def drop_me(self, coords):
        """
        The actual particle is getting dropped

        :param coords: the given position
        :return: None
        """
        self.world.particle_map_coords[coords] = self
        self.coords = coords
        self.__isCarried = False
        self.set_alpha(1)
        self.touch()

    def create_tile(self, color=gray, alpha=1):
        """
        Creates a tile on the particles actual position

        :return: New Tile or False
        """
        logging.info("Going to create a tile on position %s", str(self.coords))
        new_tile = self.world.add_tile(self.coords[0], self.coords[1], color, alpha)
        if new_tile:
            self.world.tile_map_coords[self.coords[0], self.coords[1]].created = True
            self.csv_particle_writer.write_particle(tile_created=1)
            self.world.csv_round.update_tiles_num(len(self.world.get_tiles_list()))
            self.world.csv_round.update_metrics( tile_created=1)
            return new_tile
        else:
            return False

    def create_tile_in(self, dir=None, color=gray, alpha=1):
        """
        Creates a tile either in a given direction

        :param dir: The direction on which the tile should be created. Options: E, SE, SW, W, NW, NE,
        :return: New tile or False
        """
        logging.info("particle with id %s is", self.get_id())
        logging.info("Going to create a tile in %s ", str(dir) )
        if dir != None:
            coords = self.world.get_coords_in_dir(self.coords, dir)
            new_tile = self.world.add_tile(coords[0], coords[1], color, alpha)
            if new_tile:
                self.world.tile_map_coords[coords[0], coords[1]].created = True
                logging.info("Tile is created")
                self.world.new_tile_flag = True
                self.csv_particle_writer.write_particle(tile_created=1)
                self.world.csv_round.update_tiles_num(len(self.world.get_tiles_list()))
                self.world.csv_round.update_metrics( tile_created=1)
                return new_tile
            else:
                return False
        else:
            logging.info("Not created tile ")
            return False

    def create_tile_on(self, x=None, y=None, color=gray, alpha=1):
        """
        Creates a tile either on a given x,y coordinates

        :param x: x coordinate
        :param y: y coordinate
        :return: New Tile or False
        """

        logging.info("particle with id %s is", self.get_id())
        if x is not None and y is not None:
            coords = (x, y)
            if check_coords(x,y):
                logging.info("Going to create a tile on position \(%i , %i\)", x,y )
                if self.world.add_tile(coords[0], coords[1], color, alpha) == True:
                    self.world.tile_map_coords[coords[0], coords[1]].created = True
                    self.world.new_tile_flag = True
                    self.csv_particle_writer.write_particle(tile_created=1)
                    self.world.csv_round.update_tiles_num(len(self.world.get_tiles_list()) )
                    self.world.csv_round.update_metrics( tile_created=1)
                    return True
                else:
                    logging.info("Not created tile on coords  \(%i , %i\)", y,x )
                    return False
            else:
                logging.info("Not created tile on coords   \(%i , %i\)", y,x )
                return False

    def delete_tile(self):
        """
        Deletes a tile on current position

        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        logging.info("Particle %s is", self.get_id())
        logging.info("is going to delete a tile on current position")
        if self.coords in self.world.get_tile_map_coords():
            if self.world.remove_tile_on(self.coords):
                self.csv_particle_writer.write_particle(tile_deleted=1)
                return True
        else:
            logging.info("Could not delet tile")
            return False

    def delete_tile_with(self, id):
        """
        Deletes a tile with a given tile-id

        :param tile_id: The id of the tile that should be deleted
        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        logging.info("Particle %s is", self.get_id())
        logging.info("is going to delete a tile with tile id %s", str(id))
        if self.world.remove_tile(id):
            self.csv_particle_writer.write_particle(tile_deleted=1)
            return True
        else:
            logging.info("Could not delet tile with tile id %s", str(id))
            return False

    def delete_tile_in(self, dir=None):
        """
        Deletes a tile either in a given direction

        :param dir: The direction on which the tile should be deleted. Options: E, SE, SW, W, NW, NE,

        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        coords = ()
        if dir is not None:
            coords = self.world.get_coords_in_dir(self.coords, dir)
            logging.info("Deleting tile in %s direction", str(dir))
            if coords is not None:
                if self.world.remove_tile_on(coords):
                    logging.info("Deleted tile with tile on coords %s", str(coords))
                    self.csv_particle_writer.write_particle(tile_deleted=1)
                    return True
                else:
                    logging.info("Could not delet tile on coords %s", str(coords))
                    return False
        else:
            logging.info("Could not delet tile on coords %s", str(coords))
            return False

    def delete_tile_on(self, x=None, y=None):
        """
        Deletes a tile either on a given x,y coordinates
,
        :param x: x coordinate
        :param y: y coordinate
        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        coords = ()
        if x is not None and y is not None:
            coords = (x, y)
            if self.world.remove_tile_on(coords):
                logging.info("Deleted tile with tile on coords %s", str(coords))
                self.csv_particle_writer.write_particle(tile_deleted=1)
                return True
            else:
                logging.info("Could not delet tile on coords %s", str(coords))
                return False
        else:
            logging.info("Could not delet tile on coords %s", str(coords))
            return False

    def take_tile(self):
        """
        Takes a tile on the actual position

        :param id:  The id of the tile that should be taken
        :return: True: successful taken; False: unsuccessful taken
        """
        if self.carried_particle is None and self.carried_tile is None:
            if self.coords in self.world.tile_map_coords:
                self.carried_tile = self.world.tile_map_coords[self.coords]
                if self.carried_tile.take(coords=self.coords):
                    logging.info("Tile has been taken")
                    self.world.csv_round.update_metrics( tiles_taken=1)
                    self.csv_particle_writer.write_particle(tiles_taken=1)
                    return True
                else:
                    logging.info("Tile could not be taken")
                    return False
            else:
                logging.info("No tile on the actual position not in the world")
                return False
        else:
            logging.info("Tile cannot taken because particle is carrieng either a tile or a particle")
            return False

    def take_tile_with(self, id):
        """
        Takes a tile with a given tile id

        :param id:  The id of the tile that should be taken
        :return: True: successful taken; False: unsuccessful taken
        """
        if self.carried_particle is None and self.carried_tile is None:
            if id in self.world.tile_map_id:
                logging.info("Tile with tile id %s is in the world", str(id))
                self.carried_tile = self.world.tile_map_id[id]
                if self.carried_tile.take(coords=self.coords):
                    logging.info("Tile with tile id %s  has been taken", str(id))
                    self.world.csv_round.update_metrics( tiles_taken=1)
                    self.csv_particle_writer.write_particle(tiles_taken=1)
                    return True
                else:
                    logging.info("Tile with tile id %s could not be taken", str(id))
                    return False
            else:
                logging.info("Tile with tile id %s is not in the world", str(id))
                return False
        else:
            logging.info("Tile cannot taken because particle is carrieng either a tile or a particle", str(id))
            return False

    def take_tile_in(self, dir):
        """
        Takes a tile that is in a given direction

        :param dir: The direction on which the tile should be taken. Options: E, SE, SW, W, NW, NE,
        :return: True: successful taken; False: unsuccessful taken
        """
        if self.carried_particle is None and self.carried_tile is None:
            coords = self.world.get_coords_in_dir(self.coords, dir)
            if coords in self.world.tile_map_coords:
                self.carried_tile = self.world.tile_map_coords[coords]
                logging.info("Tile with tile id %s is in the world", str(self.carried_tile.get_id()))
                if self.carried_tile.take(coords=self.coords):
                    logging.info("Tile with tile id %s  has been taken", str(self.carried_tile.get_id()))
                    self.world.csv_round.update_metrics( tiles_taken=1)
                    self.csv_particle_writer.write_particle(tiles_taken=1)
                    return True
                else:
                    logging.info("Tile with tile id %s could not be taken", str(self.carried_tile.get_id()))
                    return False
            else:
                logging.info("Tile is not in the world")
                return False
        else:
            logging.info("Tile cannot taken because particle is carrieng either a tile or a particle")
            return False

    def take_tile_on(self, x=None, y=None):
        """
        Takes a tile that is in a given direction

        :param x: x coordinate
        :param y: y coordinate
        :return: True: successful taken; False: unsuccessful taken
        """
        if self.carried_particle is None and self.carried_tile is None:
            if check_coords(x, y):
                coords = (x, y)
                if coords in self.world.tile_map_coords:
                    self.carried_tile = self.world.tile_map_coords[coords]
                    logging.info("Tile with tile id %s is in the world", str(self.carried_tile.get_id()))
                    if self.carried_tile.take(coords=self.coords):
                        self.world.csv_round.update_metrics( tiles_taken=1)
                        self.csv_particle_writer.write_particle(tiles_taken=1)
                        logging.info("Tile with tile id %s  has been taken", str(self.carried_tile.get_id()))
                        return True
                    else:
                        logging.info("Tile with tile id %s could not be taken", str(self.carried_tile.get_id()))
                        return False
                else:
                    logging.info("Tile is not in the world")
                    return False
            else:
                logging.info("Coordinates are wrong")
                return False
        else:
            logging.info("Tile cannot taken because particle is carrieng either a tile or a particle")
            return False

    def drop_tile(self):
        """
        Drops the taken tile on the particles actual position

        :return: None
        """
        if self.carried_tile is not None:
            if self.coords not in self.world.tile_map_coords:
                try:  # cher: insert so to overcome the AttributeError
                    self.carried_tile.drop_me(self.coords)
                except AttributeError:
                    pass
                self.carried_tile = None
                logging.info("Tile has been dropped on the actual position")
                self.world.csv_round.update_metrics( tiles_dropped=1)
                self.csv_particle_writer.write_particle(tiles_dropped=1)
                return True
            else:
                logging.info("Is not possible to drop the tile on that position because it is occupied")
                return False
        else:
            return False

    def drop_tile_in(self, dir):
        """
        Drops the taken tile on a given direction

         :param dir: The direction on which the tile should be dropped. Options: E, SE, SW, W, NW, NE,
        """
        if self.carried_tile is not None:
            coords = self.world.get_coords_in_dir(self.coords, dir)
            if coords not in self.world.tile_map_coords:
                try:  # cher: insert so to overcome the AttributeError
                    self.carried_tile.drop_me(coords)
                except AttributeError:
                    pass
                self.carried_tile = None
                self.world.csv_round.update_metrics( tiles_dropped=1)
                self.csv_particle_writer.write_particle(tiles_dropped=1)
                logging.info("Dropped tile on %s coordinate", str(coords))
                return True
            else:
                logging.info("Is not possible to drop the tile on that position")
                return False

        else:
            logging.info("No tile taken for dropping")
            return False

    def drop_tile_on(self, x=None, y=None):
        """
        Drops the taken tile on a given direction

        :param x: x coordinate
        :param y: y coordinate
        """
        if self.carried_tile is not None:
            if check_coords(x, y):
                coords = (x, y)
                if coords not in self.world.get_tile_map_coords():
                    try:  # cher: insert so to overcome the AttributeError
                        self.carried_tile.drop_me(coords)
                    except AttributeError:
                        pass
                    self.carried_tile = None
                    self.world.csv_round.update_metrics( tiles_dropped=1)
                    self.csv_particle_writer.write_particle(tiles_dropped=1)
                    logging.info("Dropped tile on %s coordinate", str(coords))
                    return True
                else:
                    logging.info("Is not possible to drop the tile on that position because it is occupied")
                    return False
            else:
                logging.info("Wrong coordinates for dropping the tile")
                return False
        else:
            logging.info("No tile is taken for dropping")
            return False

    def create_particle(self, color=black, alpha=1):
        """
        Creates a particle on the particles actual position

        :return: New Particle or False
        """
        logging.info("Going to create on position %s", str(self.coords))
        new_particle = self.world.add_particle(self.coords[0], self.coords[1], color, alpha)
        if new_particle:
            self.world.particle_map_coords[self.coords[0], self.coords[1]].created=True
            self.csv_particle_writer.write_particle(particle_created=1)
            self.world.csv_round.update_particle_num(len(self.world.get_particle_list()))
            self.world.csv_round.update_metrics( particle_created=1)
            return new_particle
        else:
            return False

    def create_particle_in(self, dir=None, color=black, alpha=1):
        """
        Creates a particle either in a given direction

        :toDo: seperate the direction and coordinates and delete state

        :param dir: The direction on which the particle should be created. Options: E, SE, SW, W, NW, NE,
        :return: New Particle or False
        """
        coords = (0, 0)
        if dir is not None:
            coords = self.world.get_coords_in_dir(self.coords, dir)
            logging.info("Going to create a particle in %s on position %s", str(dir), str(coords))
            new_particle= self.world.add_particle(coords[0], coords[1], color, alpha)
            if new_particle:
                self.world.particle_map_coords[coords[0], coords[1]].created = True
                logging.info("Created particle on coords %s", coords)
                self.world.csv_round.update_particle_num(len(self.world.get_particle_list()))
                self.world.csv_round.update_metrics( particle_created=1)
                self.csv_particle_writer.write_particle(particle_created=1)
                return new_particle
            else:
                return False
        else:
            logging.info("Not created particle on coords %s", str(coords))
            return False

    def create_particle_on(self, x=None, y=None, color=black, alpha=1):
        """
        Creates a particle either on a given x,y coordinates

        :toDo: seperate the direction and coordinates and delete state

        :param x: x coordinate
        :param y: y coordinate
        :return: New Particle or False
        """
        coords = (0, 0)
        if x is not None and y is not None:
            if check_coords(x, y):
                coords = (x, y)
                logging.info("Going to create a particle on position %s", str(coords))
                new_particle = self.world.add_particle(coords[0], coords[1], color, alpha)
                if new_particle:
                    self.world.particle_map_coords[coords[0], coords[1]].created = True
                    logging.info("Created particle on coords %s", str(coords))
                    self.world.csv_round.update_particle_num(len(self.world.get_particle_list()))
                    self.world.csv_round.update_metrics( particle_created=1)
                    self.csv_particle_writer.write_particle(particle_created=1)
                    return new_particle
                else:
                    return False
            else:
                return False
        else:
            logging.info("Not created particle on coords %s", str(coords))
            return False

    def delete_particle(self):
        """
        Deletes a tile on current position

        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        logging.info("Particle %s is", self.get_id())
        logging.info("is going to delete a particle on current position")
        if self.coords in self.world.get_particle_map_coords():
            if self.world.remove_particle_on(self.coords):
                self.csv_particle_writer.write_particle(particle_deleted=1)
                return True
        else:
            logging.info("Could not delet particle")
            return False

    def delete_particle_with(self, id):
        """
        Deletes a particle with a given id

        :param id: The id of the particle that should be deleted
        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        logging.info("Particle %s is", self.get_id())
        logging.info("is going to delete a particle with id %s", str(id))
        if self.world.remove_particle(id):
            self.csv_particle_writer.write_particle(particle_deleted=1)
            return
        else:
            logging.info("Could not delet particle with particle id %s", str(id))

    def delete_particle_in(self, dir=None):
        """
        Deletes a particle either in a given direction

        :param dir: The direction on which the particle should be deleted. Options: E, SE, SW, W, NW, NE,
        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        if dir is not None:
            coords = self.world.get_coords_in_dir(self.coords, dir)
            logging.info("Deleting tile in %s direction", str(dir))
            if self.world.remove_particle_on(coords):
                logging.info("Deleted particle with particle on coords %s", str(coords))
                self.csv_particle_writer.write_particle(particle_deleted=1)
            else:
                logging.info("Could not delet particle on coords %s", str(coords))

    def delete_particle_on(self, x=None, y=None):
        """
        Deletes a particle either on a given x,y coordinates

        :param x: x coordinate
        :param y: y coordinate
        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        if x is not None and y is not None:
            if check_coords(x, y):
                coords = (x, y)
                if self.world.remove_particle_on(coords):
                    logging.info("Deleted particle with particle on coords %s", str(coords))
                    self.csv_particle_writer.write_particle(particle_deleted=1)
                    return True
                else:
                    logging.info("Could not delet particle on coords %s", str(coords))
                    return False
            else:
                return False
        else:
            return False

    def take_particle(self):
        """
        Takes a particle on the actual position

        :return: True: successful taken; False: unsuccessful taken
        """
        if self.carried_particle is None and self.carried_tile is None:
            if self.coords in self.world.particle_map_coords:
                self.carried_particle = self.world.particle_map_coords[self.coords]
                if self.carried_particle.take_me(coords=self.coords):
                    logging.info("particle has been taken")
                    self.world.csv_round.update_metrics( particles_taken=1)
                    self.csv_particle_writer.write_particle(particles_taken=1)
                    return True
                else:
                    logging.info("particle could not be taken")
                    return False
            else:
                logging.info("No particle on the actual position not in the world")
                return False
        else:
            logging.info("particle cannot taken because particle is carrieng either a particle or a particle")
            return False

    def take_particle_with(self, id):
        """
        Takes a particle with a given tile id

        :param id:  The id of the particle that should be taken
        :return: True: successful taken; False: unsuccessful taken
        """
        if self.carried_tile is None and self.carried_particle is None:
            if id in self.world.get_particle_map_id():
                logging.info("particle with particle id %s is in the world", str(id))
                self.carried_particle = self.world.particle_map_id[id]
                if self.carried_particle.take_me(self.coords):
                    logging.info("particle with particle id %s  has been taken", str(id))

                    self.world.csv_round.update_metrics(
                                                               particles_taken=1)
                    self.csv_particle_writer.write_particle(particles_taken=1)
                    return True
                else:
                    logging.info("particle with particle id %s could not be taken", str(id))
                    return False
            else:
                logging.info("particle with particle id %s is not in the world", str(id))
        else:
            logging.info("particle cannot taken because particle is carrieng either a particle or a particle", str(id))

    def take_particle_in(self, dir):
        """
        Takes a particle that is in a given direction

        :param dir: The direction on which the particle should be taken. Options: E, SE, SW, W, NW, NE,
        :return: True: successful taken; False: unsuccessful taken
        """
        if self.carried_tile is None and self.carried_particle is None:
            coords = self.world.get_coords_in_dir(self.coords, dir)
            if coords in self.world.particle_map_coords:
                logging.info("Take particle")
                self.carried_particle = self.world.particle_map_coords[coords]
                if self.carried_particle.take_me(coords=self.coords):
                    logging.info("particle with particle id %s  has been taken", str(self.carried_particle.get_id()))
                    self.world.csv_round.update_metrics(
                                                               particles_taken=1)
                    self.csv_particle_writer.write_particle(particles_taken=1)
                    return True
                else:
                    logging.info("particle could not be taken")
                    return False
            else:
                logging.info("particl is not in the world")
                return False
        else:
            logging.info("particle cannot be  taken")
            return False

    def take_particle_on(self, x=None, y=None):
        """
        Takes the particle on the given coordinate if it is not taken

        :param y:
        :param x:
        :return: True: Successful taken; False: Cannot be taken or wrong Coordinates
        """
        if self.carried_particle is None and self.carried_tile is None:
            if check_coords(x, y):
                coords = (x, y)
                if coords in self.world.particle_map_coords:
                    self.carried_particle = self.world.particle_map_coords[coords]
                    logging.info("Particle with id %s is in the world", str(self.carried_particle.get_id()))
                    if self.carried_particle.take_me(coords=self.coords):
                        self.world.csv_round.update_metrics( particles_taken=1)
                        self.csv_particle_writer.write_particle(particles_taken=1)
                        logging.info("particle with tile id %s has been taken", str(self.carried_particle.get_id()))
                        return True
                    else:
                        logging.info("Particle with id %s could not be taken", str(self.carried_particle.get_id()))
                        return False
                else:
                    logging.info("Particle is not in the world")
                    return False
            else:
                logging.info("Coordinates are wrong")
                return False
        else:
            logging.info("Particle cannot taken because particle is carrieng either a tile or a particle")
            return False

    def drop_particle(self):
        """
        Drops the taken particle on the particles actual position

        :return: None
        """
        if self.carried_particle is not None:
            if self.coords not in self.world.particle_map_coords:
                try:  # cher: insert so to overcome the AttributeError
                    self.carried_particle.drop_me(self.coords)
                except AttributeError:
                    logging.info("Dropped particle: Error while dropping")
                    return False
            self.carried_particle = None
            self.world.csv_round.update_metrics( particles_dropped=1)
            self.csv_particle_writer.write_particle(particles_dropped=1)
            logging.info("Particle succesfull dropped")
            return True
        else:
            logging.info("No particle taken to drop")
            return False

    def drop_particle_in(self, dir):
        """
        Drops the particle tile in a given direction

         :param dir: The direction on which the particle should be dropped. Options: E, SE, SW, W, NW, NE,
        """
        if self.carried_particle is not None:
            coords = self.world.get_coords_in_dir(self.coords, dir)
            if coords not in self.world.particle_map_coords:
                try:  # cher: insert so to overcome the AttributeError
                    self.carried_particle.drop_me(coords)
                except AttributeError:
                    logging.info("Dropped particle in: Error while dropping")
                    return False
                self.carried_particle = None
                logging.info("Dropped particle on %s coordinate", str(coords))
                self.world.csv_round.update_metrics( particles_dropped=1)
                self.csv_particle_writer.write_particle(particles_dropped=1)
                return True
            else:
                logging.info("Is not possible to drop the particle on that position because it is occupied")
                return False
        else:
            logging.info("No particle taken to drop")
            return False

    def drop_particle_on(self, x=None, y=None):
        """
        Drops the particle tile on a given x and y coordination

        :param x: x coordinate
        :param y: y coordinate
        """
        if self.carried_particle is not None and x is not None and y is not None and check_coords(x, y):
            coords = (x, y)
            if coords not in self.world.particle_map_coords:
                try:  # cher: insert so to overcome the AttributeError
                    self.carried_particle.drop_me(coords)
                except AttributeError:
                    logging.info("Dropped particle on: Error while dropping")
                    return False
                self.carried_particle = None
                logging.info("Dropped particle on %s coordinate", str(coords))
                self.world.csv_round.update_metrics(particles_dropped=1)
                self.csv_particle_writer.write_particle(particles_dropped=1)
                return True
            else:
                logging.info("Is not possible to drop the particle on that position  because it is occupied")
                return False
        else:
            logging.info("drop_particle_on: Wrong Inputs")
            return False

    def update_particle_coords(self, particle, new_coords):
        """
        Upadting the particle with new coordinates
        Only necessary for taking and moving particles

        :param particle: The particle object
        :param new_coords: new coorindation points
        :return: None
        """
        particle.coords = new_coords
        self.particle_map_coords[new_coords] = particle

    def create_marker(self, color=black, alpha=1):
        """
         Creates a marker on the particles actual position

        :return: New marker or False
        """

        logging.info("Going to create on position %s", str(self.coords))
        new_marker=self.world.add_marker(self.coords[0], self.coords[1], color, alpha)
        if new_marker != False:
            self.csv_particle_writer.write_particle(marker_created=1)
            self.world.csv_round.update_markers_num(len(self.world.get_marker_list()))
            self.world.csv_round.update_metrics( marker_created=1)
            return  new_marker
        else:
            return False

    def create_marker_in(self, dir=None, color=black, alpha=1):
        """
        Creates a marker either in a given direction
        :param dir: The direction on which the marker should be created. Options: E, SE, SW, W, NW, NE,
        :return: New marker or False

        """
        coords = (0, 0)
        if dir is not None:
            coords = self.world.get_coords_in_dir(self.coords, dir)
            logging.info("Going to create a marker in %s on position %s", str(dir), str(coords))
            new_marker = self.world.add_marker(coords[0], coords[1], color, alpha)
            if new_marker:
                logging.info("Created marker on coords %s", str(coords))
                self.world.csv_round.update_markers_num(len(self.world.get_marker_list()))
                self.world.csv_round.update_metrics( marker_created=1)
                return new_marker
            else:
                return False
        else:
            logging.info("Not created marker on coords %s", str(coords))
            return False

    def create_marker_on(self, x=None, y=None, color=black, alpha=1):
        """
        Creates a marker either on a given x,y coordinates

        :param x: x coordinate
        :param y: y coordinate
        :return: New marker or False

        """
        coords = (0, 0)
        if x is not None and y is not None:
            if check_coords(x, y):
                coords = (x, y)
                logging.info("Going to create a marker on position %s", str(coords))
                new_marker =  self.world.add_marker(coords[0], coords[1], color, alpha)
                if new_marker:
                    logging.info("Created marker on coords %s", str(coords))
                    self.world.csv_round.update_markers_num(len(self.world.get_marker_list()))
                    self.world.csv_round.update_metrics( marker_created=1)
                    return new_marker
            else:
                return False
        else:
            logging.info("Not created marker on coords %s", str(coords))
            return False

    def delete_marker(self):
        """
        Deletes a marker on current position

        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        logging.info("Particle %s is", self.get_id())
        logging.info("is going to delete a marker on current position")
        if self.coords in self.world.get_marker_map_coords():
            if self.world.remove_marker_on(self.coords):
                self.csv_particle_writer.write_particle(marker_deleted=1)
                return True
        else:
            logging.info("Could not delet marker")
            return False

    def delete_marker_with(self, marker_id):
        """
        Deletes a marker with a given marker-id

        :param marker_id: The id of the marker that should be deleted
        :return: True: Deleting successful; False: Deleting unsuccessful
        """

        logging.info("marker %s is", self.get_id())
        logging.info("is going to delete a marker with id %s", str(marker_id))
        if self.world.remove_marker(marker_id):
            self.csv_particle_writer.write_particle(marker_deleted=1)
            return
        else:
            logging.info("Could not delet marker with marker id %s", str(marker_id))

    def delete_marker_in(self, dir=None):
        """
        Deletes a marker either in a given direction or on a given x,y coordinates

        :param dir: The direction on which the marker should be deleted. Options: E, SE, SW, W, NW, NE,
        :param x: x coordinate
        :param y: y coordinate
        :return: True: Deleting successful; False: Deleting unsuccessful
        """

        if dir is not None:
            coords = self.world.get_coords_in_dir(self.coords, dir)
            logging.info("Deleting tile in %s direction", str(dir))
            if self.world.remove_marker_on(coords):
                logging.info("Deleted marker with marker on coords %s", str(coords))
                self.csv_particle_writer.write_particle(marker_deleted=1)
            else:
                logging.info("Could not delet marker on coords %s", str(coords))

    def delete_marker_on(self, x=None, y=None):
        """
        Deletes a particle either on a given x,y coordinates

        :param x: x coordinate
        :param y: y coordinate
        :return: True: Deleting successful; False: Deleting unsuccessful
        """
        if x is not None and y is not None:
            if check_coords(x, y):
                coords = (x, y)
                if self.world.remove_marker_on(coords):
                    logging.info("Deleted marker  oords %s", str(coords))
                    self.csv_particle_writer.write_particle(marker_deleted=1)
                    return True
                else:
                    logging.info("Could not delet marker on coords %s", str(coords))
                    return False
            else:
                return False
        else:
            return False

