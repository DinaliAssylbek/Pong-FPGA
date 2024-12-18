# Pong Game for DE1-SoC
This repository contains the implementation of a Pong game designed for the DE1-SoC FPGA board. It was developed as part of the CS 3710 course at the University of Utah. The project showcases a hardware-based approach to game development, integrating CPU, RAM, and VGA display components.

![Screenshot 2024-12-18 154414](https://github.com/user-attachments/assets/1d259fe1-f5d9-480b-8d32-74c7f1eb04e1)

### Project Overview
The Pong game relies on three key components:
##### 1. Central Processing Unit (CPU)
- Executes CR-16 assembly code to manage game logic.
- Organized into three loops corresponding to the game states: intro, game, and game over.
- Calculates and updates paddle positions, ball position, game state, and scores.
##### 2. Memory
- Stores game data, including paddle/ball positions, scores, and game state.
- Implements a Verilog-based wrapper module for memory-mapped I/O functionality.
- Special memory addresses interact with controllers for player input.
##### 3. VGA Display
- Continuously reads specific memory locations to render the game.
- Updates the display to show paddle and ball positions, scores, and game states.

### Repository Structure
VGA Submodule: Contains the VGA display logic responsible for rendering the game visuals based on memory data.

CPU Submodule: Includes the CPU implementation that executes the assembly code and handles game logic.

Assembler Folder:Holds the Python-based assembler for CR-16 assembly code and the assembly code for the game.

### Memory Organization
The memory is divided into the following sections:
![image](https://github.com/user-attachments/assets/3cec1c7f-d727-4a05-be0c-66a872a2613b)

### SEGA Genesis Controller Integration
The game uses two SEGA Genesis controllers for input. The controllers are connected to the FPGA’s GPIO pins. The memory wrapper maps controller input to specific memory addresses, allowing the CPU to "read" inputs during each game loop.

![image](https://github.com/user-attachments/assets/286bdbb0-627c-42f7-bb58-ed16a34d6615)

### How It Works
- CPU: Reads inputs from the controllers and updates game elements in memory.
- Memory: Acts as an intermediary between the CPU and VGA. Includes special functionality for memory-mapped I/O.
- VGA: Continuously refreshes the screen based on memory data.
- Controllers: Provide real-time input for gameplay through memory-mapped addresses.

This structure enables smooth gameplay and efficient data management, recreating the classic Pong game on hardware.
