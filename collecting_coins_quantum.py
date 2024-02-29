import random
import arcade
import math
import os
from qiskit import QuantumCircuit, Aer, execute

# Constants
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.2
SPRITE_SCALING_LASER = 0.8
COIN_COUNT = 50

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Collecting coins and creating quantum circuit"

BULLET_SPEED = 5

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        # Set the working directory to where this file is located
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        
        # Variables that will hold sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        
        # Set up the player
        self.player_sprite = None
        self.score = 0
        
        # Load sounds
        self.gun_sound = arcade.load_sound(":resources:sounds/laser1.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/phaseJump1.wav")
        
        # Set background color
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """
        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.score = 0
        
        # Set up the player
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)
        
        # Create the coins
        for i in range(COIN_COUNT):
            coin = arcade.Sprite(":resources:images/items/coinGold.png", SPRITE_SCALING_COIN)
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)
            self.coin_list.append(coin)

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()  # Starts the render process, this line is necessary.
        
        # Draw all the sprites
        self.coin_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()
        
        # Render the text
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called whenever the mouse button is clicked. """
        # Gun sound
        arcade.play_sound(self.gun_sound)
        
        # Create a bullet
        bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING_LASER)
        bullet.center_x = self.player_sprite.center_x
        bullet.center_y = self.player_sprite.center_y
        
        # Calculate the angle to the target
        x_diff = x - self.player_sprite.center_x
        y_diff = y - self.player_sprite.center_y
        angle = math.atan2(y_diff, x_diff)
        
        bullet.angle = math.degrees(angle)
        bullet.change_x = math.cos(angle) * BULLET_SPEED
        bullet.change_y = math.sin(angle) * BULLET_SPEED
        
        self.bullet_list.append(bullet)

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.bullet_list.update()
        
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.coin_list)
            
            for coin in hit_list:
                coin.remove_from_sprite_lists()
                self.score += 1
                self.display_quantum_gate()  # Display a quantum gate upon coin collection
                
            if bullet.bottom > self.height or bullet.top < 0 or bullet.right < 0 or bullet.left > self.width:
                bullet.remove_from_sprite_lists()

    def display_quantum_gate(self):
        """Create and display a specific quantum circuit when a coin is collected."""
        qc = QuantumCircuit(3)
        qc.h([0, 1, 2])
        qc.cx(0, 1)
        qc.cx(1, 2)
        print("Quantum Circuit when a coin is collected:")
        print(qc)

def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
