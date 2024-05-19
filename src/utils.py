def get_proximal_object(curr_position, direction, desired_object_group):
    new_coordinates = tuple(map(sum, zip(curr_position, direction)))
    for obj in desired_object_group:
        if obj.position == new_coordinates:
            return obj

    return None
