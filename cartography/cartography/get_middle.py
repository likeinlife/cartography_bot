from .classes import Degrees

def get_middle(first: Degrees, second: Degrees, number_of_parts: int):
    delta = (second - first) / number_of_parts
    text = ''
    for i in range(number_of_parts + 1):
        text += str(delta*i + first) + '\n'
    return text


if __name__ == "__main__":
    first = Degrees(*list(map(float, input('first >> ').split(' '))))
    second = Degrees(*list(map(float, input('second >> ').split(' '))))
    delta = int(input('Parts >> '))
    get_middle(first, second, delta)
