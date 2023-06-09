
from bs4 import BeautifulSoup
import os
import re

DEBUG = False


def parse_link(href_content):
    # Extract the arguments within the JavaScript function call
    start = href_content.find("'") + 1
    end = href_content.rfind("'")
    args_str = href_content[start:end]

    # Split the arguments string by '+'
    args = args_str.split('+')

    # Remove quotes and HTML entities from the arguments
    args = [arg.replace("'", "").replace("&#38;", "&") for arg in args]

    results = "https://nces.ed.gov/globallocator/"
    for arg in args:
        results += arg

    return results


def remove_after_last_number(s):
    match = re.search(r'\d[^0-9]*$', s)
    if match:
        end = match.start() + 1
        return s[:end]
    return s


def parse_html(html_line):
    soup = BeautifulSoup(html_line, 'html.parser')

    id_str = soup.find('a')['href']
    id = parse_link(id_str)
    # Find the first <td> tag with class "InstDesc"
    td_tag = soup.find('td', {'class': 'InstDesc'})

    school_name = td_tag.a.string.strip().replace(",", "")
    address = td_tag.contents[2].strip().replace(",", "")
    phone = td_tag.contents[4].strip().split("\xa0\xa0-\xa0\xa0")[0]
    phone = remove_after_last_number(phone)
    details = soup.find(class_='InstDetail').get_text()

    result = f"{id},{school_name},{address},{phone},{details}"
    return result


def extract_lines(html_file_path):
    # Get the zipcode from the file name
    filename = os.path.basename(html_file_path)
    zipcode = os.path.splitext(filename)[0]
    try:
        with open(html_file_path, 'r') as file:
            for line in file:
                if 'InstDesc' in line and not line.strip().startswith('<TABLE'):
                    # strip() is used to remove leading/trailing white space
                    if DEBUG:
                        print(line.strip())
                    csv_line = parse_html(line)
                    if DEBUG:
                        print(csv_line)
                    with open(f'results/{zipcode}.csv', 'a') as output_file:
                        output_file.write(csv_line + '\n')
    except FileNotFoundError:
        print(f"{html_file_path} not found.")


def parse_dir(directory):
    # Get a list of all files in the directory
    files = os.listdir(directory)

    # Loop over each file
    for filename in files:
        # Join the directory path and file name to get the full file path
        file_path = os.path.join(directory, filename)

        # If this file is a file (not a directory), call extract_lines on it
        if os.path.isfile(file_path):
            print(f"Parsing {file_path}")
            # remove the file if it already exists
            if os.path.exists(f'results/{filename}'):
                # remove the file if it already exists
                try:
                    os.remove(file_path)
                    if DEBUG:
                        print(f"{file_path} has been deleted.")
                except FileNotFoundError:
                    print(f"{file_path} not found.")
            extract_lines(file_path)


# Example of using the function
parse_dir('saved_pages')
