import arcade
import qiskit
from qiskit import QuantumCircuit, Aer, execute

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprites, Bullets, and Quantum Gates Example"

class QuantumGate:
    def __init__(self):
        self.circuit = QuantumCircuit(1)  # One qubit circuit

    def apply_hadamard(self):
        self.circuit.h(0)  # Apply Hadamard gate to qubit 0
        print("Hadamard gate applied. Circuit now:")
        print(self.circuit)

    def simulate(self):
        simulator = Aer.get_backend('statevector_simulator')
        result = execute(self.circuit, simulator).result()
        statevector = result.get_statevector()
        print("Current state vector:", statevector)

class EnemySprite(arcade.Sprite):
    """ Enemy ship class that tracks how long it has been since firing. """

    def __init__(self, image_file, scale, bullet_list, time_between_firing):
        super().__init__(image_file, scale)
        self.time_since_last_firing = 0.0
        self.time_between_firing = time_between_firing
        self.bullet_list = bullet_list

    def on_update(self, delta_time: float = 1 / 60):
        self.time_since_last_firing += delta_time
        if self.time_since_last_firing >= self.time_between_firing:
            self.time_since_last_firing = 0
            bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png")
            bullet.center_x = self.center_x
            bullet.angle = -90
            bullet.top = self.bottom
            bullet.change_y = -2
            self.bullet_list.append(bullet)

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        self.player = None
        self.player_list = None
        self.enemy_list = None
        self.bullet_list = None
        self.quantum_gate = QuantumGate()  # Initialize QuantumGate object

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        self.player = arcade.Sprite(":resources:images/space_shooter/playerShip1_orange.png", 0.5)
        self.player_list.append(self.player)

        # Enemy setup code remains the same

    def on_draw(self):
        self.clear()
        self.enemy_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()

    def on_update(self, delta_time):
        self.enemy_list.on_update(delta_time)
        self.bullet_list.update()

        # Check for collision between bullets and enemies
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
                bullet.remove_from_sprite_lists()
                self.quantum_gate.apply_hadamard()  # Apply Hadamard gate when an enemy is hit
                self.quantum_gate.simulate()  # Optional: Simulate and print the quantum state

            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        self.player.center_x = x
        self.player.center_y = 20

def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
