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

## API
`:8000/api/bills/upload-excel/` - endpoint to upload excel file, process it and create instances in db \
`:8000/api/bills/[?client_name=...][&client_org=...]` - endpoint for retrieving bills and optionally filter them by client name or client org