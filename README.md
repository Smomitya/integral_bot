# Telegram бот для оттачивания навыков взятия интегралов.
Для использования нужно запустить контейнер docker. Я всё настраивал на локальном сервере и использовал сервис ngrok для подключения к внешней сети.
Cначала нужно сконфигурировать ngrok:
```$ ngrok config add-authtoken {ngrok_token}
```
Перед запуском самого приложения пробрасываем порты:
```$ ngrok http 5000
$ curl --location --request POST 'https://api.telegram.org/bot{tg_bot_token}/setWebhook' \
--header 'Content-Type: application/json' \
--data-raw '{"url": "{ngrok_address}"}'
```
Ключи `tg_bot_token` и `ngrok_token` лежат в соответствующих файлах. `ngrok_address` получаем из терминала, в котором запустили первую команду.
Для проверки работоспособности: бота можно найти `@study_integrals_bot`. Управление довольно нативное. Предлагается решить набор интегралов.
Как только всё будет решено, пользователя похвалят. Приложение допускает добавление новых файлов по мере прохождения методов интегрирования в институте. Будучи честным, сразу скажу - запустить ngrok из контейнера у меня не удалось. Много потратил времени, но всё время натыкался на проблемы.