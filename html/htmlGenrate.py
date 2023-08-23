import json

import jinja2
from jinja2 import FileSystemLoader, Environment


def main():
    env = Environment(loader=FileSystemLoader('.', encoding='utf8'))
    template = env.get_template('template.txt')

    # data = {'data_list' : [
    #     {
    #         'name': 'リンゴ',
    #         'price' : 150,
    #         'profit' : 1000
    #     },
    #     {
    #         'name': 'バナナ',
    #         'price' : 100,
    #         'profit' : -500
    #     },
    #     {
    #         'name': 'レモン',
    #         'price' : 200,
    #         'profit' : 0
    #     }]}

    with open("template/template.json", 'r', ) as f:
        params = json.load(f)
        rendered = template.render(params)
        print(rendered)

        # レンダリングしてhtml出力
        rendered_html = template.render(params)
        with open('./results/result_01.html', 'w', encoding='shift_jis') as f:
            f.write(rendered_html)
            f.close()


if __name__ == "__main__":
    main()
