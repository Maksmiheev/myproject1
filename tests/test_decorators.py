import unittest
import os
import sys
from io import StringIO
from src.decorators import log


class TestLogDecorator(unittest.TestCase):

    def test_console_logging_success(self):
        output = StringIO()
        sys.stdout = output

        @log()
        def add(a, b):
            return a + b

        result = add(5, 7)
        sys.stdout = sys.__stdout__

        self.assertEqual(result, 12)
        log_output = output.getvalue()
        self.assertIn("Начало выполнения функции: add", log_output)
        self.assertIn("Функция add успешно выполнена. Результат: 12", log_output)
        self.assertIn("Конец выполнения функции: add", log_output)

    def test_console_logging_error(self):
        output = StringIO()
        sys.stdout = output

        @log()
        def div(a, b):
            return a / b

        with self.assertRaises(ZeroDivisionError):
            div(10, 0)

        sys.stdout = sys.__stdout__
        log_output = output.getvalue()

        self.assertIn("Начало выполнения функции: div", log_output)
        self.assertIn("Ошибка в функции div: ZeroDivisionError", log_output)
        self.assertIn("Входные параметры: 10, 0", log_output)
        self.assertIn("Трассировка ошибки", log_output)
        self.assertIn("Конец выполнения функции: div", log_output)

    def test_file_logging_success_and_error(self):
        log_filename = "test_log.log"
        if os.path.exists(log_filename):
            os.remove(log_filename)

        @log(log_filename)
        def mul(a, b):
            if not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
                raise TypeError("Оба параметра должны быть числами")
            return a * b

        # Успешный вызов
        result = mul(3, 4)
        self.assertEqual(result, 12)

        # Ошибочный вызов
        with self.assertRaises(TypeError):
            mul(3, "oops")

        # Читаем файл с логами
        with open(log_filename, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Начало выполнения функции: mul", content)
        self.assertIn("Функция mul успешно выполнена. Результат: 12", content)
        self.assertIn("Ошибка в функции mul: TypeError", content)
        self.assertIn("Входные параметры: 3, 'oops'", content)
        self.assertIn("Трассировка ошибки", content)

        os.remove(log_filename)

    if __name__ == "__main__":
        unittest.main()