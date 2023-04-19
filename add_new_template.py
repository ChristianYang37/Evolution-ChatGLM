import argparse
from Evolution.template import add_new_template


def get_input(args):
    if args.identity is None:
        args.identity = input('请输入你要添加的模板身份（示例：程序员）：')
    if args.prompt is None:
        args.prompt = input(f'请为{args.identity}这个身份输入prompt模板：')
    return args


def main():
    paser = argparse.ArgumentParser()

    paser.add_argument("--model_name", type=str, default="THUDM/chatglm-6b")
    paser.add_argument("--identity", type=str, default=None)
    paser.add_argument("--prompt", type=str, default=None)
    paser.add_argument("--response", type=str, default=None)

    args = paser.parse_args()

    args = get_input(args)
    add_new_template(args)


if __name__ == '__main__':
    main()
