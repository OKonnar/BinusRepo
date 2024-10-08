# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 17:44:58 2024

@author: Loic_
"""

import sys
import time
import random
import os
from collections import namedtuple

MapElement = namedtuple('MapElement', ['character', 'battery_delta', 'message', 'weight'])

# Constants for map elements
HAZARD = MapElement("M", -2, "Hazard :(, you lost - 2 energy", 2)
NOTHING = MapElement(" ", -1, "Nothing...", 5)
BATTERY = MapElement("+", 1, "A battery ! + 1 energy", 2)
BOOSTER = MapElement("x", 2, "B-b-b-b-b-booooster kill ! + 2 energy", 1)
PLAYER = MapElement("P", 0, "", 0)
ERROR = MapElement(".", -1, "You hurt youself on wall !", 0)

class Map:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.map_data = self.generate_map()
        self.player_position = (int(width / 2), int(height / 2)) # cast to int to make sure

    def has_element(self, element_to_check):
        """
        Returns if the map has any given element
        """
        for value in self.map_data.values():
            if value == element_to_check:
                return True
        return False

    def move_player(self, direction): # tries to move the player and return the new tile underneath the players
        """
        Update the player position and returns the new tile underneath the player or error if it couldn't move'
        """
        x, y = self.player_position    
        if direction == "Up" and y > 0:
            y -= 1
        elif direction == "Down" and y < self.height - 1:
            y += 1
        elif direction == "Left" and x > 0:
            x -= 1
        elif direction == "Right" and x < self.width - 1:
            x += 1
        else:
            return ERROR
        self.player_position = (x, y) # update position
        tile_content = self.map_data.get(self.player_position) # store the data before overiding it
        if tile_content is not HAZARD:
            self.map_data[self.player_position] = NOTHING
        return tile_content # return tile data


    def generate_map(self):
        """
        Populate the map with elements and weights.
        """
        elements = [HAZARD, NOTHING, BATTERY, BOOSTER]
        map_dict = {}
        weights = [element.weight for element in elements]
        
        for x in range(self.width):
            for y in range(self.height):
                # Choose a map element based on weighted probabilities
                map_dict[(x, y)] = random.choices(elements, weights=weights, k=1)[0]
        return map_dict

    def display_map(self):
        """
        Prints out in terminal the current map.
        """
        print('\t ' + ('-' * self.width * 2))
        for y in range(self.height):
            row = '\t| '
            for x in range(self.width):
                # Check if the current position matches the player's position
                if (x, y) == self.player_position:
                    row += PLAYER.character + ' '  # If so, then print the player character ('P')
                else: # If it doesn't match then we simply print the character underneath
                    row += self.map_data[(x, y)].character + ' '
            print(row + '|')
        print('\t ' + ('-' * self.width * 2))
        print("")

class Robot:
    def __init__(self):
        self.batteries = 5
        self.max_batteries = 10

    def display_batteries(self):
        """
        Prints out in terminal the battery status of the player.
        """
        battery_bar = f"[ {'x ' * self.batteries}{'_ ' * (self.max_batteries - self.batteries)}]"
        battery_info = f" {self.batteries}/{self.max_batteries} Batteries"
        print(f"\n{battery_bar} {battery_info}\n")
        
    def update(self, tile_content):
        """
        Updates the robot data given the tile underneath.
        """
        self.batteries += tile_content.battery_delta
        self.batteries = max(0, min(self.batteries, self.max_batteries))
        game_log.push_log(tile_content.message)

class Log:
    def __init__(self):
        self.logs = []
        
    def push_log(self, new_log):
        self.logs.append(new_log)        
        
    def display_logs(self):
        for log in self.logs:
            print(log)
        self.logs.clear()

class Visualizer():
    def clear_display(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    
    def display(self):
        self.clear_display()
        time.sleep(0.1)
        game_robot.display_batteries()
        game_map.display_map()
        game_log.display_logs()


game_log = Log()
game_map = Map(5, 5)
game_visualizer = Visualizer()
game_robot = Robot()
keywords = ["Up", "Down", "Left", "Right"]
    
while (True):
    if not game_map.has_element(BATTERY) and not game_map.has_element(BOOSTER):
        print("You collected all of the batteries... YOU WIN !")
        break
    if game_robot.batteries == 0:
        print("You ran out of batteries... YOU LOST !")
        break
    game_visualizer.display()
    input_msg = input("Your Input: ").capitalize()
    if input_msg == "Quit":
        break
    if input_msg not in keywords: # simple error handling
        continue
    tile_content = game_map.move_player(input_msg.capitalize())
    game_robot.update(tile_content)



