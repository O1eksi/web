import os
import datetime
import requests
import requests_html
import pandas as pd

BASE_DIR = os.path.dirname(__file__)

HTML = requests_html.HTML


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


def url_to_txt (url, filename="Exchange.html", save=False):
    r = requests.get(url)
    if r.status_code == 200:
        html_text = r.text
        if save:
            with open(f"Exchange{day}-{month}-{year}.html", 'w', encoding="utf-8") as f:
                f.write(html_text)
        return html_text
    return ""


def parse_and_extract(url, name="2020"):
    html_text = url_to_txt(url)
    r_html = HTML(html=html_text)

    table_class = ".outer"
    r_table = r_html.find(table_class)

    header_names = []
    table_data = []

    if len(r_table) == 1:
        parsed_table = r_table[0]
        rows = parsed_table.find("tr")
        header_row = rows[0].find('th')
        header_names = [x.text for x in header_row]
        table_data = []
        for row in rows[1:]:
            print()
            cols = row.find('td')
            row_data = []
            for col in cols:
                # print(col.text, end='\t\t')
                row_data.append(col.text)
            table_data.append(row_data)
        df = pd.DataFrame(table_data, columns=header_names)
        path = os.path.join(BASE_DIR, "data")
        os.makedirs(path, exist_ok=True)
        filepath = os.path.join('data', f'{name}.csv')
        df.to_csv(filepath, index=False, encoding="utf-8")


def run(day_mon_year_fin=None, day_mon_year_start=None):
    if day_mon_year_fin == None:
        day_mon_year_fin = datetime.datetime.now()
    else:
        day_mon_year_fin = datetime.datetime.strptime(day_mon_year_fin, '%d/%m/%Y')

    if day_mon_year_start == None:
        day_mon_year_start == day_mon_year_fin
    else:
        day_mon_year_start = datetime.datetime.strptime(day_mon_year_start, '%d/%m/%Y')
        for single_date in daterange(day_mon_year_start, day_mon_year_fin):
            url = f'https://bank.gov.ua/ua/markets/exchangerates?date={single_date.day}.{single_date.month}.' \
              f'{single_date.year}&period=daily'
            parse_and_extract(url, name=f"{single_date.day}.{single_date.strftime('%b')}.{single_date.year}")

    url = f'https://bank.gov.ua/ua/markets/exchangerates?date={day_mon_year_fin.day}.{day_mon_year_fin.month}.' \
          f'{day_mon_year_fin.year}&period=daily'
    parse_and_extract(url, name=f"{day_mon_year_fin.day}.{day_mon_year_fin.strftime('%b')}.{day_mon_year_fin.year}")

if __name__ == "__main__":
    run("27/05/2021", "30/04/2021")
