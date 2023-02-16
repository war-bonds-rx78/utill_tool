import glob
import pandas as pd
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
## 概要　 ##
# csv情報からSQLを生成するツール
##########

# テンプレート読み込み
tmpl = Environment(loader=FileSystemLoader(
    './template/', encoding='utf8')).get_template('template_make_sql.j2')

# ファイル一覧を取得（csv限定）
file_list = sorted(glob.glob('./input/*csv'))
# マージファイルA情報
mage_data_a = []
# 全てのファイルをマージして１つのファイルに出力
for file in file_list:
    # リストの設定
    # hedarをNoneにして自動で割り当ててcsvの自動結合ができるようにする
    mage_data_a.append(pd.read_csv(
        file, encoding='utf-8', sep=',', header=None))

# 結合条件
mage_csv = pd.concat(mage_data_a)
# 統合したファイルを出力
mage_csv.to_csv('./output/sample.csv', encoding='utf-8',
                index=False, header=False)

# 行単位でリストする
re_data = mage_csv.set_axis(
    ['id', 'name', 'age', 'sex'], axis=1).to_dict(orient='records')
# テンプレートつ買ってSQLを生成
params = {}
params['items'] = re_data
# ninjaによるレンダリング

# レンダリングデータを出力
rendered_s = tmpl.render(params)
d = datetime.now()
d_str = d.strftime("%Y%m%d%H%M%S")
file_name = "sample_" + d_str + ".sql"
with open("./output/" + file_name, "w", encoding="utf-8") as f:
    f.write(rendered_s)
