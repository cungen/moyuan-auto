from direct_keys import *

prev_movement = []
prev_action = []


def take_action(movement_index, action_index):
    """Send action to the game."""
    global prev_movement
    # Movements
    movements = [[], [W], [S], [A], [D]]
    actions = [[], [J], [K], [I], [O], [G]]

    print('movement: ' + str(movement_index) + ' and action: ' + str(action_index))

    move = movements[movement_index]
    action = actions[action_index]

    if prev_movement != move:
        for m in prev_movement:
            ReleaseKey(m)
        for m in move:
            PressKey(m)

        prev_movement = move

    if prev_action != action:
        for a in prev_action:
            ReleaseKey(a)
        for a in action:
            PressKey(a)

    time.sleep(0.18)
