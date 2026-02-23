import arcade
import random

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Dodge Game 3.x Version"

PLAYER_SPEED = 5
BLOCK_SPEED = 8
BLOCK_SIZE = 40

class DodgeGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        self.player_x = SCREEN_WIDTH // 2
        self.player_y = 50
        self.blocks = []
        self.score = 0
        self.score_text = arcade.Text(f"Score: {self.score}", 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 20)

        # track currently held keys for arrows
        self.held_keys = set()

    def on_draw(self):
        self.clear()
        # player
        arcade.draw_lbwh_rectangle_filled(
            self.player_x - BLOCK_SIZE//2,
            self.player_y - BLOCK_SIZE//2,
            BLOCK_SIZE, BLOCK_SIZE,
            arcade.color.GREEN
        )
        # blocks
        for (bx, by) in self.blocks:
            arcade.draw_lbwh_rectangle_filled(
                bx - BLOCK_SIZE//2,
                by - BLOCK_SIZE//2,
                BLOCK_SIZE, BLOCK_SIZE,
                arcade.color.RED
            )
        # score
        self.score_text.draw()

    def on_update(self, delta_time):
        # move player for held arrow keys
        if arcade.key.LEFT in self.held_keys:
            self.player_x -= PLAYER_SPEED
        if arcade.key.RIGHT in self.held_keys:
            self.player_x += PLAYER_SPEED

        # keep player in bounds
        self.player_x = max(BLOCK_SIZE//2, min(SCREEN_WIDTH - BLOCK_SIZE//2, self.player_x))

        # move blocks down
        self.blocks = [(x, y - BLOCK_SPEED) for (x, y) in self.blocks]
        self.blocks = [(x, y) for (x, y) in self.blocks if y > -BLOCK_SIZE]

        # spawn new block randomly
        if random.random() < 0.2:
            new_x = random.randint(BLOCK_SIZE//2, SCREEN_WIDTH - BLOCK_SIZE//2)
            self.blocks.append((new_x, SCREEN_HEIGHT + BLOCK_SIZE))

        # check collisions
        for (bx, by) in self.blocks:
            if abs(bx - self.player_x) < BLOCK_SIZE and abs(by - self.player_y) < BLOCK_SIZE:
                print("Game Over! Final Score:", self.score)
                arcade.close_window()
                return

        # update score
        self.score += 1
        self.score_text.text = f"Score: {self.score}"

    def on_key_press(self, symbol, modifiers):
        # tap keys
        if symbol == arcade.key.A:
            self.player_x -= PLAYER_SPEED
        elif symbol == arcade.key.D:
            self.player_x += PLAYER_SPEED
        # start holding arrow keys
        elif symbol in (arcade.key.LEFT, arcade.key.RIGHT):
            self.held_keys.add(symbol)

        # clamp
        self.player_x = max(BLOCK_SIZE//2, min(SCREEN_WIDTH - BLOCK_SIZE//2, self.player_x))

    def on_key_release(self, symbol, modifiers):
        if symbol in self.held_keys:
            self.held_keys.remove(symbol)

game = DodgeGame()
arcade.run()