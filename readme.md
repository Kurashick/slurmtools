# SlurmSh

SlurmShは、Slurmジョブスケジューラ用のシェルスクリプト(.shファイル)を生成および提出するためのPythonモジュールです。

## インストール

このプロジェクトには特別なインストール手順は必要ありません。Pythonがインストールされている環境であれば動作します。

## 使い方

### 1. 初期化

まず、`SlurmSh`クラスのインスタンスを作成します。引数にはシェルスクリプトを保存するディレクトリのパスを指定します。

```python
from slurmsh import SlurmSh

path = "path/to/dir"
obj = SlurmSh(path)
```

### 2. Slurmオプションの設定

`set_batch`メソッドを使用して、Slurmのオプションを設定します。デフォルトのキュー名、実行時間、リソースの指定を引数として受け取ります。その他のオプションはキーワード引数として指定できます。

```python
obj.set_batch(p="gr19999b", t="24:00:00", rsc='p=4:t=8:c=8:m=8G')
```

### 3. コマンドの設定

`set_command`メソッドを使用して、シェルスクリプト内で実行するコマンドを設定します。引数にはコマンドを文字列で指定します。

```python
obj.set_command("set -x","srun ./a.out")
```

### 4. シェルスクリプトの作成と提出

`submit_sh`メソッドを使用して、シェルスクリプトを作成し、それをSlurmに提出します。引数にはシェルスクリプトのファイル名(.sh抜き)を指定します。

```python
obj.submit_sh("shellscript")
```

## 出力ファイル

シェルスクリプトの実行結果及びエラーは、指定したディレクトリの`output`フォルダに保存されます。



## サンプル

以下は、`sample.py`ファイルのサンプルコードです。

```python
from slurmsh import SlurmSh

path = "path/to/dir"
obj = SlurmSh(path)

obj.set_batch(p="gr19999b", t="12:00:00", rsc='p=4:t=8:c=8:m=8G')
obj.set_command("set -x","srun ./a.out")
obj.submit_sh("sample")
```

実行後ファイル構成例:
```
path/to/dir
    ├sample.sh
    └output
        ├sample.sh.1234567.err
        └sample.sh.1234567.out
```


## 参考リンク

- [スーパーコンピュータシステムの使い方](https://web.kudpc.kyoto-u.ac.jp/manual/ja/run/batch)
- [Slurm公式:sbatchのオプション](https://slurm.schedmd.com/sbatch.html)

