# slurmtools
**内容物**

- slurmsh:バッチ処理を行うためのモジュール. `SlurmSh`クラスを定義している。
- batchespresso:`ase.calculator.espresso`をバッチ処理向けに改変したモジュール。

## SlurmSh

SlurmShは、Slurmジョブスケジューラ用のシェルスクリプト(.shファイル)を生成および提出するためのPythonモジュールです。

### 使い方

#### 1. 初期化

まず、`SlurmSh`クラスのインスタンスを作成します。引数にはシェルスクリプトを保存するディレクトリのパスを指定します。

```python
from slurmsh import SlurmSh

path = "path/to/dir"
obj = SlurmSh(path)
```

#### 2. Slurmオプションの設定

`set_batch`メソッドを使用して、Slurmのオプションを設定します。デフォルトのキュー名、実行時間、リソースの指定を引数として受け取ります。その他のオプションはキーワード引数として指定できます。

```python
obj.set_batch(p="gr19999b", t="24:00:00", rsc='p=4:t=8:c=8:m=8G')
```

#### 3. コマンドの設定

`set_command`メソッドを使用して、シェルスクリプト内で実行するコマンドを設定します。引数にはコマンドを文字列で指定します。

```python
obj.set_command("set -x","srun ./a.out")
```

#### 4. シェルスクリプトの作成と提出

`submit_sh`メソッドを使用して、シェルスクリプトを作成し、それをSlurmに提出します。引数にはシェルスクリプトのファイル名(.sh抜き)を指定します。

```python
obj.submit_sh("shellscript")
```

### 出力ファイル

シェルスクリプトの実行結果及びエラーは、指定したディレクトリの`output`フォルダに保存されます。



### サンプル

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


### 参考リンク

- [スーパーコンピュータシステムの使い方](https://web.kudpc.kyoto-u.ac.jp/manual/ja/run/batch)
- [Slurm公式:sbatchのオプション](https://slurm.schedmd.com/sbatch.html)


## batchespresso

batchespressoは`ase.calculator.espresso`をスパコンで行うバッチ処理向けに改変したモジュール。

### 相違点
- モジュール名.対応関係は以下.
    - BatchEspressoProfile(EspressoProfile)
    - BatchEspressoTemplate(EspressoTemplate)
    - BatchEspresso(Espresso)
- BatchEspressoProfile
    - 引数`command`の削除
    - 引数`slshobj`の追加(SlurmSh型のオブジェクト)
- BatchEspressoTemplate
    - EspressoTemplate のアトリビュート`execute`のオーバーライド(ソースの`batchexecute`を参照)

### 使い方
基本は`ase.calculator.espresso`と同じ
- [ASE公式ドキュメント:Espresso](https://www.google.com/search?q=ase+qe&oq=ase+&gs_lcrp=EgZjaHJvbWUqDggBEEUYJxg7GIAEGIoFMgYIABBFGDsyDggBEEUYJxg7GIAEGIoFMg4IAhBFGCcYOxiABBiKBTIHCAMQABiABDIJCAQQABgEGIAEMgwIBRAAGAQYsQMYgAQyCQgGEAAYBBiABDIJCAcQABgEGIAEMgkICBAAGAQYgAQyCQgJEAAYBBiABNIBCTU1MTJqMGoxNagCCLACAQ&sourceid=chrome&ie=UTF-8) を見よ。

`EspressoProfile`の作成について変更があるので注意。

```python
#SlurmShオブジェクトの作成
obj=SlurmSh(dir='path/to/shdir',filename='qebatch')
obj.set_batch(p="gr19999b",t="24:00:00",rsc='p=108:t=1:c=1:m=4G',o='output/%x.%j.out',e='output/%x.%j.err')
obj.set_command('srun pw.x -nk 3 -nt 6 -nd 6 < ./espresso.pwi > ./espresso.pwo')

#BatchEspressoProfileオブジェクトの作成の作成
profile = BatchEspressoProfile(
    pseudo_dir='path/to/pseudodir',
    slshobj=obj
)
```

このように`profile`に`SlurmSh`オブジェクトを含めることにより、バッチ処理で計算が行われるようになる。