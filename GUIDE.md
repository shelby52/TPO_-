# Лабораторная 11: полный пошаговый гайд (CI/CD, тесты, GitHub Pages)

Документ привязан к **текущему содержимому папки проекта** и профилю на GitHub.

**Твой аккаунт:** [github.com/Xutrikk](https://github.com/Xutrikk)

**Значения по умолчанию в командах ниже:**

| Параметр | Значение |
|----------|----------|
| Логин (owner) | `Xutrikk` |
| Имя репозитория | `TPO-lab11` |
| HTTPS remote | `https://github.com/Xutrikk/TPO-lab11.git` |
| После включения Pages (проектный сайт) | `https://xutrikk.github.io/TPO-lab11/` |

Если при создании репозитория на GitHub укажешь **другое имя** — замени везде `TPO-lab11` на своё имя.

**Git email** — свой (тот же, что в настройках GitHub, или любой указанный в `git config`):

```powershell
git config --global user.email "<твой email>"
git config --global user.name "Kirill"
```
(имя можно написать и по-другому — как удобно в коммитах.)

Все команды для консоли ниже для **PowerShell** и пути **`C:\BSTU\SEM6\TPO\lab11`**. Если у тебя другой диск или папка — замени путь.

---

## Что уже подготовлено в этом проекте (связь с пунктами методички)

| Пункт методички | Что лежит в репозитории |
|-----------------|-------------------------|
| 1. Простая веб-страница (форма) | `public\index.html` |
| 3. 3–4 UI-теста (Selenium) | `tests\test_ui.py` (4 теста), вспомогательно `tests\conftest.py` |
| 4. GitHub Actions при push | `.github\workflows\ci.yml` |
| 10–11. Деплой на GitHub Pages только после успешных тестов на `main` | В `ci.yml`: job `deploy` с `needs: test` и условием ветки `main` |

Тесты запускаются в **Microsoft Edge** (локально достаточно установленного Edge; отдельная папка с драйвером не нужна — Selenium 4 подтягивает драйвер сам).

---

## Подготовка Git на компьютере (один раз)

Проверка, что Git установлен:

```powershell
git --version
```

Если Git нет — установи [Git for Windows](https://git-scm.com/download/win).

Один раз (если ещё не настраивал):

```powershell
git config --global user.name "Kirill"
git config --global user.email "<твой email>"
```

---

## Задание 1. Веб-страница (форма)

**Уже сделано в проекте:** открой в браузере файл `public\index.html` (двойной клик или перетащи в Edge).

Проверка вручную:

1. Открылась страница с заголовком «Форма обратной связи».  
2. Есть поля Имя, Электронная почта, Комментарий и кнопка «Отправить сообщение».  
3. После «отправки» появляется зелёный блок со словом «Спасибо».

Если преподаватель требует **свою** надпись — правь текст в `public\index.html`; если меняешь текст кнопки или заголовка, обнови тесты в `tests\test_ui.py`, чтобы они проверяли новые строки.

---

## Задание 2. Репозиторий на GitHub и ветки `main`, `dev`, `fix`

Смысл методички: **`main`** — стабильная ветка, **`dev`** — основная для разработки, **`fix`** — ветка для правок задачи (иногда создают от `dev` отдельную ветку на каждую задачу, например `fix/форма-текст` — уточни у преподавателя формат имени).

### Шаг A. Создать пустой репозиторий на GitHub

1. Зайди на [github.com/new](https://github.com/new) под аккаунтом **Xutrikk**.  
2. **Repository name:** **`TPO-lab11`** (или своё имя — тогда поправь URL в следующих блоках команд).  
3. Выбери **Public**.  
4. **Не** включай галочки «Add a README», «Add .gitignore» (чтобы первый push не конфликтовал; или включи README и тогда на первом `git pull` разрули конфликт — проще без них).  
5. Нажми **Create repository**.  
6. На странице репозитория скопируй HTTPS:

   **`https://github.com/Xutrikk/TPO-lab11.git`**

### Шаг B. Первый коммит и отправка в `main`

Открой PowerShell и выполни по очереди:

```powershell
cd C:\BSTU\SEM6\TPO\lab11
git init -b main
git status
git add .
git commit -m "feat: страница формы, тесты Selenium, CI и деплой на Pages"
git remote add origin https://github.com/Xutrikk/TPO-lab11.git
git push -u origin main
```

Если `git remote add` ругается, что remote уже есть:

```powershell
git remote remove origin
git remote add origin https://github.com/Xutrikk/TPO-lab11.git
```

Если запросят логин/пароль — для GitHub используй **Personal Access Token** вместо пароля (Settings → Developer settings → Personal access tokens), либо войди через **Git Credential Manager**.

### Шаг C. Создать ветки `dev` и `fix` и отправить на GitHub

```powershell
cd C:\BSTU\SEM6\TPO\lab11
git branch dev
git push -u origin dev
git branch fix
git push -u origin fix
```

Проверка на GitHub: **Code** репозитория [github.com/Xutrikk/TPO-lab11](https://github.com/Xutrikk/TPO-lab11) → выпадающий список веток — должны быть **main**, **dev**, **fix**.

---

## Задание 3. Автотесты UI (Selenium), локальный запуск

### Шаг A. Виртуальное окружение Python

```powershell
cd C:\BSTU\SEM6\TPO\lab11
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Если политика запрещает скрипты:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Повтори активацию:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Шаг B. Установка зависимостей

```powershell
pip install -U pip
pip install -r requirements.txt
```

### Шаг C. Запуск тестов

Должен быть установлен **Microsoft Edge** (на Windows обычно уже есть).

```powershell
pytest -v tests
```

Ожидается: **4 passed**.  
Если ошибка про драйвер или браузер — обнови Edge и Selenium (`pip install -U selenium`), при отсутствии интернета Selenium не сможет скачать драйвер.

Деактивация venv (когда закончишь):

```powershell
deactivate
```

---

## Задание 4. GitHub Actions — автозапуск тестов при отправке в репозиторий

**Уже сделано:** файл `.github\workflows\ci.yml`.

Что он делает:

- При каждом **`push`** и при каждом **`pull_request`** запускается job **`test`**: checkout, установка Edge на раннере Linux, Python, `pytest`.  
- Job **`deploy`** (GitHub Pages) выполняется **только** при **`push` в `main`** и **только если `test` успешен** (`needs: test`).

После первого `push`:

1. Открой [Actions в репозитории](https://github.com/Xutrikk/TPO-lab11/actions).  
2. Выбери workflow **CI**.  
3. Убедись, что последний запуск **зелёный** (успешный).

---

## Задание 5. Убедиться, что при ошибке в коде тесты падают

Цель: показать преподавателю, что CI «ловит» поломку.

### Вариант (простой): сломать `id` у кнопки

1. Открой `public\index.html`, найди кнопку:

   `id="submit-btn"`

2. Временно замени, например, на `id="submit-btn-broken"`.

3. Сохрани файл, коммит и push (например, в ветку `fix` — см. сценарий ниже):

```powershell
cd C:\BSTU\SEM6\TPO\lab11
git checkout fix
git pull origin fix
git add public\index.html
git commit -m "temp: сломать id кнопки для проверки CI"
git push origin fix
```

4. На GitHub открой **Actions** — последний прогон для этой ветки должен быть **красным** (failed).  
5. Верни **`id="submit-btn"`**, снова commit + push:

```powershell
git add public\index.html
git commit -m "fix: восстановить id кнопки для тестов"
git pull origin fix
git push origin fix
```

После восстановления тесты снова должны проходить.

---

## Задание 6. Работа с ветками без прямых коммитов в `main`

Правило: **в `main` не коммить рабочие изменения напрямую** с рабочего ПК для отчётного процесса. Разрабатываешь в **`dev`** или **`fix`** (или feature-ветках от `dev`), а в **`main`** попадаешь через **Pull Request**.

На практике для учебной сдачи последовательность такая:

1. Изменения делаются в **`fix`** (или от `fix` можно отвести задачную ветку).  
2. PR **`fix` → `dev`**, merge.  
3. PR **`dev` → `main`**, merge — после этого возможен деплой на Pages (см. ниже).

---

## Задание 7. Сценарий: `fix` → PR в `dev` → PR в `main`

Командная последовательность на ПК может выглядеть так.

### Часть 1 — правка кода во ветке `fix`

```powershell
cd C:\BSTU\SEM6\TPO\lab11
git fetch origin
git checkout fix
git pull origin fix
git merge origin/dev
```

Если конфликт — разрули в редакторе, затем:

```powershell
git add .
git commit -m "merge dev into fix"
```

Сделай **осмысленное изменение** для отчёта (пример — поменяй текст кнопки и тест):

1. В `public\index.html` измени текст кнопки с «Отправить сообщение» на что-то своё.  
2. В `tests\test_ui.py` в тесте `test_submit_button_is_visible` обнови проверку текста кнопки под новую строку.

Затем:

```powershell
git add public\index.html tests\test_ui.py
git commit -m "fix: изменить текст кнопки и тест"
git push origin fix
```

### Часть 2 — Pull Request на GitHub: `fix` → `dev`

1. Репозиторий: **[Xutrikk/TPO-lab11](https://github.com/Xutrikk/TPO-lab11)**.  
2. Быстрое сравнение для PR: [**Compare fix → dev**](https://github.com/Xutrikk/TPO-lab11/compare/dev...fix) (или **Pull requests** → **New pull request**).  
3. **base:** `dev`, **compare:** `fix`.  
4. Создай PR, дождись **проверок Actions** (должны быть зелёными).  
5. Нажми **Merge pull request** → подтверди merge.  
6. Локально обнови `dev`:

```powershell
git checkout dev
git pull origin dev
```

### Часть 3 — Pull Request: `dev` → `main`

1. Сравнение для PR: [**Compare dev → main**](https://github.com/Xutrikk/TPO-lab11/compare/main...dev).  
2. **base:** `main`, **compare:** `dev`.  
3. Создай PR, дождись успешного CI.  
4. **Merge** в `main`.  
5. Локально:

```powershell
git checkout main
git pull origin main
```

После merge в `main` в **Actions** должен пройти **test**, затем **deploy** (если настроены Pages).

---

## Задания 10–11. GitHub Pages и деплой только после успешных тестов на `main`

### Шаг A. Включить публикацию через Actions

1. Открой [Settings → Pages](https://github.com/Xutrikk/TPO-lab11/settings/pages) для **TPO-lab11**.  
2. **Build and deployment** → **Source:** выбери **GitHub Actions** (не «Deploy from a branch» для этого сценария).  
3. Сохрани, если нужно подтвердить настройку.

При первом деплое интерфейс может попросить разрешить **GitHub Actions** и окружение **github-pages** — согласись.

### Шаг B. Убедиться, что деплой привязан к `main` и тестам

В `.github/workflows/ci.yml` уже задано:

- `deploy` имеет **`needs: test`** — без успешных тестов деплой не выполнится.  
- **`if: github.ref == 'refs/heads/main' && github.event_name == 'push'`** — деплой **только при push в `main`**.

После успешного **deploy** проект будет доступен по адресу (регистр в поддомене не важен):

**`https://xutrikk.github.io/TPO-lab11/`**

Открой эту страницу в браузере; точную ссылку после деплоя дублирует блок **Pages** и job **deploy** в Actions.

### Шаг C. Если деплой не появился

1. **Actions** → последний запуск на `main`: убедись, что **оба** job `test` и `deploy` успешны.  
2. **Settings** → **Pages** — проверь, что источник **GitHub Actions**.  
3. Подожди 1–3 минуты и обнови страницу сайта с принудительным обновлением кэша (Ctrl+F5).

---

## Контрольный чеклист перед сдачей отчёта

- [ ] Репозиторий на GitHub создан, есть ветки **`main`**, **`dev`**, **`fix`**  
- [ ] Локально `pytest -v tests` — **все зелёные**  
- [ ] На GitHub в **Actions** workflow **CI** проходит для PR / push  
- [ ] Был эксперимент: **нарочная поломка** → CI **красный** → **исправление** → CI зелёный  
- [ ] Выполнен сценарий **PR fix→dev** и **PR dev→main** (скрины для отчёта)  
- [ ] **Pages** включены, сайт открывается по ссылке с GitHub  
- [ ] После ошибки тестов в `main` деплей **не** должен считаться успешным следующим шагом (deploy не выполнится без `test`)

---

## Краткая шпаргалка команд (повтор каждого раза перед работой)

```powershell
cd C:\BSTU\SEM6\TPO\lab11
git fetch origin
git checkout ИМЯ-ВЕТКИ
git pull origin ИМЯ-ВЕТКИ
# правки файлов...
git add .
git commit -m "кратко: что сделано"
git push origin ИМЯ-ВЕТКИ
```

Проверка ветки:

```powershell
git branch
```

---

Если нужно, распечатай этот файл или приложи **`GUIDE.md`** к отчёту как описание действий для преподавателя.
