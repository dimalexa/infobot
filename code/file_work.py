from code.polls import user_data


def get_results():
    results = []
    f = open('../data/results.txt', 'r')
    for line in f:
        results.append(line.replace('\n', '').split(','))
    f.close()
    return results

def update_results(results, name):
    for i in range(len(results)):
        if results[i][0] == name:
            results[i][1] = int(results[i][1]) + 1
    f = open('../data/results.txt', 'w')
    for e in results:
        f.write(f'{e[0]},{e[1]}' + '\n')
    f.close()

def get_winner():
    results = get_results()
    win = [[results[0][0], results[0][1]]]
    for e in results:
        if e[1] > win[0][1]:
            win[0][0],win[0][1] = e[0], e[1]

    for e in results:
        if e[1] == win[0][1] and e[0] != win[0][0]:
            win.append([e[0], e[1]])

    if len(win) == 1:
        output = f'Победил(а) {win[0][0].capitalize()}, поздравляем!'
    else:
        print(win)
        output = ''
        for e in win:
            output += f'{e[0].capitalize()}, '
        output += 'вы набрали равное количество голосов!'
    return output


def get_complited():
    teg_id = []
    f = open('../data/complited_poll.txt', 'r')
    for line in f:
        teg_id.append(int(line.replace('\n', '')))
    f.close()
    return teg_id

def update_complited(t_id):
    teg_id = get_complited()
    teg_id.append(t_id)
    f = open('../data/complited_poll.txt', 'w')
    for e in teg_id:
        f.write(f'{e}' + '\n')
    f.close()

def clear_complited():
    f = open('../data/complited_poll.txt', 'w')
    f.close()


def new_results():
    results = []
    for e in user_data:
        results.append([e, 0])

    f = open('../data/results.txt', 'w')
    for e in results:
        f.write(f'{e[0]},{e[1]}' + '\n')
    f.close()