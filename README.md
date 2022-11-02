# public_filler

## Это Telegram бот сделан для отправки контента в канал.
После запуска он принимает Картинки,Видео и Анимации в автоматическом режиме.

## Install
Клонируем репозиторий или качаем код.

### В файле data\config.py вы должны указать свои данные
```python
<token="your_bot_token"  - токен бота
chat_link = 'your_chat_link' - ссылка на канал формата https://t.me/канал
channel_id = 'your_channel_id' - id этого же канала
admin_id = 'your_id' - Ваш персональный id
send = f'<a href="{chat_link}">*your_chanel_name*</a>' - подпись. в поле *your_chanel_name* прописать название вашего канала
```
## Start
Переходим в папку куда вы распаковали код или подключаем ее через GIt.
<p>Запускаем virtual environment и запускаем выполнение бота

```bash
venv\Scripts\activate
python start.py
```


### Запуск отправки сообщений в канал:
<p>После запуска бот покажет привественное сообщение и после этого пишем боту 2 сообщения

#### 1ое сообщение:
<p>Время и цифру чтобы указать промежуток отправки постов. 
 
#### Пример помежутка  5 минут:
 ```python
 Время 5
 ```

#### 2ое сообщение:
<p>Задержка и цифру (не стоит ставить сильно большую цифру). 
<p>Параметр предназначен для создания эффекта случайного времени отправки 
 
#### Пример разброса в пределах 3 минут
 ```python
 Задержка 3
  ```
<p>После этого нажать кнопку 'Запустить отправку' или написать этоже ручками
<p>Отправка запустится и Покажет пост как он будет выглядеть в канале.
<p>Остаток постов в базе и время когда будет отправлен.

 ![image](https://user-images.githubusercontent.com/10975524/199413182-1201d8ae-31ef-4bba-9f65-caeaa743dae2.png)

<p>Остановка бота(остановка отправки):
<p>Нажимаем кнопку 'Остановить отправку'(так же можно прописать текст вручную)
<p>Бот продолжит принимать контент, но отправлять до следующего нажатия 'Запустить отправку' ничего не будет
<p>В этом моменте можно поменять параметры Время и Задержка
