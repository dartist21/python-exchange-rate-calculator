import csv
import requests
from datetime import datetime
import chardet
import argparse
import random
import time

column_name_date = "Дата операції"
column_name_total = "Сума"
column_name_exchange_rate = "Курс (UAH)"
column_name_total_uah = "Сума (UAH)"
column_name_quarter = "Квартал"


def get_random_mobile_user_agent():
    user_agents = [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    ]
    return random.choice(user_agents)


def detect_encoding(file_path):
    with open(file_path, "rb") as f:
        result = chardet.detect(f.read())
        return result["encoding"]


def get_exchange_rate(date):
    print(f"Getting exchange rate for {date}")
    formatted_date = date.strftime("%Y%m%d")
    url = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=USD&date={formatted_date}&json"
    headers = {
        "User-Agent": get_random_mobile_user_agent(),
        "Accept": "application/json",
        "Connection": "keep-alive",
        "Referer": "https://bank.gov.ua/",
        "Accept-Language": "en-US,en;q=0.9",
    }
    time.sleep(random.uniform(3, 8))
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(
            f"API request failed with status code {response.status_code}: {response.text}"
        )
    data = response.json()

    if data:
        return data[0]["rate"]
    raise Exception("USD rate not found in API response")


def load_csv(file_path):
    encoding = detect_encoding(file_path)
    with open(file_path, newline="", encoding=encoding) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        return [row for row in reader]


def add_uah_column(data):
    for row in data:
        date = datetime.strptime(row[column_name_date], "%d.%m.%Y")
        exchange_rate = get_exchange_rate(date)
        row[column_name_exchange_rate] = exchange_rate
        row[column_name_total_uah] = (
            round(
                float(row[column_name_total].replace(" ", "").replace(",", "."))
                * exchange_rate,
                2,
            )
            if exchange_rate
            else None
        )
    return data


def add_quarters(data):
    for row in data:
        date = datetime.strptime(row[column_name_date], "%d.%m.%Y")
        row[column_name_quarter] = (date.month - 1) // 3 + 1
    return data


def save_to_csv(data, output_file):
    fieldnames = data[0].keys()
    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(data)


def main(input_file, output_file):
    print("Starting...")
    data = load_csv(input_file)
    data = add_uah_column(data)
    data = add_quarters(data)
    save_to_csv(data, output_file)
    print(f"💰 Data saved to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process a CSV file to convert USD to UAH"
    )
    parser.add_argument(
        "-i", "--input_file", required=True, help="Path to the input CSV file"
    )
    parser.add_argument(
        "-o", "--output_file", required=True, help="Path to the output CSV file"
    )
    args = parser.parse_args()

    main(args.input_file, args.output_file)
