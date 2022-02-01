# Takes GitHut2.0 json's as input
# Outputs one csv spreadsheet formatted for app.flourish.studio


import os
import json
import csv


# Constants
START_YEAR = 2012
START_QUARTER = 2
END_YEAR = 2021
END_QUARTER = 4
RESOURCES = "./resources"
OUTPUT_FILENAME = "./out.csv"


def main():
    # Prepare output csv headers
    csv_headers = ["Language", "Image"]
    current_year = START_YEAR
    current_quarter = START_QUARTER
    while current_year < END_YEAR or (current_year == END_YEAR and current_quarter <= END_QUARTER):
        if current_quarter <= 4:
            csv_headers.append(str(current_year) + 'q' + str(current_quarter))
            current_quarter = current_quarter + 1
        else:
            current_year = current_year + 1
            current_quarter = 1
    with open(OUTPUT_FILENAME, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(csv_headers)

    # Grab resource file paths
    resource_file_names = []
    dirListing = os.listdir(RESOURCES)
    for item in dirListing:
        if ".json" in item:
            resource_file_names.append(RESOURCES + '/' + item)

    # Grab language names and max values
    language_names = set()
    max_issues = 0
    max_pulls = 0
    max_pushes = 0
    max_stars = 0
    for resource_file_name in resource_file_names:
        with open(resource_file_name) as resource_file:
            resource_file_json = json.load(resource_file)
            for entry in resource_file_json:
                language_names.add(entry["name"])
                if "issue" in resource_file_name and max_issues < int(entry["count"]):
                    max_issues = int(entry["count"])
                elif "pull" in resource_file_name and max_pulls < int(entry["count"]):
                    max_pulls = int(entry["count"])
                elif "push" in resource_file_name and max_pushes < int(entry["count"]):
                    max_pushes = int(entry["count"])
                elif "star" in resource_file_name and max_stars < int(entry["count"]):
                    max_stars = int(entry["count"])

    # Prepare empty output data
    lang_data = dict()
    for language_name in language_names:
        lang_data[language_name] = []
        current_year = START_YEAR
        current_quarter = START_QUARTER
        while current_year < END_YEAR or (current_year == END_YEAR and current_quarter <= END_QUARTER):
            if current_quarter <= 4:
                lang_data[language_name].append(0)
                current_quarter = current_quarter + 1
            else:
                current_year = current_year + 1
                current_quarter = 1

    # Fill output data
    for resource_file_name in resource_file_names:
        with open(resource_file_name) as resource_file:
            resource_file_json = json.load(resource_file)
            for entry in resource_file_json:
                if "issue" in resource_file_name:
                    lang_data[entry["name"]][get_index(entry["year"], entry["quarter"])] = lang_data[entry["name"]][get_index(entry["year"], entry["quarter"])] + ((int(entry["count"]) / max_issues) / 4)
                elif "pull" in resource_file_name:
                    lang_data[entry["name"]][get_index(entry["year"], entry["quarter"])] = lang_data[entry["name"]][get_index(entry["year"], entry["quarter"])] + ((int(entry["count"]) / max_pulls) / 4)
                elif "push" in resource_file_name:
                    lang_data[entry["name"]][get_index(entry["year"], entry["quarter"])] = lang_data[entry["name"]][get_index(entry["year"], entry["quarter"])] + ((int(entry["count"]) / max_pushes) / 4)
                elif "star" in resource_file_name:
                    lang_data[entry["name"]][get_index(entry["year"], entry["quarter"])] = lang_data[entry["name"]][get_index(entry["year"], entry["quarter"])] + ((int(entry["count"]) / max_stars) / 4)

    # Write output data to csv
    with open("out.csv", 'a') as file:
        writer = csv.writer(file)
        for language_name in language_names:
            line = [language_name, '']
            line.extend(lang_data[language_name])
            writer.writerow(line)


def get_index(year, quarter):
    year = int(year)
    quarter = int(quarter)
    index = 0
    current_year = START_YEAR
    current_quarter = START_QUARTER
    while current_year < year or (current_year == year and current_quarter < quarter):
        if current_quarter <= 4:
            current_quarter = current_quarter + 1
            index = index + 1
        else:
            current_year = current_year + 1
            current_quarter = 1
    return index


main()

