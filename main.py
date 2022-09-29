from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# テンプレート読み込み
env = Environment(loader=FileSystemLoader('./template/', encoding='utf8'))
tmpl = env.get_template('template.j2')

# エクセルファイル読み込み
params = {"name": "田中",
          "a_value": "test1", "b_value": "test2",
          'items': ['みかん', 'りんご', 'パナナ'],
          'dataObj': {'a': '愛', 'b': '雨', 'c': '江尾'}, }

# レンダリングして出力
rendered_s = tmpl.render(params)
# print(rendered_s)
# ファイルを出力
d = datetime.now()
d_str = d.strftime("%Y%m%d%H%M%S")
file_name = "sample_" + d_str + ".json"
with open("./output/" + file_name, "w", encoding="utf-8") as f:
    f.write(rendered_s)
