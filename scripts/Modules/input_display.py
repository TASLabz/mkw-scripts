from dolphin import gui


def create_unpressed_button(center: tuple, radius: int, color: int):
    """
    Creates an empty circle similar to an "ABXY" button.

    Args:
        center (tuple): The center of the button in the form of [x, y].
        radius (int): The radius of the button.
        color (int): The color of the button outline in the form of 0xAARRGGBB.
    """
    gui.draw_circle(center, radius, color, 32)


def fill_pressed_button(center: tuple, radius: int, color: int):
    """
    Creates a filled circle similar to an "ABXY" button.

    Args:
        center (tuple): The center of the button in the form of [x, y].
        radius (int): The radius of the button.
        color (int): The color of the button in the form of 0xAARRGGBB.
    """
    gui.draw_circle_filled(center, radius, color, 32)


def create_unpressed_bumper(bottom_left_pos: tuple, width: int,
                            height: int, color: int):
    """
    Creates an empty rectangle shape similar to a bumper.

    Args:
        bottom_left_pos (tuple): The position of the bumper in the form of [x, y].
        width (int): The width of the bumper.
        height (int): The height of the bumper.
        color (int): The color of the bumper outline in the form of 0xAARRGGBB.
    """
    gui.draw_rect(bottom_left_pos,
                  [bottom_left_pos[0] + width, bottom_left_pos[1] + height], color, 10)


def fill_pressed_bumper(bottom_left_pos: tuple, width: int, height: int, color: int):
    """
    Creates a filled rectangle shape similar to a bumper.

    Args:
        bottom_left_pos (tuple): The position of the bumper in the form of [x, y].
        width (int): The width of the bumper.
        height (int): The height of the bumper.
        color (int): The color of the bumper in the form of 0xAARRGGBB.
    """
    gui.draw_rect_filled(bottom_left_pos,
                        [bottom_left_pos[0] + width, bottom_left_pos[1] + height],
                        color, 10)


def create_dpad(bottom_left_pos: tuple, button_width: int,
                button_height: int, color: int):
    """
    Creates a shape similar to a directional pad.

    Args:
        bottom_left_pos (tuple): The position of the D-Pad in the form of [x, y].
        width (int): The width of an individual direction on the pad.
        height (int): The height of an individual direction on the pad.
        color (int): The color of the D-Pad outline in the form of 0xAARRGGBB.

    TODO: fix this and remove the warning
    **IF USING GET_DISPLAY_SIZE IN THE POSITION,
    **USE THE NEGATIVE VALUE FOR IT TO APPEAR CORRECTLY**
    """
    x, y = bottom_left_pos

    # D-Up
    gui.draw_line([x + button_width, y + button_height * 3],
                  [x + button_width * 2, y + button_height * 3], color)
    gui.draw_line([x + button_width, y + button_height * 2],
                  [x + button_width, y + button_height * 3], color)
    gui.draw_line([x + button_width * 2, y + button_height * 2],
                  [x + button_width * 2, y + button_height * 3], color)

    # D-Down
    gui.draw_line([x + button_width, y],
                  [x + button_width * 2, y], color)
    gui.draw_line([x + button_width, y + button_height],
                  [x + button_width, y], color)
    gui.draw_line([x + button_width * 2, y + button_height],
                  [x + button_width * 2, y], color)

    # D-Left
    gui.draw_line([x, y + button_height],
                  [x + button_width, y + button_height], color)
    gui.draw_line([x, y + button_height * 2],
                  [x, y + button_height], color)
    gui.draw_line([x, y + button_height * 2],
                  [x + button_width, y + button_height * 2], color)

    # D-Right
    gui.draw_line([x + button_width * 2, y + button_height],
                  [x + button_width * 3, y + button_height], color)
    gui.draw_line([x + button_width * 3, y + button_height * 2],
                  [x + button_width * 3, y + button_height], color)
    gui.draw_line([x + button_width * 2, y + button_height * 2],
                  [x + button_width * 3, y + button_height * 2], color)


def fill_dpad(bottom_left_pos: tuple, button_width: int, button_height: int,
              color: int, directions: tuple):
    """
    Fills out direction(s) on a directional pad, used in conjunction with create_dpad.
    If using the create_dpad function, paste those arguments here,
    and fill out the "directions" argument appropriately.

    Args:
        bottom_left_pos (tuple): The position of the D-Pad in the form of [x, y].
        width (int): The width of an individual direction on the pad.
        height (int): The height of an individual direction on the pad.
        color (int): The color of the pressed D-Pad button in the form 0xAARRGGBB.
        directions (tuple): The button(s) pressed ("Up", "Down", "Left", and/or "Right")
        Can accept multiple values.

    TODO: fix this and remove the warning
    **IF USING GET_DISPLAY_SIZE IN THE POSITION,
    **USE THE NEGATIVE VALUE FOR IT TO APPEAR CORRECTLY**
    """
    x, y = bottom_left_pos

    # D-Up
    if "Up" in directions:
        gui.draw_rect_filled([x + button_width, y + button_height * 2],
                             [x + button_width * 2, y + button_height * 3], color)

    # D-Down
    if "Down" in directions:
        gui.draw_rect_filled([x + button_width, y],
                             [x + button_width * 2, y + button_height], color)

    # D-Left
    if "Left" in directions:
        gui.draw_rect_filled([x, y + button_height],
                             [x + button_width, y + button_height * 2], color)

    # D-Right
    if "Right" in directions:
        gui.draw_rect_filled([x + button_width * 2, y + button_height],
                             [x + button_width * 3, y + button_height * 2], color)


def create_control_stick(center: tuple, bounding_radius: int, stick_radius: int,
                         move_radius: int, stick_x: int, stick_y: int, color: int):
    """
    Creates a control stick with a bounding circle.

    Args:
        center (tuple): The [x, y] position of the center of the control stick.
        bounding_radius (int): The radius of the bounding circle.
        stick_radius (int): The radius of the control stick.
        move_radius (int): The radius the control stick can move in.
        stick_x (int): The x-axis position of the stick (0-255).
        stick_x (int): The y-axis position of the stick (0-255).
        color (int): The color of the pressed D-Pad button in the form of 0xAARRGGBB.
    """

    stick_x -= 127
    stick_y -= 127

    x, y = (center[0] + (bounding_radius * (stick_x / 127)),
            center[1] - (bounding_radius * (stick_y / 127)))

    if (x < center[0] - bounding_radius - move_radius):
        x = center[0] - bounding_radius - move_radius
    elif (x > center[0] + bounding_radius + move_radius):
        x = center[0] + bounding_radius + move_radius
    if (y < center[1] - bounding_radius - move_radius):
        y = center[1] - bounding_radius - move_radius
    elif (y > center[1] + bounding_radius + move_radius):
        y = center[1] + bounding_radius + move_radius

    gui.draw_circle(center, bounding_radius, color, 8)
    gui.draw_circle_filled([x, y], stick_radius, color, 8)
