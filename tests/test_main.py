import csv
import json
import os
import tempfile

import openpyxl

from main import (filter_status, load_csv, load_json, load_xlsx,
                  process_bank_operations, process_bank_search)


def test_process_bank_search():
    data = [
        {"description": "Payment from Alice"},
        {"description": "Transfer to Bob"},
        {"description": "Invoice payment"},
        {"description": "Other"},
    ]
    result = process_bank_search(data, "payment")
    assert len(result) == 2
    assert all("payment" in item["description"].lower() for item in result)


def test_process_bank_operations():
    data = [
        {"description": "Food"},
        {"description": "Transport"},
        {"description": "Food"},
        {"description": "Entertainment"},
    ]
    categories = ["Food", "Transport"]
    counts = process_bank_operations(data, categories)
    assert counts == {"Food": 2, "Transport": 1}


def test_load_json():
    sample = [{"a": 1}, {"b": 2}]
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as f:
        json.dump(sample, f)
        path = f.name
    loaded = load_json(path)
    os.remove(path)
    assert loaded == sample


def test_load_csv():
    sample = [
        {"name": "Alice", "age": "30"},
        {"name": "Bob", "age": "25"},
    ]
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "age"])
        writer.writeheader()
        writer.writerows(sample)
        path = f.name
    loaded = load_csv(path)
    os.remove(path)
    assert loaded == sample


def test_load_xlsx():
    sample = [
        {"name": "Alice", "score": 90},
        {"name": "Bob", "score": 80},
    ]
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
        path = f.name
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["name", "score"])
    for row in sample:
        ws.append([row["name"], row["score"]])
    wb.save(path)
    loaded = load_xlsx(path)
    os.remove(path)
    assert loaded == sample


def test_filter_status():
    data = [
        {"status": "EXECUTED"},
        {"status": "pending"},
        {"status": "Executed"},
        {"status": "CANCELED"},
        {},
    ]
    filtered = filter_status(data, "executed")
    assert len(filtered) == 2
    assert all(op["status"].upper() == "EXECUTED" for op in filtered)
