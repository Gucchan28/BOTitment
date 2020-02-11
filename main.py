import os
import traceback # エラー表示のためにインポート

import discord
from discord.ext import commands # Bot Commands Frameworkをインポート

# 読み込むコグの名前を格納しておく。
INITIAL_EXTENSIONS = [
    'cogs.recruitment',
]

# クラスの定義。ClientのサブクラスであるBotクラスを継承。
class MyBot(commands.Bot):
    # MyBotのコンストラクタ。
    def __init__(self, command_prefix, help_command):
        # スーパークラスのコンストラクタに値を渡して実行。
        super().__init__(command_prefix, help_command)

        # INITIAL_COGSに格納されている名前から、コグを読み込む。
        # エラーが発生した場合は、エラー内容を表示。
        for cog in INITIAL_EXTENSIONS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    # Botの準備完了時に呼び出されるイベント
    async def on_ready(self):
        print('------')
        print('Discordに接続しました！')
        print('ボット名：' + self.user.name)
        print('discord.py：' + str(discord.__version__))
        print('------')

class JapaneseHelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__()
        self.commands_heading = 'コマンド:'
        self.no_category = 'その他'
        self.command_attrs['help'] = 'コマンド一覧と簡単な説明を表示するよ！'

    def get_ending_note(self):
        return ('コマンドを打つときは、最初に -- をつけてね！\n'
                'コマンドのネタがないから募集中だよ！\n```'
                'http://www.google.com\n```')

# MyBotのインスタンス化及び起動処理。
if __name__ == '__main__':
    bot = MyBot(command_prefix='--', help_command=JapaneseHelpCommand())
    bot.run(os.environ['DISCORD_TOKEN'])
