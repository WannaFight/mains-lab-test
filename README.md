# MainsLab Test task

# Stack
Python 3.10, Django 4.1 + DRF

## Task
1. эндпоинт для обработки файла bills.xlsx

В базу писать только валидные счета. Счет считается валидным, если выполнены все условия:
-	значение sum является числом
-	в service не пусто ( пусто так же считается, если вместо текста знак “-”)
-	корректная дата (дата считается корректной, если есть день, месяц и год).
-	№(номер счет) тип  int
-	client_name, client_org не пустые

2. эндпоинт со списком счетов с возможностью фильтровать по организации, клиенту.
3. У клиентов могут быть специфичные названия колонок в файле bills. То есть набор колонок везде одинаковый, но названия и порядок могут отличаться.
4. Создать модель `ServiceClass` с аттрибутами: `name` (str), `code` (int)
5. При загрузке файла bills.xlsx колонку service нужно рандомно сопоставлять с записью из модели `ServiceClass`
6. В эндпоинт со списком счетов (из первой части задания) добавить вывод значения name



## Run
```shell
docker-compose up
```

## API
`:8000/swagger/` - docs
`:8000/api/bills/upload-excel/` - endpoint to upload excel file, process it and create instances in db \
`:8000/api/bills/[?client_name=...][&client_org=...]` - endpoint for retrieving bills and optionally filter them by client name or client org