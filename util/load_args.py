import argparse
from logger import logger
from logging import getLogger

# logger = getLogger("log")


def load_args():
    print("read args")
    args = None
    # 読み込む引数はテストケースフォルダ名
    # 環境名
    # オプションでテスト名
    # インサートのみ等の指定も可能
    # 必須項目が指定されていない場合はエラーで終了する
    # python main.py createCusomer -env=ita -caseNo=01 -mode=only

    parser = argparse.ArgumentParser(
        prog='main.py',  # プログラム名
        usage='自動化テスト実行ツール',  # プログラムの利用方法
        description='以下のように指定する。　'
                    'python3 main.py -env=ita -case=createCustomer',  # 引数のヘルプの前に表示
        add_help=True,  # -h/–help オプションの追加
    )

    # 実行環境の指定
    parser.add_argument('-env',
                        help='実行環境の指定(dev,ita,reg,brl)',  # 開発環境のみ指定可能とする。todo ローカルの設定は一旦保留
                        required=True,  # 実行時の必須項目
                        )

    # 実行するフォルダの指定
    parser.add_argument('-case',
                        help='実行するテストフォルダを入力する。'
                             '最初は一つのファイルのみ実行するようにする',  # todo 親ディレクトリを指定した場合はすべて実行するようにする
                        required=True,  # 実行時の必須項目
                        )

    # 実行するテスト番号の指定
    parser.add_argument('-no',
                        help='実行するテスト番号を入力する。'
                             '複数指定する場合はカンマ区切りで入力する(01,02,07)',
                        default=None,  # 初期値はNone,
                        # metavar='case_no'
                        )
    # 実行モード
    parser.add_argument('--mode',
                        action='store_true',  # True or Falseのみ許容とする
                        default=False,  # デフォルト値はFalse Trueの時のみデータ挿入を実施する
                        help='データ挿入のみ実行する際に使用するフラグ')  # データ挿入のみ実行のフラグ

    # 引数を解析し、返却
    return parser.parse_args()

