import itertools
from copy import deepcopy

STEP_ENERGY = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}


def room_done(room, i):
    return room == ['ABCD'[i], ] * 2


def done(rooms):
    return all(room_done(room, i) for i, room in enumerate(rooms))


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


def dist(room_idx, room_pos, hall_pos):
    room_x = 2 * (room_idx + 1)
    return abs(room_x - hall_pos) + (2 - room_pos)


def can_move_to_room(hall_idx, hall, rooms):
    amph = hall[hall_idx]
    target_room_idx = ord(amph) - ord('A')
    room_x = 2 * (target_room_idx + 1)

    # print('target_room', target_room_idx)
    # if hall_idx >= room_x:
    #     spots = [hall[i] for i in range(room_x + 1, hall_idx + 1)]
    # else:
    #     spots = [hall[i] for i in range(hall_idx + 1, room_x + 1)]
    if room_x <= hall_idx:
        spots = [hall[i] for i in range(room_x, hall_idx)]
    else:
        spots = [hall[i] for i in range(hall_idx + 1, room_x + 1)]
    # print('spots', spots)

    if len(rooms[target_room_idx]) == 2:
        return False

    if any(amph_in_room != amph for amph_in_room in rooms[target_room_idx]):
        return False

    if any(s is not None for s in spots):
        return False

    return True


def part1(hall, rooms):
    seen = {}

    def run(hall, rooms, total_energy):
        key = tuple(map(tuple, rooms)) + tuple(hall) + (total_energy,)
        if key in seen:
            return seen[key]

        # if hall == [None, None, None, None, None, 'D', None, 'D', None, 'A', None]:
        #     print('STATE: ', rooms, hall, total_energy)

        # if hall == [None, None, None, None, None, None, None, None, None, 'A', None] and \
        #         rooms[0] == ['A']:
        #     print('STATE: ', rooms, hall, total_energy)

        # if total_energy == 12521:
        #     print("MATCH? ", rooms, hall)
        if done(rooms):
            # print(rooms, hall)
            seen[key] = [total_energy]
            return [total_energy]

        results = []
        for hall_idx, amph in enumerate(hall):
            if amph is None:
                continue

            # print('here', amph, hall_idx)
            if can_move_to_room(hall_idx, hall, rooms):
                target_room_idx = ord(amph) - ord('A')
                new_hall = hall[:]
                new_rooms = deepcopy(rooms)
                new_hall[hall_idx] = None
                target_room_pos = len(rooms[target_room_idx])
                new_rooms[target_room_idx].append(amph)
                new_energy = total_energy + \
                    STEP_ENERGY[amph] * \
                    dist(target_room_idx, target_room_pos, hall_idx)
                results.extend(run(new_hall, new_rooms, new_energy))

        for room_idx, room in enumerate(rooms):
            # if room_done(room, i) or not room:
            #     continue

            # if room == ['ABCD'[i]]:
            #     continue
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
                    dist(room_idx, room_pos, next_pos)
                results.extend(run(new_hall, new_rooms, new_energy))

        seen[key] = results
        return results

    return min(run(hall, rooms, 0))


def part2(hall, rooms):
    pass


if __name__ == '__main__':
    hall = [None] * 11
    # rooms = [list('ABDCCBAD'[i:i+2]) for i in range(0, 8, 2)]
    rooms = [list('BDAADBCC'[i:i+2]) for i in range(0, 8, 2)]

'''
#############
#.B.B.D.C.CD#
###.#.#.#.###
  #A#.#.#A#
  #########
'''

# hall, rooms = [None, 'B', None, 'B', None, 'D', None,
#                'C', None, 'C', 'D'], [['A'], [], [], ['A']]

# print(can_move_to_room(3, hall, rooms))
# hall = [None, None, None, None, None, None, None, None, None, 'A', None]
# rooms = [
#     ['A'],
#     ['B', 'B'],
#     ['C', 'C'],
#     ['D', 'D'],
# ]

print(part1(hall, rooms))
# print(part2(hall, rooms))

'''
#############
#...B.......#
###B#C#.#D###
  #A#D#C#A#
  #########
'''
# hall, rooms = [None, None, None, 'B', None, None,
#                None, None, None, None, None], [['A', 'B'], ['D', 'C'], ['C'], ['A', 'D']]

# print(list(available_hall_positions(2, hall)))
# assert dist(0, 0, 10) == 10
# C from room 1 to hall 6
# print(dist(1, 1, 5))
# print(dist(2, 1, 5))

# hall, rooms = [None, None, None, None, 'B', None, 6,
#                None, None, None, None], [['A', 'B'], ['D', 'C'], ['C'], ['A', 'D']]

# hall, rooms = [None, None, None, 'B', None, 'C',
#                None, None, None, None, None], [['A', 'B'], ['D'], ['C'], ['A', 'D']]
# print(can_move_to_room(5, hall, rooms))
