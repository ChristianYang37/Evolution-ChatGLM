import torch
from transformers import AutoModel, AutoTokenizer


DEVICE = "cuda"
DEVICE_ID = "0"
CUDA_DEVICE = f"{DEVICE}:{DEVICE_ID}" if DEVICE_ID else DEVICE


def torch_gc():
    if torch.cuda.is_available():
        with torch.cuda.device(CUDA_DEVICE):
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()


class ChatGLM:
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(model_name, trust_remote_code=True).half().cuda()
        self.model.eval()

    def response(self, prompt, history):
        response, history = self.model.chat(self.tokenizer, prompt, history=history, max_length=2048, top_p=0.7,
                                            temperature=0.95)
        torch_gc()
        return response, history
