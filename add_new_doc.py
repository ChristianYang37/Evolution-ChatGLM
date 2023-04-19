import argparse
from Evolution.doc import add_new_doc


def read_docs(path):
    with open(path, mode='r', encoding='utf-8') as file:
        docs = file.read().split('\n\n')
    return docs


def main():
    paser = argparse.ArgumentParser()

    paser.add_argument("--doc", type=str, default=None)

    args = paser.parse_args()

    docs = read_docs(args.doc)
    add_new_doc(docs)


if __name__ == '__main__':
    main()
