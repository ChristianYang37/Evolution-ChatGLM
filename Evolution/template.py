from .utils import save, read
from .ChatGLM import ChatGLM

path = './prompt_templates.pkl'


def add_new_template(args):
    model = ChatGLM(args.model_name)
    identity, prompt, response = args.identity, args.prompt, args.response
    if response is None:
        response = model.response(prompt, [])
    t = templates()
    t.add_new_identity(identity, prompt, response)


class templates:
    def __init__(self):
        self.templates = read(path)

    def identity(self, identity):
        return self.templates['identity'][identity]

    def get_all_identities(self):
        return tuple(self.templates['identity'].keys())

    # def langchain(self, prompt):
    #     """
    #     接下来请你严格按照这个格式回答我的问题:\n
    #     为了解决{我的输入}这个问题，我制定了一系列计划来解决：\n
    #     我的计划是：\n
    #     1. {计划第一步}
    #     2. {计划第二步}
    #     ···（此处意为着你可以有任意多步计划）
    #     """

    def keyword(self, prompt):
        """
        template = '请阅读以下文本“{}”，为此文本提取关键词。'
        """
        return self.templates['keyword'].format(prompt)

    def improve(self, ask, plan):
        """
        template = '请依照“{}”这个问题，完成以下任务：{}'
        """
        if len(plan) <= 1:
            return ask
        return self.templates['improve'].format(ask, ' '.join(plan))

    def reference(self, prompt, references):
        """
        template = '现在你有以下案例参考“{}”，{}'
        """
        if len(references) == 0:
            return prompt
        return self.templates['references'].format('，'.join(references), prompt)

    def opinion(self, prompt, response):
        """
        template = 请你阅读接下来的一段对话：“人：{}，AI：{}”请你评价这段对话中AI的回答有没有实际解决到人的问题，请回答有或者没有
        """
        return self.templates['opinion'].format(prompt, response)

    def plan(self):
        """
        template = 如果是你，你会怎么去修改他的回答，请按顺序回答
        """
        return self.templates['plan']

    def add_new_identity(self, identity, prompt, response):
        self.templates['identity'][identity] = (prompt, response)
        self.save()

    def save(self):
        save(self.templates, path)
