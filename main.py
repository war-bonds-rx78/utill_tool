import ast
import pandas as pd
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# テンプレート読み込み
env = Environment(loader=FileSystemLoader('./template/', encoding='utf8'))
tmpl = env.get_template('template.j2')

# キーマッピングシート読み込み
mappingData = pd.read_excel(
    'input/input.xlsx', sheet_name="mapping", index_col=0)

# ターゲットシート（svod/set/est/series/pit）取得
inputSheet = pd.read_excel('input/input.xlsx', sheet_name="inputSheet")

# ターゲットシートから投入データのjsonを作成
for row in inputSheet.values:
    targetSheet = pd.read_excel(
        'input/input.xlsx', sheet_name=row[0])
    mappingList = targetSheet.columns.values
    # 1行分を取得
    for _, row in targetSheet.iterrows():
        # ninja変換データ
        params = {}
        # ヘッダ＝項目であるので項目分データを設定
        for column in mappingList:
            # マッピングキーと項目合わせた型を取得
            # 本来ならであればkeyとtypeのみで十分だがkey名の確定が遅い場合に備えて仮設定も考慮
            # print(row[cloum])
            key = mappingData.loc[column, "key"]
            type = mappingData.loc[column, "type"]
            if "string" == type:
                value = row[column]

            elif 'list' == type:
                value = row[column].split(',')
            elif 'obj' == type:
                value = ast.literal_eval(row[column])
            # 型に合わせてデータを作成
            params[key] = value
            # 変換データを辞書型で保持

        # ninjaによるレンダリング
        # レンダリングデータを出力
        rendered_s = tmpl.render(params)
        d = datetime.now()
        d_str = d.strftime("%Y%m%d%H%M%S")
        file_name = "sample_" + d_str + '_' + row['name'] + ".json"
        with open("./output/" + file_name, "w", encoding="utf-8") as f:
            f.write(rendered_s)
