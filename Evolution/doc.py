from .utils import read, save
from rank_bm25 import BM25Okapi

path = './local_ref.pkl'

stop_word = {'。', '：', '，', '“', '”', '’', '‘', '？', '【', '】', '；', '、'}


class doc:
    def __init__(self):
        self.doc = read(path)
        self.bm25 = BM25Okapi(self.tokenize(text) for text in self.doc)

    def top_k_ref(self, prompt, k=3):
        return self.bm25.get_top_n(self.tokenize(prompt), self.doc, n=k)

    def join(self, prompt, response):
        self.doc.append(f'问：{prompt}，答：{response}')
        self.save()

    def join_doc(self, new_doc):
        self.doc.extend(new_doc)
        self.save()

    def save(self):
        save(self.doc, path)

    @staticmethod
    def tokenize(text):
        ret = []
        for c in text:
            if c not in stop_word:
                ret.append(c)
        return ret


def add_new_doc(docs):
    local_doc = doc()
    local_doc.join_doc(new_doc=docs)


def add_new_QA(prompt, response):
    local_doc = doc()
    local_doc.join(prompt, response)
