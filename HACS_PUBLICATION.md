# Публикация в HACS

## Готовность репозитория ✅

Репозиторий готов для публикации в HACS! Все требования выполнены:

- ✅ Структура `custom_components/sim2m/`
- ✅ `manifest.json` с зависимостями
- ✅ `hacs.json` для HACS
- ✅ Config flow для настройки через UI
- ✅ Сенсоры с правильными device_class
- ✅ Переводы (ru/en)
- ✅ README с инструкциями
- ✅ LICENSE (MIT)
- ✅ Git репозиторий

## Шаги для публикации

### 1. Создайте GitHub репозиторий

```bash
# Создайте репозиторий на GitHub: https://github.com/new
# Название: sim2m
# Public repository

# Добавьте remote
git remote add origin https://github.com/ifilatov/sim2m.git
git branch -M main
git push -u origin main
```

### 2. Создайте первый Release

1. На GitHub: Releases → Create a new release
2. Tag: `v1.0.0`
3. Title: `v1.0.0 - Initial release`
4. Description:
   ```
   Initial release of Sim2M integration for Home Assistant

   Features:
   - Balance monitoring
   - Traffic monitoring (limit/used/remain/percent)
   - Auto-update every hour
   - Config flow for easy setup
   ```
5. Publish release

### 3. Добавьте в HACS (опционально)

Для добавления в официальный список HACS:

1. Fork репозиторий: https://github.com/hacs/default
2. Отредактируйте файл `integration` (добавьте ваш репозиторий)
3. Создайте Pull Request

**Или используйте как Custom Repository:**

В HACS → Integrations → ⋮ → Custom repositories →
URL: `https://github.com/ifilatov/sim2m`
Category: Integration

### 4. Тестирование

После публикации, проверьте:

1. Установка через HACS
2. Config flow работает
3. Сенсоры появляются
4. Данные обновляются

## Требования HACS

✅ **Обязательно:**
- [x] Public GitHub репозиторий
- [x] `custom_components/<domain>/` структура
- [x] `manifest.json` с правильными полями
- [x] `hacs.json`
- [x] README.md с инструкциями
- [x] Releases (теги)

✅ **Рекомендуется:**
- [x] LICENSE файл
- [x] Config flow
- [x] Переводы
- [x] Device class для сенсоров

## После публикации

Пользователи смогут установить через HACS:

1. HACS → Integrations → Explore & Download Repositories
2. Поиск: "Sim2M"
3. Download
4. Restart Home Assistant
5. Settings → Integrations → Add Integration → Sim2M
6. Ввод токена и ID

## Обновления

Для выпуска новых версий:

```bash
# Внесите изменения
git add .
git commit -m "Update: описание изменений"

# Обновите версию в manifest.json
# version: "1.0.1"

git tag v1.0.1
git push origin main --tags
```

Создайте новый Release на GitHub.

## Поддержка

- Issues на GitHub
- Discussions для вопросов
- Pull Requests приветствуются

---

**Репозиторий готов к публикации!** 🎉
