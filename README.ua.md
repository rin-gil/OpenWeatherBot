<p align="center">
    <img src="https://repository-images.githubusercontent.com/559574279/ac1f8317-c07c-4c0f-a4e4-c49ae01237cd" alt="Open Weather Bot" width="640">
</p>

<p align="center">
    <a href="https://www.python.org/downloads/release/python-3108/">
        <img src="https://img.shields.io/badge/python-v3.10-informational" alt="python version">
    </a>
    <a href="https://pypi.org/project/aiogram/2.23.1/">
        <img src="https://img.shields.io/badge/aiogram-v2.23.1-informational" alt="aiogram version">
    </a>
    <a href="https://pypi.org/project/aiohttp/3.8.3/">
        <img src="https://img.shields.io/badge/aiohttp-v3.8.3-informational" alt="aiohttp version">
    </a>
    <a href="https://pypi.org/project/aiosqlite/0.17.0/">
        <img src="https://img.shields.io/badge/aiosqlite-v0.17.0-informational" alt="aiosqlite version">
    </a>
    <a href="https://pypi.org/project/APScheduler/3.9.1.post1/">
        <img src="https://img.shields.io/badge/APScheduler-v3.9.1.post1-informational" alt="APScheduler version">
    </a>
    <a href="https://pypi.org/project/environs/9.5.0/">
        <img src="https://img.shields.io/badge/environs-v9.5.0-informational" alt="environs version">
    </a>
    <a href="https://pypi.org/project/Pillow/9.3.0/">
        <img src="https://img.shields.io/badge/Pillow-v9.3.0-informational" alt="Pillow version">
    </a>
    <a href="https://github.com/psf/black">
        <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-black.svg">
    </a>
    <a href="https://github.com/rin-gil/OpenWeatherBot/actions/workflows/tests.yml">
        <img src="https://github.com/rin-gil/OpenWeatherBot/actions/workflows/tests.yml/badge.svg" alt="Code tests">
    </a>
    <a href="https://github.com/rin-gil/OpenWeatherBot/actions/workflows/codeql.yml">
        <img src="https://github.com/rin-gil/OpenWeatherBot/actions/workflows/codeql.yml/badge.svg" alt="Code tests">
    </a>
    <a href="https://github.com/rin-gil/OpenWeatherBot/blob/master/LICENCE">
        <img src="https://img.shields.io/badge/licence-MIT-success" alt="MIT licence">
    </a>
</p>

<p align="right">
    <a href="https://github.com/rin-gil/OpenWeatherBot/blob/master/README.md">
        <img src="https://raw.githubusercontent.com/rin-gil/rin-gil/main/assets/img/icons/flags/united-kingdom_24x24.png" alt="En"></a>
    <a href="https://github.com/rin-gil/OpenWeatherBot/blob/master/README.ru.md">
        <img src="https://raw.githubusercontent.com/rin-gil/rin-gil/main/assets/img/icons/flags/russia_24x24.png" alt="Ru">
    </a>
</p>

## Open Weather Bot

????????????????-??????, ???????? ?????????????? ?????????????? ????????????.
???????????? ???????????? ???????????????? ???? ???????????????????? [@OpenWeatherSmartBot](https://t.me/OpenWeatherSmartBot)

### ????????????????????

* ?????????? ?????????? ???? ???????????? ?????? ????????????????????????
* ?????????? ???????????????? ???????????? ???? ???????????????? ???? 24 ????????????
* ?????????????????? ???????????????? ???????????? ?????????? 3 ????????????

### ????????????????????????

```
git clone https://github.com/rin-gil/OpenWeatherBot.git
cd OpenWeatherBot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mv .env.dist .env
```

<img align="right" width="300" src="https://raw.githubusercontent.com/rin-gil/rin-gil/main/assets/img/projects/OpenWeatherBot/screenshot_ua.png" alt="???????????????? ?????????? OpenWeatherBot">

### ???????????????????????? ???? ????????????

* ???????????????????????? ???????????? ???????? ?? [@BotFather](https://t.me/BotFather) ?? ?????????????????? ?????????????????? ??????????
* ?????????????? ?????????? ???????? ?? ???????? .env
* ???????????????????????? ?????????????????? ?????????? ???? ?????????? [OpenWeatherMap](https://home.openweathermap.org/users/sign_in)
* ???????????????? [API ????????](https://home.openweathermap.org/api_keys) ?? ?????????????????? ???????? ?? ???????? .env
* ?????????????? ???????? id ???????????????? ?? ???????? .env
* ?????????????????? ???????? id ??????????, ??????????????????, ?????????????????? ???????? [@getmyid_bot](https://t.me/getmyid_bot)
* ???????????? ???????? ?????????? ???????? bot.py `python bot.py`

### ??????????????????????

* ?? ???????????? 1.1.0 ?? ?????? ???????????? ?????????????????????? ?????? ??????????????????????, ?????????????????????? ???? ???????????????????? ????????
* ?????? ?????????????????? ?????????????????? ???? ???????? ????????, ?????????????? ????????????????:
  1. ?????????????????? ?? ?????????? ?? ??????????
  2. ?????????????????? ???????????????????? ????????????????:

     `source venv/bin/activate`
  3. ???????????????? ???????? ?????????????????? ???? ???????? ????????, ???? **{language}** - ?????? ???????? ???? ???????????????????? [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)

     `pybabel init --input-file=tgbot/locales/tgbot.pot --output-dir=tgbot/locales --domain=tgbot --locale={language}`
  4. ?????????????????????? ?????????? ?? ?????????? **locales/{language}/LC_MESSAGES/tgbot.po**
  5. ?????????????????????? ???????????????? ????????????????:

     `pybabel compile --directory=tgbot/locales --domain=tgbot`
  6. ?????????????????????????? ????????
* ?????? ???????????? ???????????? ?????? ?????????????????? ?? ????????, ?????? ???????????????? ???????? ???????????????? ???????????????????????? ?? ???????????????????????? ?????????? 
  ?????????????????? ?????? ???????? ??????????????????????:
  1. ?????????????? ?????????? ?????? ?????????????????? ?? ????????:

     `pybabel extract --input-dirs=./tgbot --output-file=tgbot/locales/tgbot.pot --sort-by-file --project=OpenWeatherBot`
  2. ???????????????? ?????????? ?????????????????? ?????? ???????? ??????????????????????:

     `pybabel init --input-file=tgbot/locales/tgbot.pot --output-dir=tgbot/locales --domain=tgbot --locale={language}`
  3. ???????????????????????? ??????????????????:

     `pybabel compile --directory=tgbot/locales --domain=tgbot`
* ???????????????????? ?????? ???? ?????????? ?????????????????? ?? ???????????????? ?? ???????????????????????? [aiogram](https://docs.aiogram.dev/en/latest/examples/i18n_example.html)

### ????????????????????

* [Ringil](https://github.com/rin-gil)

### ????????????????

* ???????????????? ?????? **Open Weather Bot** ?????????????????? ???? ?????????????????? [MIT](https://github.com/rin-gil/OpenWeatherBot/blob/master/LICENCE)
* ???????? ?????? ?????????????? ???????????? ???????????? ???????????????? [OpenWeather](https://openweathermap.org/)
* ???????????? ???????????? ?????? [www.wishforge.games](https://freeicons.io/profile/2257) c [freeicons.io](https://freeicons.io/)
