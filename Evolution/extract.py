def extract_keyword(response):
    return response[4:-1].split('、')


def extract_plan(response):
    ret = []
    for i in range(1, 20):
        start = response.find(f'{i}.')
        if start == -1:
            break
        s = ''
        while response[start] != '\n':
            s += response[start]
            start += 1
        ret.append(s)
    return ret
