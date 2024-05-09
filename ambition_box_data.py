import requests
import csv
from lxml import html

session = requests.session()
output_file = "C:/Users/Public/haneet/B_30/fetching_all_company_data.csv"

header = {
    'authority': 'www.ambitionbox.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'if-none-match': '"4dfcd-FcG41TSKP24BSFDBfvbQmxTDEP0"',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}


def get_details():
    count = 1

    while True:
        base_path = f"https://www.ambitionbox.com/list-of-companies?sortBy=popular&indianEmployeeCounts=501-1000,1001-5000,5001-10000,10001-50000,50001-100000,100001&page={count}"
        get_request = session.get(base_path, headers=header)

        if get_request.status_code == 200:
            get_response = html.fromstring(get_request.content)
            company_details = get_response.xpath('//*[@id="__layout"]//a/h2/text()')
            company_industry = get_response.xpath('//*[@id="__layout"]//div[2]/div[2]/div[1]/div[1]/span/text()')

            with open(output_file, "a", newline='', encoding='utf-8') as write_csv:
                fieldnames = ["company_name", "company_industry"]
                csv_write = csv.DictWriter(write_csv, fieldnames=fieldnames)

                for company, details in zip(company_details, company_industry):
                    company_data = company.strip()
                    company_industry_data = details.strip()
                    entry = {"company_name": company_data, "company_industry": company_industry_data}
                    print(entry)
                    csv_write.writerow(entry)

            count += 1
        else:
            break


if __name__ == "__main__":
    get_details()
