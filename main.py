import arcade
import arcade.gui as gui
import arcade.gl as gl
from arcade.types import Color
from PIL import Image
import os

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Arcane Weaponsmithy v0.0.1"

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

TEXTURE_SCALE = (SCREEN_HEIGHT // 40)
RENDER_SCALE = (SCREEN_HEIGHT // 80)

def loadTexture(texture_path: str, texture_name: str):
        print(f"Loading texture: {texture_path}...", end="")
        img = Image.open(texture_path)
        print("Resizing...", end="")
        img = img.resize((img.width * TEXTURE_SCALE, img.height * TEXTURE_SCALE), resample=Image.Resampling.NEAREST)
        print("Finishing up...")
        globals()[texture_name] = arcade.Texture(name=f"{texture_name}", image=img)

# Load textures
loadTexture("assets/gui/buttons/play_button.png", "play_button_texture")
loadTexture("assets/gui/buttons/settings_button.png", "settings_button_texture")
loadTexture("assets/gui/buttons/quit_button.png", "quit_button_texture")
loadTexture("assets/gui/buttons/play_button_hover.png", "play_button_hover_texture")
loadTexture("assets/gui/buttons/settings_button_hover.png", "settings_button_hover_texture")
loadTexture("assets/gui/buttons/quit_button_hover.png", "quit_button_hover_texture")

print("Initializing...")
class ArcaneWeaponsmithy(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
        arcade.set_background_color(Color(72, 72, 72, 255))

        # UI Manager
        self.manager = gui.UIManager()
        self.manager.enable()

        # layout using UIBoxLayout
        self.v_box = gui.UIBoxLayout()

        # Buttons
        self.play_button = gui.UITextureButton(texture=play_button_texture,
                                               width=38 * RENDER_SCALE,
                                               height=8 * RENDER_SCALE,
                                               texture_hovered=play_button_hover_texture)
        self.play_button.on_click = self.play_button_onclick

        self.settings_button = gui.UITextureButton(texture=settings_button_texture,
                                                   width=38 * RENDER_SCALE,
                                                   height=8 * RENDER_SCALE,
                                                   texture_hovered=settings_button_hover_texture)
        self.settings_button.on_click = self.settings_button_onclick

        self.quit_button = gui.UITextureButton(texture=quit_button_texture,
                                               width=38 * RENDER_SCALE,
                                               height=8 * RENDER_SCALE,
                                               texture_hovered=quit_button_hover_texture)
        self.quit_button.on_click = lambda event: arcade.close_window()

        # Add buttons to vertical layout
        self.v_box.add(self.play_button)
        self.v_box.add(gui.UISpace(height=RENDER_SCALE))
        self.v_box.add(self.settings_button)
        self.v_box.add(gui.UISpace(height=RENDER_SCALE))
        self.v_box.add(self.quit_button)

        # Anchor the layout to center of screen
        self.manager = gui.UIManager()
        self.manager.enable()

        # create an anchor layout
        self.anchor = gui.UIAnchorLayout()
        self.manager.add(self.anchor)

        # add your vertical box to the anchor
        self.anchor.add(
            self.v_box,
            anchor_x="center_x",
            anchor_y="center_y",
            align_y=-RENDER_SCALE*5
        )

    def setup(self):
        # Setup sprite list
        self.sprite_list = arcade.SpriteList()
        arcade.SpriteList.DEFAULT_TEXTURE_FILTER = gl.enums.NEAREST, gl.enums.NEAREST

        # Load logo sprite
        self.logo = arcade.Sprite("assets/gui/title/title_v3.png", scale=12)
        self.logo.center_x = self.width // 2
        self.logo.center_y = self.height - (SCREEN_WIDTH / 8)
        self.sprite_list.append(self.logo)

    def on_draw(self):
        self.clear()
        self.sprite_list.draw()
        self.manager.draw()  # draw GUI

        # update logo position on resize
        self.logo.center_x = self.width // 2
        self.logo.center_y = self.height - (self.width / 8)

    def play_button_onclick(self, event):
        pass

    def settings_button_onclick(self, event):
        pass

    def quit_button_onclick(self, event):
        arcade.close_window()


window = ArcaneWeaponsmithy()
window.setup()
arcade.run()