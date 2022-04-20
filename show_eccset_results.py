import sys


def extract_results(filename):
    with open(filename) as f:
        content = f.readlines()
    records = set()
    for line in content:
        line = line.strip()
        if line.startswith('***'):
            data = line.split()
            if data[1].startswith('ch') and data[1][-2] == '3':
                records.add(line)
            elif (data[1] == 'Number' or data[1] == 'Size' or data[1] == 'Verification' or data[1] == 'Total') and not data[-3].startswith('H_CZ'):
                records.add(line)
    for record in sorted(records):
        print(record)


if __name__ == '__main__':
    fn = None
    if len(sys.argv) != 2:
        fn = 'eccset.log'
    else:
        fn = sys.argv[1]
    extract_results(fn)
