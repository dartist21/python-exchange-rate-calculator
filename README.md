# python-exchange-rate-calculator

# USD to UAH Conversion Tool

This tool processes a CSV file containing USD payments, fetches the corresponding USD to UAH exchange rates from the NBU API, calculates the equivalent amounts in UAH, and adds metadata such as exchange rates and quarter information.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Prepare your input CSV file with the following required columns (provided example.csv):

   - `Дата операції` (Date of the operation in DD.MM.YYYY format)
   - `Сума` (Amount in USD)

2. Run the script:
   ```bash
   python usd_to_uah_conversion.py -i <input_csv_path> -o <output_csv_path>
   ```
   - `-i` or `--input_file`: Path to your input CSV file.
   - `-o` or `--output_file`: Path to save the processed CSV file.

### Example

```bash
python usd_to_uah_conversion.py -i example.csv -o update_exmaple.csv
```

## Output

The processed CSV file will contain the following additional columns:

- `Курс (UAH)` (Exchange rate for USD to UAH on the operation date)
- `Сума (UAH)` (Amount converted to UAH)
- `Квартал` (Quarter of the year for the operation date)

## License

This project is licensed under the MIT License. See the LICENSE file for details.
