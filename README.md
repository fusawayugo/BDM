# BDM
## 実行方法
### bluetoothの設定

学科PC/find_bt.pyを実行してmicrobitに割り当てられたUUIDを確認

学科PC/main.pyのtarget_adressをそのUUIDにする

### bluetoothの設定が終わったら

/BDM以下のmain.pyはmac用

ubuntuで実行するときは学科PC/以下のmain.pyを使う

windowsは作ってない

適切なディレクトリに移動して
```
python3 main.py
```
で起動する

ctrl+Cで切れる

## バージョン(念の為)

- Ubuntu
```
python 3.8.10

bleak 0.21.0
numpy 1.24.4
pyautogui 0.9.54
```
他になにか忘れてるかも



### 仮想環境の立て方（gitリポジトリの外で作成）
```
python3 -m venv (仮想環境名)
```
・立ち上げ
```
source (仮想環境名)/bin/activate
```
・切る
```
deactivate
```


UUIDのまとめサイト  
https://tomari.org/main/microbit/uuid.txt


