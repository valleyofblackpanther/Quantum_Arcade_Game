import arcade
import qiskit
import numpy as np
from qiskit import QuantumCircuit, Aer, execute
from arcade.gui import UIManager, UIFlatButton

# Game settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Quantum Circuit Puzzle Game"

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()
        self.level = 1
        self.circuit = QuantumCircuit(1)
        self.target_state = '|1⟩'  # Target state for Level 1
        self.feedback = ""

    def setup(self):
        # Clear existing UI elements
        self.ui_manager.clear()

        # Add buttons for quantum gates
        x_button = UIFlatButton('X Gate', 200, 550, 100, 40, self.ui_manager)
        x_button.set_handler('on_click', self.on_x_gate_click)
        self.ui_manager.add(x_button)
    
        h_button = UIFlatButton('H Gate', 350, 550, 100, 40, self.ui_manager)
        h_button.set_handler('on_click', self.on_h_gate_click)
        self.ui_manager.add(h_button)
    
        check_button = UIFlatButton('Check Solution', 500, 550, 150, 40, self.ui_manager)
        check_button.set_handler('on_click', self.on_check_solution_click)
        self.ui_manager.add(check_button)

    def on_draw(self):
        arcade.start_render()
        # Display the current circuit
        arcade.draw_text(f"Level {self.level}: Apply gates to match {self.target_state}", 20, 500, arcade.color.WHITE, 20)
        arcade.draw_text(f"Circuit: {self.circuit}", 20, 450, arcade.color.WHITE, 20)
        arcade.draw_text(self.feedback, 20, 400, arcade.color.YELLOW, 20)

    def on_x_gate_click(self, event):
        self.circuit.x(0)
    
    def on_h_gate_click(self, event):
        self.circuit.h(0)
    
    def on_check_solution_click(self, event):
        # Simulate the circuit
        simulator = Aer.get_backend('statevector_simulator')
        result = execute(self.circuit, simulator).result()
        statevector = result.get_statevector()
        if self.level == 1 and np.isclose(statevector, [0, 1]).all():
            self.feedback = "Correct! You've matched the target state!"
            self.level_up()
        elif self.level == 2 and np.isclose(statevector, [1/np.sqrt(2), 1/np.sqrt(2)]).all():
            self.feedback = "Correct! You've created a superposition!"
            self.level_up()
        elif self.level == 3 and np.isclose(statevector, [1/np.sqrt(2), -1/np.sqrt(2)]).all():
            self.feedback = "Correct! You've achieved the |-⟩ state!"
            self.level_up()
        else:
            self.feedback = "Not quite right, try again!"

    def level_up(self):
        # Increase the level and reset the circuit
        self.level += 1
        self.circuit = QuantumCircuit(1)
        if self.level > 3:
            self.feedback = "Congratulations! You've completed all levels!"
            # Optionally, reset to level 1 or end the game

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = GameView()
    window.show_view(start_view)
    start_view.setup()
    arcade.run()

if __name__ == "__main__":
    main()