import telnetlib

def get_matrix(tn):
    lines = []
    for i in range(5):
        line = tn.read_until(b'\n').decode('ascii').strip()
        line = line.replace('[', '').replace(']', '').replace(' ', '')
        line = [int(num) for num in line.split(',')]
        lines.append(line)
    return lines

def get_answer(matrix):
    # add the smallest values in each row
    answer = 0
    for row in matrix:
        answer += min(row)
    return answer

if __name__ == '__main__':
    tn = telnetlib.Telnet('code.deadface.io', 50000)

    matrix = get_matrix(tn)
    print(matrix)

    answer = get_answer(matrix)
    print(answer)

    tn.write(str(answer).encode('utf-8'))

    for i in range(2):
        print(tn.read_until(b'\n'))