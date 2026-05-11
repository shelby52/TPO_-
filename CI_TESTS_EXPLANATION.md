# Как у меня работает автозапуск тестов и CI/CD

Этот файл объясняет, как именно в текущем проекте устроен автоматический запуск тестов в GitHub и деплой на GitHub Pages.

## 1) Что значит "автодобавление тестов на git"

Технически GitHub **не добавляет** тесты в репозиторий сам.  
Реально происходит следующее:

1. Ты один раз кладешь в проект:
   - файл workflow: `.github/workflows/ci.yml`
   - сами тесты: `tests/test_ui.py` (и `tests/conftest.py`)
2. Коммитишь и пушишь эти файлы в репозиторий.
3. После каждого `push`/`pull_request` GitHub Actions автоматически запускает workflow и выполняет тесты.

То есть автоматизация касается **запуска**, а не создания тестов.

---

## 2) Что делает `ci.yml` в этом проекте

Файл: `.github/workflows/ci.yml`

Он содержит 2 job:

- `test` — CI (прогон автотестов)
- `deploy` — CD (публикация на GitHub Pages)

### Когда workflow стартует

```yaml
on:
  push:
  pull_request:
```

Это означает:
- запускается на любой `push` в любую ветку,
- запускается на любой Pull Request.

---

## 3) Как работает job `test` (CI)

Шаги `test`:

1. `actions/checkout@v4` — скачивает код репозитория на GitHub runner.
2. `browser-actions/setup-edge@v1` — ставит Edge на runner.
3. `actions/setup-python@v5` — ставит Python 3.12 + кэширует `pip`.
4. `pip install -r requirements.txt` — ставит зависимости.
5. `pytest -v tests/` — запускает все тесты из папки `tests`.

Если хотя бы один тест упал, job `test` = failed.

---

## 4) Как работают сами UI-тесты

Файл: `tests/test_ui.py`

Ключевые моменты:

- используется `webdriver.Edge(...)`,
- режим `--headless=new`, поэтому браузерное окно не показывается,
- Selenium Manager сам подтягивает `msedgedriver`,
- проверяются:
  1. заголовок и `h1`,
  2. видимость и текст кнопки,
  3. ввод в поля формы,
  4. текст "Спасибо" после отправки.

---

## 5) Как работает job `deploy` (CD)

`deploy` запускается только если:

1. `test` успешен (`needs: test`),
2. это `push` в `main`:

```yaml
if: github.ref == 'refs/heads/main' && github.event_name == 'push'
```

Шаги `deploy`:

1. `checkout`
2. `actions/configure-pages@v5`
3. `actions/upload-pages-artifact@v3` с `path: public`
4. `actions/deploy-pages@v4`

Итог: на Pages публикуется содержимое папки `public`.

---

## 6) Как это связано с ветками `fix -> dev -> main`

Рекомендуемый процесс:

1. Работаешь в `fix`.
2. Делаешь PR `fix -> dev`.
3. На PR автоматически бежит `test`.
4. Если зелено, мерджишь в `dev`.
5. Делаешь PR `dev -> main`.
6. После merge в `main`:
   - снова идет `test`,
   - при успехе автоматически идет `deploy`.

---

## 7) Что смотреть на GitHub

- Вкладка **Actions**:
  - workflow `CI`,
  - статус job `test` и `deploy`.
- Вкладка **Settings -> Pages**:
  - source = GitHub Actions,
  - ссылка на опубликованный сайт.

---

## 8) Быстрая диагностика

Если тесты не стартуют локально:

1. Активируй окружение:
   `.\.venv\Scripts\Activate.ps1`
2. Переустанови зависимости:
   `pip install -r requirements.txt`
3. Запусти:
   `pytest -v tests`

Если в GitHub `deploy` не запускается:

- проверь, что был именно `push` в `main`,
- проверь, что `test` прошел успешно,
- проверь `Settings -> Pages` (источник GitHub Actions).

