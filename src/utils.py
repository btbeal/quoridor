def get_proximal_object(curr_position, direction, distance, desired_object_group):
    new_coordinates = get_new_position(curr_position, direction, distance)
    obj_to_return = [obj for obj in desired_object_group if obj.position == new_coordinates]

    return obj_to_return


def get_new_position(curr_position, direction, distance):
    if direction == 'right':
        new_position = tuple(map(sum, zip(curr_position, (distance, 0))))
    elif direction == 'left':
        new_position = tuple(map(sum, zip(curr_position, (-distance, 0))))
    elif direction == 'up':
        new_position = tuple(map(sum, zip(curr_position, (0, -distance))))
    elif direction == 'down':
        new_position = tuple(map(sum, zip(curr_position, (0, distance))))

    return new_position
