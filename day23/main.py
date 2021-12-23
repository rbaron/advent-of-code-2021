from copy import deepcopy

STEP_ENERGY = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}


def room_done(room, i, room_size):
    return room == ['ABCD'[i], ] * room_size


def done(rooms, room_size):
    return all(room_done(room, i, room_size) for i, room in enumerate(rooms))


def available_hall_positions(room_idx, hall):
    room_x = 2 + 2 * room_idx
    # Walk left.
    for x in range(room_x, 0 - 1, -1):
        if hall[x] is not None:
            break
        if x not in (2, 4, 6, 8):
            yield x
    # Walk right.
    for x in range(room_x, 11):
        if hall[x] is not None:
            break
        if x not in (2, 4, 6, 8):
            yield x


def dist(room_idx, room_pos, hall_pos, room_size):
    room_x = 2 * (room_idx + 1)
    return abs(room_x - hall_pos) + (room_size - room_pos)


def can_move_to_room(hall_idx, hall, rooms, room_size):
    amph = hall[hall_idx]
    target_room_idx = ord(amph) - ord('A')
    room_x = 2 * (target_room_idx + 1)

    if room_x <= hall_idx:
        spots = [hall[i] for i in range(room_x, hall_idx)]
    else:
        spots = [hall[i] for i in range(hall_idx + 1, room_x + 1)]

    if len(rooms[target_room_idx]) == room_size:
        return False

    if any(amph_in_room != amph for amph_in_room in rooms[target_room_idx]):
        return False

    if any(s is not None for s in spots):
        return False

    return True


def find_least_energy_steps(hall, rooms, room_size):
    cache = {}

    def run(hall, rooms, total_energy):
        key = tuple(map(tuple, rooms)) + tuple(hall) + (total_energy,)
        if key in cache:
            return cache[key]

        if done(rooms, room_size):
            cache[key] = [total_energy]
            return [total_energy]

        results = []
        for hall_idx, amph in enumerate(hall):
            if amph is None:
                continue

            if can_move_to_room(hall_idx, hall, rooms, room_size):
                target_room_idx = ord(amph) - ord('A')
                new_hall = hall[:]
                new_rooms = deepcopy(rooms)
                new_hall[hall_idx] = None
                target_room_pos = len(rooms[target_room_idx])
                new_rooms[target_room_idx].append(amph)
                new_energy = total_energy + \
                    STEP_ENERGY[amph] * \
                    dist(target_room_idx, target_room_pos, hall_idx, room_size)
                results.extend(run(new_hall, new_rooms, new_energy))

        for room_idx, room in enumerate(rooms):
            if all(amph == 'ABCD'[room_idx] for amph in room):
                continue

            amph = room[-1]
            # Move topmost amph to the hall.
            room_pos = len(room) - 1
            for next_pos in available_hall_positions(room_idx, hall):
                new_rooms = deepcopy(rooms)
                new_hall = hall[:]
                new_hall[next_pos] = new_rooms[room_idx].pop()
                new_energy = total_energy + \
                    STEP_ENERGY[amph] * \
                    dist(room_idx, room_pos, next_pos, room_size)
                results.extend(run(new_hall, new_rooms, new_energy))

        cache[key] = results
        return results

    return min(run(hall, rooms, 0))


if __name__ == '__main__':
    hall = [None] * 11
    # Test input part 1.
    # rooms_str = 'AB-DC-CB-AD'
    # Test input part 2.
    # rooms_str = 'ADDB-DBCC-CABB-ACAD'

    # Real input part 1.
    # rooms_str = 'BD-AA-DB-CC'
    # Real input part 2.
    rooms_str = 'BDDD-ABCA-DABB-CCAC'

    rooms = [list(r) for r in rooms_str.split('-')]

    print(find_least_energy_steps(hall, rooms, room_size=len(rooms[0])))
