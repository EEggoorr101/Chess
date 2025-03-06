import scenes
import pyray as pr
from screeninfo import get_monitors

def application():
    pr.set_target_fps(60)
    monitor = get_monitors()[0]
    print(monitor)
    pr.init_window(monitor.width, monitor.height, "Chess")
    scenes_dict = {'menu': scenes.Menu(), 'game': scenes.Game()}
    scenes_dict['game'].new_game()
    scene = 'menu'
    while not pr.window_should_close():
        current = scenes_dict[scene]
        scene = current.act()
    pr.close_window()
    return 0


if __name__=='__main__':
    application()