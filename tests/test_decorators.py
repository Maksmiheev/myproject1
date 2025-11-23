import pytest
import os
import logging
from src.decorators import log

def test_console_logging_success(caplog):
    @log()
    def add(a, b):
        return a + b

    with caplog.at_level(logging.INFO):
        result = add(5, 7)

    assert result == 12

    for rec in caplog.records:
        print(f"{rec.levelname} | {rec.funcName} | {rec.message}")

    assert any("Начало выполнения функции" in rec.message for rec in caplog.records)
    assert any("Функция успешно выполнена. Результат: 12" in rec.message for rec in caplog.records)

def test_console_logging_error(caplog):
    @log()
    def div(a, b):
        return a / b

    with caplog.at_level(logging.INFO):
        with pytest.raises(ZeroDivisionError):
            div(10, 0)

    error_logs = [rec for rec in caplog.records if rec.levelname == "ERROR"]
    assert any("Ошибка: ZeroDivisionError" in rec.message for rec in error_logs)
    assert any("10" in rec.message and "0" in rec.message for rec in error_logs)

def test_file_logging_success_and_error(tmp_path, caplog):
    log_file = tmp_path / "test_log.log"

    @log(str(log_file))
    def mul(a, b):
        if not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
            raise TypeError("Оба параметра должны быть числами")
        return a * b

    with caplog.at_level(logging.INFO):
        result = mul(3, 4)
    assert result == 12
    assert any(rec.levelname == "INFO" and "Начало выполнения функции" in rec.message for rec in caplog.records)
    assert any(rec.levelname == "INFO" and "Функция успешно выполнена. Результат: 12" in rec.message for rec in caplog.records)

    with caplog.at_level(logging.INFO):
        with pytest.raises(TypeError):
            mul(3, "oops")

    error_logs = [r for r in caplog.records if r.levelname == "ERROR"]
    assert any("Ошибка: TypeError" in rec.message for rec in error_logs)
    assert any("3" in rec.message and "'oops'" in rec.message or '"oops"' in rec.message for rec in error_logs)


    assert log_file.exists() and log_file.stat().st_size > 0

