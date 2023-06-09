from concurrent.futures import ThreadPoolExecutor
import os
import requests
import csv
from time import sleep

# Replace with your csv file path
csv_file_path = 'ZIP_Locale_Detail.csv'


def savePage(zipcode):
    # Validate input is a 5-digit number
    if len(str(zipcode)) != 5 or not str(zipcode).isdigit():
        print(f"Invalid input: {zipcode}. Please provide a 5-digit integer.")
        return

    url = f"https://nces.ed.gov/globallocator/index.asp?search=1&State=&city=&zipcode={zipcode}&miles=&itemname=&sortby=name&School=1&PrivSchool=1&College=1"

    attempts = 10

    for i in range(attempts):
        try:
            response = requests.get(url)
            response.raise_for_status()
            break  # If successful, break the loop and don't retry
        except requests.HTTPError as err:
            print(f"Attempt {i+1} of {attempts} failed with error: {err}")
            if i < attempts - 1:  # i is zero indexed, so subtract 1
                sleep(i)  # wait for attempts second before retrying
                continue
            else:
                print(f"Failed to get {zipcode} after {attempts} attempts.")
                return
        except requests.exceptions.ConnectionError as err:
            print(f"Attempt {i+1} of {attempts} failed with error: {err}")
            if i < attempts - 1:  # i is zero indexed, so subtract 1
                sleep(i)  # wait for attempts second before retrying
                continue
            else:
                print(f"Failed to get {zipcode} after {attempts} attempts.")
                return

    # Check if folder exists, if not create one
    if not os.path.exists('saved_pages'):
        os.makedirs('saved_pages')

    with open(f'saved_pages/{zipcode}.html', 'w', encoding='utf-8') as file:
        file.write(response.text)


def read_csv_and_print_integers(csv_file_path):
    try:
        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            next(reader)  # Skip the header row
            zipcodes = []
            for row in reader:
                zipcode = row[4]
                if not os.path.isfile(f'saved_pages/{zipcode}.html'):
                    zipcodes.append(zipcode)
            return zipcodes
    except FileNotFoundError:
        print(f"{csv_file_path} not found.")


def main():
    # Replace with your csv file path
    zipcodes = read_csv_and_print_integers(csv_file_path)
    for zip in zipcodes:
        print(zip)
    with ThreadPoolExecutor(max_workers=30) as executor:
        # Use the executor to map the download_file function to the download info
        results = executor.map(lambda x: savePage(x), zipcodes)
        for result in results:
            print(result)


if __name__ == "__main__":
    main()
