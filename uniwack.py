# read a raw binary file

from collections import deque

from uritemplate import partial


def get_bits():
    file = open('uniwack-formatted-message.txt', 'rb')
    data = file.read()

    # make a deque of bits as integer 1 or 0
    bits = deque()
    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)

    return bits

def grab_good_bits(input_bits: deque):
    # grab the good bits
    good_bits = deque()
    while input_bits:
        halfword = deque()
        true_parity = 1
        try:
            for _ in range(18):
                bit = input_bits.popleft()
                true_parity = true_parity ^ bit
                halfword.append(bit)
            received_parity = input_bits.popleft()
            if true_parity == received_parity:
                good_bits.extend(halfword)
        except IndexError:
            break
    return good_bits


def print_deque(bits: deque, end=''):
    # print the bits
    while bits:
        print(bits.popleft(), end=end)
    print()


def bits_to_ints(bits: deque):
    ints = deque()
    while bits:
        next_int = 0
        for i in range(9):
            next_int += bits.popleft() << i
        # convert deque to int
        ints.append(next_int)
    return ints

def ints_to_chars(ints: deque):
    chars = deque()
    while ints:
        next_char = ints.popleft()
        if next_char == 0:
            break
        chars.append(chr(next_char))
    return chars

if __name__ == '__main__':
    bits = get_bits()
    
    # grab the good bits
    good_bits = grab_good_bits(bits)
    ints = bits_to_ints(good_bits)
    chars = ints_to_chars(ints)
    print_deque(chars)

