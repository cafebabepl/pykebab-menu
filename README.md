# pykebab-menu
mikrousługa do zwracania menu w ramach projektu pykebab (kebab 2.1)

Aplikacja zainstalowana jest w serwisie https://www.pythonanywhere.com/

Usługa dostępna jest pod adresem http://wkozi.pythonanywhere.com/menu

### Programowanie
mikroframework Flask http://flask.pocoo.org/

```
set FLASK_APP=flask_app.py
set FLASK_ENV=development
flask run
```

### Instalacja i konfiguracja
instalacja biblioteki 
`pip3.7 install --user scrapinghub`

zdefiniowanie zadania
`curl -u API_KEY: https://app.scrapinghub.com/api/run.json -d project=355230 -d spider=camel-pizza -d add_tag=pythonanywhere-task`
