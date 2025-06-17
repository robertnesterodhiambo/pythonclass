# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 15:14:02 2022

@author: Asad Mehmood (asadmahmood16@hotmail.com)
"""

import logging
from datetime import datetime
import string
import usaddress
import re

global dev
dev = False
TABLE_Logger = "Logger"
PUNCTUATION = string.punctuation
TRANSLATOR = str.maketrans('', '', PUNCTUATION)

US_STREET_KEYS = ['AddressNumberPrefix', 'AddressNumberSuffix', 'AddressNumber',
                  'BuildingName', 'StreetNamePreDirectional', 'StreetNamePreModifier',
                  'StreetNamePreType', 'StreetName', 'StreetNamePostDirectional',
                  'StreetNamePostModifier', 'StreetNamePostType']
US_CITY_KEYS = ['PlaceName']
REQUIRE_KEYS = US_STREET_KEYS + US_CITY_KEYS + ['StateName', 'ZipCode']

def print_log(text, error=False):
    if dev:
        print(text)
    else:
        if error:
            logging.error(text.strip())
        else:
            logging.info(text.strip())

def RepresentsInt(s):
    isInt = True
    try:
        int(s)
    except ValueError:
        isInt = False
    return isInt

def parse_address(address):
    zip_code = re.findall(r'\d{4,5}', address)
    address = address.split('.')[0]
    if len(zip_code) > 0:
        zip_code = zip_code[0]

    if len(address.split(',')) > 3:
        new_add = address.split(',')[:3]
        zip_part = re.findall(r'\d{4,5}', " ".join(new_add[1:]))
        sec_elm = new_add[1]
        num_center = len(sec_elm.split())
        if not RepresentsInt(sec_elm) and bool(zip_part) and num_center <= 3:
            address = ",".join(new_add).strip()

    if bool(address) and any([address.startswith(p) for p in PUNCTUATION]):
        address = address[1:].strip()

    street = str(address.split(',')[0].title().strip() if len(address.split(',')) > 0 else '').strip()
    city = str(address.split(',')[1].title().strip() if len(address.split(',')) > 1 else '').strip()

    if street.lower().endswith(" rd"):
        street = street[:-2] + "Road"
    if street.lower().endswith(" st"):
        street = street[:-2] + "Street"
    if street.lower().endswith(" ave"):
        street = street[:-3] + "Avenue"
    if street.lower().endswith(" dr."):
        street = street[:-3] + "Drive"

    info = {
        'Street': street,
        'City': city,
        'Zip_Code': zip_code if bool(zip_code) else '',
        'Address': str(bool(address)),
    }
    return info

def gets_usaddress(text):
    ans = usaddress.parse(text)
    addr = list()
    for val in ans:
        dict_val, dict_key = val
        tupe = (dict_key, dict_val)
        addr.append(tupe)
    return addr

def parse_usaddress(address):
    dump = dict()
    scrape_info = list()
    for val in address.values():
        str_street = list()
        str_city = list()
        ZipCode = None
        for ind, i in enumerate(val.copy()):
            k, v = i
            if k in US_STREET_KEYS:
                str_street.append(v)
            if k in US_CITY_KEYS:
                str_city.append(v)

            if 'ZipCode' == k:
                ZipCode = v.strip()
                if any(ZipCode.endswith(s) for s in PUNCTUATION):
                    ZipCode = ZipCode[:-1].strip()
                for s in PUNCTUATION:
                    if s in ZipCode:
                        ZipCode = ZipCode.split(s)[0].strip()
                        break
            try:
                next_key = val[ind + 1][0]
                if next_key not in REQUIRE_KEYS:
                    break
            except IndexError:
                break

        info = dict()
        if bool(str_street) and bool(str_city):
            info_street = " ".join(str_street)
            info_city = " ".join(str_city)

            while any(info_street.endswith(s) for s in PUNCTUATION):
                info_street = info_street[:-1].strip()

            while any(info_city.endswith(s) for s in PUNCTUATION):
                info_city = info_city[:-1].strip()

            us_street = info_street.strip().title()
            us_city = info_city.strip().title()

            if us_street.strip().lower().endswith(" rd"):
                us_street = us_street[:-2] + "Road"
            if us_street.strip().lower().endswith(" st"):
                us_street = us_street[:-2] + "Street"
            if us_street.strip().lower().endswith(" ave"):
                us_street = us_street[:-3] + "Avenue"
            if us_street.strip().lower().endswith(" dr"):
                us_street = us_street[:-2] + "Drive"

            info.update({'Street': us_street, 'City': us_city, 'Zip_Code': ''})
            if bool(ZipCode):
                info['Zip_Code'] = ZipCode

        if bool(info):
            scrape_info.append(info)
    if bool(scrape_info):
        info_list = [dict(t) for t in {tuple(d.items()) for d in scrape_info}]
        if len(info_list) > 1:
            try:
                for i, vault in enumerate(info_list.copy()):
                    if not bool(vault['Zip_Code']):
                        del info_list[i]
            except IndexError:
                info_list = scrape_info[:1].copy()

        if len(info_list) > 1:
            info_list = scrape_info[:1].copy()
        dump = info_list.pop()
        dump.update({'Address': str(bool(dump['Street']))})
    return dump

def filter_notice(notice):
    content = notice.lower().strip()
    address = ''
    address_list = dict()
    us_addr_list = dict()

    # Expanded search phrases
    search_strings = [
        'property is more commonly known as', 'said property being known as:', 'said property is known as',
        'property known a/s', 'known as located at', 'known as address', 'k/a',
        'located at', 'property address:', 'following parcels', 'commonly known as',
        'property located at', 'street address:', 'property location:', ':property location:',
        ": location:", "location:", " location:", 
        "at the location indicated:", "on "
    ]

    for find_str in search_strings:
        if find_str in content:
            part = content.split(find_str, 1)[1].strip()
            # Try to get only the part before the date
            match = re.match(r"([0-9]{3,5}.+? ga [0-9]{5})", part)
            if match:
                address = match.group(1)
            else:
                address = part.split(" on ")[0].strip()

            nr_parsed = parse_address(address)
            us_parsed = gets_usaddress(address)

            address_list[find_str] = nr_parsed
            us_addr_list[find_str] = us_parsed

    # Additional fallback: try raw regex search if no match
    if not address_list:
        raw_matches = re.findall(r"(\d{3,5} [^\n,]+(?:Blvd|Road|Rd|Drive|Dr|Ave|Avenue|Street|St)?[, ]+[\w ]+,? ?Ga ?\d{5})", content, re.IGNORECASE)
        if raw_matches:
            address = raw_matches[0]
            nr_parsed = parse_address(address)
            us_parsed = gets_usaddress(address)
            address_list["regex_fallback"] = nr_parsed
            us_addr_list["regex_fallback"] = us_parsed

    parsed_us = parse_usaddress(us_addr_list)

    parser_nr = dict()
    parse = False
    num_addresses = len(address_list)
    vals = list(address_list.values())
    if num_addresses == 1:
        parse = True
    elif num_addresses > 1 and not bool(parsed_us):
        parse = True
        vals = [dict(t) for t in {tuple(d.items()) for d in vals}]

    if parse:
        dump = vals.pop()
        if dump['City'] == str(datetime.today().year):
            dump['City'] = ''

        if dump.get('Street') and dump.get('City'):
            zip_code = dump['Zip_Code']
            if zip_code == str(datetime.today().year) or dump['Street'].startswith(zip_code):
                dump['Zip_Code'] = ''
            if len(dump['City'].split()) > 3 or len(dump['Street'].split()) > 8:
                parser_nr = dict()
            else:
                parser_nr = dump.copy()

    return parsed_us, parser_nr


def start_logger(limited, database, source):
    r_starts = 1
    r_finish = limited
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    where_clause = "Data_Source = '{}'".format(source)
    stmt = "SELECT Next_Starts,Next_Finish FROM {} WHERE {}".format(TABLE_Logger, where_clause)
    sql = "({}) AS NUM".format(stmt)
    num = database.get_count(sql)
    if num:
        rows = database.show_data(TABLE_Logger, stmt)
        r_starts, r_finish = list(rows).pop()
        if not bool(r_starts):
            r_starts = 1
        if not bool(r_finish):
            r_finish = limited
    else:
        info = dict(Data_Source=source, Run_Time=date_now,Next_Starts=str(r_starts),Next_Finish=str(r_finish))
        columns_str = "`, `".join(info.keys())
        values = "', '".join(info.values())
        stmt = "INSERT INTO `{}` (`{}`) VALUES ('{}');".format(TABLE_Logger, columns_str, values)
        try:
            database.run_query(stmt)
        except Exception as e:
            error_str = "{}: {}".format(str(type(e).__name__), str(e))
            error_sql = "SQL: '{}'".format(stmt)
            print_log(error_str, True)
            print_log(error_sql, True)
    return date_now, r_starts, r_finish

def calculate_run(urls, total_return, limited, r_starts, r_finish, full_data):
    all_pages = urls.copy()
    if total_return <= limited:
        if r_starts > 1:
            all_pages = urls[r_starts:].copy()
            if full_data and len(all_pages) <= limited and total_return <= limited:
                all_pages = urls[-limited:].copy()

        if r_starts <= total_return:
            r_starts = total_return
    else:
        if r_starts == 1:
            all_pages = urls[:limited].copy()
            r_starts = limited
        else:
            if full_data:
                all_pages = urls[r_starts:r_finish].copy()
            else:
                all_pages = urls[:limited].copy()
            r_starts += len(all_pages)

    if bool(all_pages):
        r_finish = r_starts + limited
    return all_pages, r_starts, r_finish

def update_logger(database, source, date_now, limited, r_starts, r_finish, total_return, urls, full=True):
    set_equal = list()
    set_equal.append("Run_Time = '{}'".format(date_now))
    set_equal.append("Starts = {}".format(r_starts))
    set_equal.append("Finish = {}".format(r_finish))
    set_equal.append("Total_Records = {}".format(total_return))

    all_pages, r_starts, r_finish = calculate_run(urls, total_return, limited, r_starts, r_finish, full)

    n_records = len(all_pages)
    set_equal.append("Scrapped = {}".format(n_records))
    set_equal.append("Next_Starts = {}".format(r_starts))
    set_equal.append("Next_Finish = {}".format(r_finish))

    equals = ", ".join(set_equal)
    where_clause = "Data_Source = '{}'".format(source)
    stmt = """UPDATE `{}` SET {} WHERE {}""".format(TABLE_Logger, equals, where_clause)
    try:
        database.run_query(stmt)
    except Exception as e:
        error_str = "{}: {}".format(str(type(e).__name__), str(e))
        error_sql = "SQL: '{}'".format(stmt)
        print_log(error_str, True)
        print_log(error_sql, True)
    return all_pages

if __name__ == "__main__":
    check = True
    total_records = 232
    limit = 200
    n_begins = 200
    n_finish = 400
    list_url = list(range(1, total_records + 1))
    if not check:
        list_url = list(range(1, limit + 1))
        if total_records > n_begins and total_records < n_finish:
            list_url = list(range(1, total_records - n_begins + 1))

    list_url, n_begins, n_finish = calculate_run(list_url, total_records, limit, n_begins, n_finish, check)
