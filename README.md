# Симулятор кассового аппарата

## Стек технологий:
- python 3.10
- Django
- Django Rest Framework
- библиотека qrcode
- библиотека pdfkit
- библиотека jinja2

## Системные требования к запуску:
- python 3.10
- wkhtmltox для создания pdf-файлов

## Порядок запуска:
1. Склонируйте репозиторий
```
git clone https://github.com/mosevaa/generating_receipts
```
2. Установите зависимости приложения
```
python -m venv venv
pip install -r requirements.txt
```
3. Выполните миграции базы данных
```
python manage.py migrate
```
4. Запустите приложение
```
python manage.py <host>:<port>
```

## Краткое описание работы приложения
При заполненной продуктами базе данных необходимо отправить POST запрос на адрес `http://<host>:<port>/cash_machine` c телом вида
```json
{
	"items": [1, 2, 3]
}
```
где items - это массив id товаров. Сервер формирует чек в формате pdf и отправляет, как ответ, QR-код, по которому можно открыть этот чек.