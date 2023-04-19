import pickle


def save(obj, path):
    with open(path, mode='wb') as file:
        pickle.dump(obj, file, True)


def read(path):
    with open(path, mode='rb') as file:
        return pickle.load(file)
