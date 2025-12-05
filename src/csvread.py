import pandas as pd


def read_financial_csv(file_path):
    """
    Читает финансовый CSV-файл и возвращает список словарей с операциями.
    """
    try:
        df = pd.read_csv(file_path)
        operations_list = df.to_dict('records')
        return operations_list
    except Exception as e:
        print(f'Ошибка при чтении файла {file_path}: {e}')
        return []


def read_financial_xlsx(file_path):
    """
    Читает финансовый Excel-файл и возвращает список словарей с операциями.
    """
    try:
        df = pd.read_excel(file_path)
        operations_list = df.to_dict('records')
        return operations_list
    except Exception as e:
        print(f'Ошибка при чтении файла {file_path}: {e}')
        return []




