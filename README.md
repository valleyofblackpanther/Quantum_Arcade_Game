# Quantum Arcade Game

This is a simple arcade game implemented in Python using the `arcade` library and `qiskit` to introduce a quantum computing element when a coin is collected.

## Description

In the game, the player controls a character that can shoot bullets towards the mouse click direction. The objective is to hit coins with the bullets to gain points. Upon hitting a coin, a simple quantum circuit is displayed in the console, showcasing the integration of quantum computing elements into the game.

## Features

- Player character that can shoot bullets towards the mouse click direction.
- Randomly placed coins that the player can shoot to gain points.
- Sound effects for shooting bullets and hitting coins.
- A simple quantum circuit displayed in the console each time a coin is collected.

## Usage

To play the game, navigate to the directory containing the game's script and run the following command:

```
python collecting_coins_quantum.py
```

## Controls

- Move the mouse to aim.
- Click the mouse to shoot a bullet in the direction of the pointer.

## Quantum Circuit

When a coin is collected, a simple quantum circuit is created and displayed using Qiskit. The circuit consists of Hadamard gates applied to three qubits followed by two CNOT gates.

#Output
[The Game](image_1.png)
[Quantum Gates](Image_2.png)
