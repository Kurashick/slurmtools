# coding:utf-8

"""Slurm提出用のシェルスクリプト(.sh)を作成・提出するためのモジュール."""
"""https://web.kudpc.kyoto-u.ac.jp/manual/ja/run/batch would be helpful."""

import os
from datetime import datetime as dt
from subprocess import check_call


class SlurmSh:
    """Slurm提出用のシェルスクリプト(.sh)を扱うクラス."""
    
    def __init__(self,dir,filename):
        """
        初期化.
        引数にはシェルスクリプトを保存するディレクトリを指定する.
        このとき、ディレクトリ内に"outdir"ディレクトリが存在しない場合は作成する.
        引数にはファイル名を指定する.
        """
        self.batch=["#!/bin/bash","#============ Slurm Options ==========="]
        self.command=["","#============ Shell Script ============"]
        self.dir=dir
        self.filename=filename
        self.outdir=dir+"/output"
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)

    def set_batch(self,p="gr10569b",t="24:00:00",rsc='p=4:t=8:c=8:m=8G',**kwargs):
        """
        Slurmのオプションを設定する.
        オプション名のhyphen(-)は１つ省略して記述する.(kwargsのkeyにはhyphen(-)を含めないため)
        p, t, rscはデフォルト値が設定されている.
        pはキュー名,tは実行時間,rscはリソースの指定.
        その他のオプションは**kwargsで指定する.
        out及びerrはoutdirディレクトリに保存される.
        """
        kwargs["p"]=p
        kwargs["t"]=t
        kwargs["-rsc"]=rsc
        kwargs["o"]=self.outdir+"/%x.%j.out"
        kwargs["e"]=self.outdir+"/%x.%j.err"
        for k, v in kwargs.items():
            self.batch.append("#SBATCH -"+k+" "+v )

    def set_command(self,*args):
        """
        シェルスクリプトのコマンドを設定する.
        引数にはコマンドを文字列で指定する.
        １つのコマンドを複数行に分けて記述する場合は引数を複数指定する.
        """
        for x in args:
            self.command.append(x)

    def make_list(self):
        """
        シェルスクリプトをリスト形式で返す.
        このとき、末尾にコメントが追加される.
        """
        lines=self.batch+self.command
        comment="# made by sh.py automatically\n# "+str(dt.now())
        lines.append(comment)
        return lines

    def make_sh(self):
        """
        シェルスクリプトを作成する.
        """
        lines=self.make_list()
        self.path=self.dir+"/"+self.filename+'.sh'
        with open(self.path, mode='w') as f:
            f.write('\n'.join(lines))
    
    def submit_sh(self):
        """
        シェルスクリプトを作成して提出する.
        """
        self.make_sh()
        cmd='sbatch ' + self.path
        check_call(cmd.split())


