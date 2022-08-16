# FairWind Portal

## 使い方

以下を順番にターミナルで実行してください。
Python のバージョンは、`3.9.13` を推奨します。

```
git clone https://github.com/vvihar/fw_djangoapp
cd fw_djangoapp
python3 -m venv env
source env/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cd fwappproject
python generate_local_settings.py
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

`python manage.py createsuperuser`を実行すると、ユーザー名、メールアドレス、パスワードが尋ねられるので、それぞれ適切に入力してください。

最後に`python manage.py runserver`を実行するとサーバーが立ち上がります。その後は以下の手順に従ってください。

1. `http://127.0.0.1:8000/admin`にアクセスし、ログインしてください。
2. 「認証と認可」→「ユーザー」をクリックしてください。
3. 先ほど作った `superuser` のユーザー名をクリックしてください。
4. 「個人情報」→「姓」「名」、およびページ下部の「ユーザー」の各項目に入力し、保存してください。
    - 「ユーザー」→「学部」「学科」「班」「担当」は空欄でも構いません。
    - この操作を行わないと、特定のページを表示したときにエラーとなります。
5. 準備が整いました。`http://127.0.0.1:8000/` にアクセスしてみてください。