import random
from .template import templates
from .crawler import crawler
from .extract import extract_keyword, extract_plan
from .doc import doc
from .ChatGLM import ChatGLM


class EvoGLM:
    def __init__(self, model_name, baidu=False, wiki=False):
        self.model = ChatGLM(model_name)

        self.template_loader = templates()
        self.crawler = crawler(baidu=baidu, wiki=wiki)
        self.doc = doc()

        self.identities = self.template_loader.get_all_identities()

    def chat(self, prompt, history, num_keywords=1, num_docs=3):
        return self.better_answer(prompt, history, num_keywords, num_docs)

    def better_answer(self, prompt, history, num_keywords=1, num_docs=3):
        original_prompt = prompt

        prompt = self.better_prompt(prompt, history)

        ref = self.references(prompt, num_keywords=num_keywords, num_docs=num_docs)
        prompt = self.template_loader.reference(prompt, ref)

        response, history = self.model.response(prompt, history)
        history[:-1] = [original_prompt, response]

        return response, history

    def better_prompt(self, prompt, history):
        response, history = self.model.response(prompt, history)

        new_history = self.model.response(self.template_loader.opinion(prompt, response), [])[1]
        plan = self.model.response(self.template_loader.plan(), new_history)
        plan = extract_plan(plan)

        prompt = self.template_loader.improve(prompt, plan)
        return prompt

    def references(self, prompt, num_keywords=1, num_docs=3):
        ref = self.online_ref(prompt, num_keywords) + self.local_ref(prompt, num_docs)
        return ref

    def online_ref(self, prompt, num_keywords=1):
        keyword_prompt = self.template_loader.keyword(prompt)
        keywords = random.choices(extract_keyword(self.model.response(keyword_prompt, [])[0]), k=num_keywords)
        return self.crawler.references(keywords)

    def local_ref(self, prompt, k=3):
        return self.doc.top_k_ref(prompt, k)

    def identity_template(self, identity):
        return self.template_loader.identity(identity)

    def add_new_QA(self, prompt, response):
        self.doc.join(prompt, response)

    def add_new_doc(self, docs):
        self.doc.join_doc(docs)
