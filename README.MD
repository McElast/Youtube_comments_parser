# ENGLISH (Русский туториал дан ниже)
-----------------------------------
# DESCRIPTION
This script can be used for collecting YouTube comments from any video, stream. 
Based on Selenium and ChromeDriver.
Useful for videos with big amount of commentaries (not suitable for huge amount of videos - may be slow).
Output file - txt.
You can use it without registration on YouTube.
Autoplay video and autoswitch to next video will be escaped.
-------------------------------------
You will get in txt file:
- video URL
- title
- likes / dislikes
- total number of views
- publication date
- description
- chanel name
- amount of subscribers
- comments expanded in tree-mode (for readability)
Works with python 3.8.1
-------------------------------------
# How to USE
- download Selenium ('pip install -U selenium')
- download ChromeDriver (it should equals you version of ChromeBrowser) - 
    https://chromedriver.chromium.org/downloads
    and put it in same directory with main.py
- paste your URL in parse function
- choose your language or make you own (will be described below)
- run script in CONSOLE or PyCharm or any editor you prefer
-------------------------------------
# Language settings
You should use language version of your ChromeBrowser (default value is Russian)
If you settings are for English - you must change optional arg to EN (in 7 places)
If your language differs from RU or EN - just create new tuple at the beginning with desired elements

--------------------------------------
THNX for using.

# Русский туториал
--------------------------------------
# Описание 
Скрипт сделан для автоматического сбора комментариев под Ютуб видео.
Не очень подходит для массового потока роликов с малым количеством комментариев 
(не так быстро, так как используется Selenium), зато собрать несколько тысяч ответов под одним роликом - 
очень удобно.
Работает с python 3.8.1
На выходе - получите файл (текстовый) древовидной структуры (все посты легко вычленяются).
Для пользования скриптом - не нужна регистрация, API.
Автовоспроизведение видео будет поставлено на паузу, также как и переключение на другой ролик 
после окончания текущего.

В текстовом файле будет собрана информация:
- канал
- подписчики
- ссылка на видео
- количество просмотров
- лайки \ дизлайки
- дата публикации
- описание под видео
- комментарии с ответами
----------------------------------------
# Как пользоваться
- скачайте Selenium ('pip install -U selenium')
- скачайте ХромДрайвер (https://chromedriver.chromium.org/downloads) и положите
    его в директорию с файлом main.py (версия драйвера должна совпадать с версией вашего браузера)
- настройте язык (по умолчанию используется русский)
- вставьте ссылку на видео (внизу, в функцию parse)
- запустите main.py в консоли или любом редакторе
----------------------------------------
# Настройки языка
Описаны на английском языке выше. Если вам нужен иной язык, то, думаю, разберетесь.
----------------------------------------
Пожелания и предложения - приветствуются
