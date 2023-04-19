import argparse
import streamlit as st
from Evolution import EvoGLM


class APP:
    def __init__(self, args):
        if 'history' not in st.session_state:
            st.session_state['history'] = []

        st.title(f'Chat with {args.model_name}')

        baidu = st.checkbox('向百度搜索专业知识以参考')
        wiki = st.checkbox('向维基百科搜索专业知识以参考')

        self.model = EvoGLM(args.model_name, baidu, wiki)
        self.container = st.container()

        identity = st.selectbox('为ChatGLM选择一个身份使其更好地完成专业工作', self.model.identities)
        self.fill_template(identity)

        self.num_keywords = args.num_keywords
        self.num_refs = args.num_refs

    def loop(self):
        form = st.form('input_area')

        form.text_input(
            "",
            label_visibility="visible",
            disabled=False,
            placeholder="请输入",
            key="prompt"
        )
        form.form_submit_button('Submit', on_click=self.action, use_container_width=True)

    def action(self):
        for prompt, response in st.session_state['history']:
            self.container.code('你：\n\t' + prompt)
            self.container.code('Evo-ChatGLM：\n\t' + response)

        prompt = st.session_state['prompt']

        self.container.code('你：\n\t' + prompt)

        st.session_state['progress'] = True
        if st.session_state['progress']:
            bar = st.progress(0, '')
            bar.progress()

        response = self.model.chat(prompt, st.session_state['history'], self.num_keywords, self.num_refs)

        st.session_state['history'].append([prompt, response])

        self.container.code('Evo-ChatGLM：\n\t' + response)

        save = self.container.button('取消加入保存', use_container_width=True)
        if save:
            new_doc = self.container.text_input('如果我回答得不好，你可以在此输入一些答案以便改进我的回答')
            self.model.add_new_doc([new_doc])
        else:
            self.model.add_new_QA(prompt, response)

        st.session_state['prompt'] = ''

    def fill_template(self, identity):
        prompt, response = self.model.identity_template(identity)
        st.session_state['history'].append([prompt, response])


def main():
    paser = argparse.ArgumentParser()

    paser.add_argument("--model_name", type=str, default="THUDM/chatglm-6b")
    paser.add_argument("--num_keywords", type=int, default=2)
    paser.add_argument("--num_refs", type=int, default=3)

    args = paser.parse_args()

    app = APP(args)
    app.loop()


if __name__ == '__main__':
    main()
