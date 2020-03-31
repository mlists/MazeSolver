from ..solver import find_insterion_index

class Item:
    def __init__(self, value):
        self.value = value



target = Item(8)
values = Item(1), Item(2), Item(3), Item(4), Item(5), Item(7), Item(9), Item(11), Item(14)

values2 = 1, 2, 3, 4, 5, 6, 7, 8, 8, 8, 9, 10
items = []
for value in values2:
    items.append(Item(value))

def test_find_insertion_index():
    # Case where number is not present
    assert find_insterion_index(values, target, "value") == 7
    # Case where number is present
    assert find_insterion_index(items, target, "value") == 11