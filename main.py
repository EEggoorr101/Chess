import raylib
import scenes
import pyray as pr

def application():
    pr.set_target_fps(60)
    pr.init_window(2200, 1500, "Chess")
    scenes_dict = {'menu': scenes.Menu(), 'game': scenes.Game()}
    scene = 'menu'
    while not pr.window_should_close():
        current = scenes_dict[scene]
        scene = current.act()
    pr.close_window()


if __name__=='__main__':
    application()