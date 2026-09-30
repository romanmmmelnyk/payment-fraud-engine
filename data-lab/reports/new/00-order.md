# Новий датасет

Файл для аналізу: `data-lab/datasets/new/train.csv`. У `test.csv` мітки немає, тому той самий ланцюжок на ньому не рахується.

Колонки файлу зіставлені з попереднім розбором так: `user_id` це клієнт, `label` це fraud, `country` це місце, `merchant_category` це категорія, `device_id` це пристрій замість картки, `channel` це окреме поле з двома значеннями. `timestamp` взятий як секунди.

Запуск: `data-lab\.venv\Scripts\python.exe data-lab\analyze_new.py`.
