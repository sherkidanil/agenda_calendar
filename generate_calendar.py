import calendar
import csv
from datetime import date, datetime

# Загрузка событий из CSV
def load_events_from_csv(filepath):
    events = []
    with open(filepath, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            start = datetime.strptime(row["start_date"], "%Y-%m-%d").date()
            end = datetime.strptime(row["end_date"], "%Y-%m-%d").date()
            title = row["title"]
            events.append({"start": start, "end": end, "label": title})
    return events

# Генерация цветов
def generate_color_map(events):
    base_colors = ["#ffd966", "#a4c2f4", "#d9ead3", "#f4cccc", "#cfe2f3", "#f9cb9c"]
    unique_labels = sorted(set(e["label"] for e in events))
    color_map = {label: base_colors[i % len(base_colors)] for i, label in enumerate(unique_labels)}
    return color_map

# Генерация словаря с выделенными датами и подписями
def get_highlight_dates(events):
    highlights = {}
    for r in events:
        current = r["start"]
        while current <= r["end"]:
            highlights[current] = r["label"]
            next_day = current.day + 1
            if next_day > calendar.monthrange(current.year, current.month)[1]:
                if current.month == 12:
                    current = date(current.year + 1, 1, 1)
                else:
                    current = date(current.year, current.month + 1, 1)
            else:
                current = date(current.year, current.month, next_day)
    return highlights

# Генерация календаря на месяц
def generate_month_calendar(year, month, highlights, color_map):
    cal = calendar.HTMLCalendar(calendar.MONDAY)
    html = f'<table class="calendar"><caption>{calendar.month_name[month]} {year}</caption><thead><tr>'
    html += ''.join(f'<th>{day}</th>' for day in calendar.day_abbr)
    html += '</tr></thead><tbody>'
    for week in cal.monthdayscalendar(year, month):
        html += '<tr>'
        for day in week:
            if day == 0:
                html += '<td></td>'
            else:
                current_date = date(year, month, day)
                if current_date in highlights:
                    label = highlights[current_date]
                    color = color_map[label]
                    html += f'<td style="background-color:{color}" title="{label}"><strong>{day}</strong><br><small>{label}</small></td>'
                else:
                    html += f'<td>{day}</td>'
        html += '</tr>'
    html += '</tbody></table>'
    return html

# Основной HTML шаблон
def build_full_html(months, year, highlights, color_map):
    html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Календарь Лето 2025</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
        }
        h1 {
            margin-bottom: 30px;
        }
        .calendar {
            border-collapse: collapse;
            margin-bottom: 40px;
            width: 100%;
        }
        .calendar caption {
            font-size: 1.6em;
            margin-bottom: 10px;
            font-weight: bold;
        }
        .calendar th, .calendar td {
            border: 1px solid #999;
            padding: 8px;
            text-align: center;
            vertical-align: top;
            width: 14.28%;
            height: 80px;
        }
        .calendar small {
            font-size: 0.75em;
        }
    </style>
</head>
<body>
    <h1>Календарь событий — Лето 2025</h1>
"""
    for month in months:
        html += generate_month_calendar(year, month, highlights, color_map)
    html += "</body></html>"
    return html

# Запуск
events = load_events_from_csv("events.csv")
highlight_dates = get_highlight_dates(events)
color_map = generate_color_map(events)
final_html = build_full_html([6, 7, 8], 2025, highlight_dates, color_map)

# Сохраняем
with open("index.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("✅ Готово! Файл index.html создан с подписями и цветами.")
