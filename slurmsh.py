# coding:utf-8

"""Slurm提出用のシェルスクリプト(.sh)を作成・提出するためのモジュール."""
"""https://web.kudpc.kyoto-u.ac.jp/manual/ja/run/batch would be helpful."""
"""https://slurm.schedmd.com/documentation.html would be helpful."""

import os
from datetime import datetime as dt
import subprocess
import time
import datetime
import warnings
from jobmanegementtool import SchedulerJob
warnings.warn("SlurmSh is deprecated. Use SlurmManager instead.", DeprecationWarning)

class SlurmJob(SchedulerJob):
    """Slurm提出用のシェルスクリプト(.sh)を作成・提出するためのクラス."""
    
    def __init__(self, dir, script_name):
        """
        初期化.
        引数にはシェルスクリプトを保存するディレクトリを指定する.
        このとき、ディレクトリ内に"output"ディレクトリが存在しない場合は作成する.
        引数にはファイル名を指定する.
        """
        self.option_prefix = "#SBATCH"
        super().__init__(dir, script_name)
    
    def iter_command_output(cmd):
        """
        Execute a shell command and yield its output line by line.
        """
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   universal_newlines=True)
        while True:
            line = process.stdout.readline()
            if line != '':
                yield line.rstrip()
            else:
                break
    
    def isRunning(self):
        """
        Check submitted job is still Running
        """

        jobs = self.iter_command_output('squeue')
        columns = None
        for line in jobs:
            if str(self.jobNum) in line:
                columns = line.split()
                #print(line)
        if columns is not None:
            return True
        else:
            return False
    
    def get_exit_status(self):
        jobs=self.iter_command_output("qs")
        columns = None
        for line in jobs:
            if str(self.jobNum) in line:
                columns = line.split()
        if columns is not None:
            return columns[3]
        else:
            return False
        
    def wait_job(self, checkinterval=5):
        """
        ジョブの完了を待つ.
        jobNum: 提出したジョブの番号
        checkinterval: ジョブの完了を確認する間隔
        """
        
        while self.isRunning():
            try:
                time.sleep(checkinterval)
            except Exception as e:
                print(e)
                self.quit_job()
                exit()
        
        result = self.get_exit_status()
        return result
        
    def quit_job(self):
        """
        ジョブをキャンセルする.
        """
        if not hasattr(self, 'jobNum'):
            print("No job number found. Please submit a job first.")
            return
        cmd1 = "scancel " + str(self.jobNum)
        out1 = subprocess.Popen(cmd1, shell=True,
                               stdout=subprocess.PIPE, universal_newlines=True)
        out1 = out1.communicate()[0]
        out2 = subprocess.Popen("Y", shell=True,
                               stdout=subprocess.PIPE, universal_newlines=True)
        print(f"Job {self.jobNum} is cannceled.") 
        return
        
    def submit_job(self, wait=False, checkinterval=5):
        """
        シェルスクリプトを作成して提出する.
        wait: ジョブの完了を待つかどうか
        """
        self.make_scriptfile()
        submitcmd='sbatch ' + self.script_path
        
        out = subprocess.Popen(submitcmd, shell=True,
                               stdout=subprocess.PIPE, universal_newlines=True)
        out = out.communicate()[0]
        self.jobNum = int(out.split()[-1])
        dt_st = datetime.datetime.now()
        print( str(dt_st) +
              f'\nQueue number is {self.jobNum}\n')

        if wait:
            self.wait_job(checkinterval)
            result=self.get_exit_status()
            dt_end = datetime.datetime.now()
            print(str(dt_end) +
                "\nJob "+ str(self.jobNum)+" ended with status "+result + 
                f"\nelapsed time: {dt_end-dt_st}\n")
            
            if result == "FAIL":
                print(f"{self.jobNum} has exited with error")
                exit()   
        return

class SlurmSh:
    """
    Slurm提出用のシェルスクリプト(.sh)を扱うクラス.
    deprecated: Use SlurmManager instead.
    """
    
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
        self.outdir=os.path.join(dir, 'output')
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
        kwargs["o"]=os.path.join(self.outdir, "%x.%j.out")
        kwargs["e"]=os.path.join(self.outdir, "%x.%j.err")
        for k, v in kwargs.items():
            self.batch.append("#SBATCH -"+k+" "+v )
            
    def add_batch(self,lines:list):
        """
        Slurmのオプションを追加する.
        lines: 追加するオプションをリスト形式で指定する.#SBATCH は省略する.
        """
        for x in lines:
            self.batch.append("#SBATCH " + x)

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
        self.path=os.path.join(self.dir, self.filename+'.sh')
        with open(self.path, mode='w') as f:
            f.write('\n'.join(lines))
            
    def isRunning(self):
        """
        Check submitted job is still Running
        """
        def runCmd(exe):
            p = subprocess.Popen(exe, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT,
                                    universal_newlines=True)
            while True:
                line = p.stdout.readline()
                if line != '':
                    # the real code does filtering here
                    yield line.rstrip()
                else:
                    break
        jobs = runCmd('squeue')
        columns = None
        for line in jobs:
            if str(self.jobNum) in line:
                columns = line.split()
                #print(line)
        if columns is not None:
            return True
        else:
            return False
    
    def get_exit_status(self):
        def runCmd(exe):
            p = subprocess.Popen(exe, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT,
                                    universal_newlines=True)
            while True:
                line = p.stdout.readline()
                if line != '':
                    # the real code does filtering here
                    yield line.rstrip()
                else:
                    break
                
        jobs=runCmd("qs")
        columns = None
        for line in jobs:
            if str(self.jobNum) in line:
                columns = line.split()
        if columns is not None:
            return columns[3]
        else:
            return False
    
    def waitjob(self, checkinterval=5):
        """
        ジョブの完了を待つ.
        jobNum: 提出したジョブの番号
        checkinterval: ジョブの完了を確認する間隔
        """
        
        while self.isRunning():
            try:
                time.sleep(checkinterval)
            except Exception as e:
                print(e)
                self.quitjob()
                exit()
        
        result = self.get_exit_status()
        return result
        
            

    
    def quitjob(self):
        """
        ジョブをキャンセルする.
        """
        cmd1 = "scancel " + str(self.jobNum)
        out1 = subprocess.Popen(cmd1, shell=True,
                               stdout=subprocess.PIPE, universal_newlines=True)
        out1 = out1.communicate()[0]
        out2 = subprocess.Popen("Y", shell=True,
                               stdout=subprocess.PIPE, universal_newlines=True)
        print(f"Job {self.jobNum} is cannceled.")
        
        
    
    def submit_sh(self, wait=False, checkinterval=5):
        """
        シェルスクリプトを作成して提出する.
        wait: ジョブの完了を待つかどうか
        """
        self.make_sh()
        cmd='sbatch ' + self.path
        
        out = subprocess.Popen(cmd, shell=True,
                               stdout=subprocess.PIPE, universal_newlines=True)
        out = out.communicate()[0]
        self.jobNum = int(out.split()[-1])
        dt_st = datetime.datetime.now()
        print( str(dt_st) +
              f'\nQueue number is {self.jobNum}\n')

        if wait:
            self.waitjob(checkinterval)
            result=self.get_exit_status()
            dt_end = datetime.datetime.now()
            print(str(dt_end) +
                "\nJob "+ str(self.jobNum)+" ended with status "+result + 
                f"\nelapsed time: {dt_end-dt_st}\n")
            
            if result == "FAIL":
                print(f"{self.jobNum} has exited with error")
                exit()
