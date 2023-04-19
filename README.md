# Evolution-ChatGLM🚀️ 🚀️ 🚀️

***想构建垂直领域LLM，却苦于没有足够的微调数据？***

***无需微调、无需训练、集成了众多prompt模板、支持联网、仅需聊天即可学习的LLM***

## [Chat with Evolution-ChatGLM-6B!!!/在线试用](https://EvoGLM.streamlit.app/)

## 效果演示

## 介绍

Evolution-ChatGLM是基于THUDM/ChatGLM为基模型，通过逻辑链以及prompt模板来引导ChatGLM生成更好的回答，配合专业文档参考（ChatPDF）后的生产效果甚至可以比拟DomainLLM。另外模型可以支持联网搜索参考（new bing），目前支持的参考网站有百度百科、维基百科。

## 本地部署与使用

克隆本项目

```commandline
git clone https://github.com/ChristianYang37/Eovlution-ChatGLM
```

安装依赖项

```commandline
pip install -r requirements.txt
```

运行web ui

```commandline
streamlit run app.py
```

我们还为调用Evolution-ChatGLM模型提供了接口

```python
from Evolution import EvoGLM

model_name = 'THUDM/chatglm-6b'
model = EvoGLM(model_name)

model.chat(
    prompt='你好',
    history=[],
    num_keywords=1, # 提取num_keywords个关键词进行搜索
    num_docs=3 # 在文档中检索出关联度最高的num_docs段文档进行答案参考
)
```

添加新的身份模板

```commandline
python add_new_template --identity 科学家 --prompt 你是一个非常优秀的科学家，我希望你尽你最大的努力使用中文为我解答科学问题，并且给出详细的解释。对于其他非科学领域相关的问题，你可以选择拒绝回答。
```

添加新的参考文档，目前只支持txt文件，每段文档间使用'\n\n'（即两个换行符）隔开

```commandline
python add_new_doc.py --doc ./docs.txt
```

## 详细效果对比
