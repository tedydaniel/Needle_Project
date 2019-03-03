import csv
import pprint


def read():
    close_value = {}
    with open('../data/DJIA_table.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        first_row = True
        for row in reader:
            if first_row:
                first_row = False
                continue
            close_value[row[0]] = float(row[6])
    return close_value


if __name__ == "__main__":
    d = read()
    pprint.pprint(d)
    print(len(d))
