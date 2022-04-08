import sys
import os
from natsort import natsorted


original_val = [900, 58, 114, 170, 450, 170, 420, 225, 347, 495, 669, 883, 1095, 1347, 63, 119, 278, 521, 443, 884, 200, 45, 75, 105, 255, 150]
original_product = 1
for val in original_val:
    original_product *= val
num_timestamps = 73
timestamps = [i * 900 if i < 48 else (i - 24) * 1800 for i in range(num_timestamps)]


def extract_results(content, max_timeout=86400):
    flag = False
    tot_time = 0
    tot_gate = 0
    num_finished = 0
    gate_product = 1
    key = ''
    result = {}
    result_timestamps = [{} for _ in range(num_timestamps)]
    for line in content:
        line = line.strip()
        data = line.split()
        if flag:
            pos = line.find(':')
            pos2 = line.find(',', pos)
            pos3 = line.find('s', pos2)
            if not line[pos + 2:pos2].isnumeric():
                continue
            val = line[pos + 2:pos2]
            result[key] = val
            num_finished += 1
            tot_gate += int(line[pos + 2:pos2])
            gate_product *= int(line[pos + 2:pos2])
            tot_time += float(line[pos2 + 2:pos3])
        if line.startswith('Optimization'):
            flag = True
            pos = line.find('.qasm')
            pos2 = line.rfind(' ', 0, pos)
            key = line[pos2 + 1:pos]
        else:
            flag = False
        if len(data) >= 2 and data[1] == 'Timeout.':
            key = data[0].split('.')[0]
            val = data[-1].split('.')[0] + ' (timeout)'
            result[key] = val
            num_finished += 1
            tot_gate += int(float(data[-1]))
            gate_product *= int(float(data[-1]))
            tot_time += max_timeout
        if len(data) >= 2 and data[1].startswith('bestCost('):
            if float(data[-2]) > max_timeout:
                continue
            key = data[0].split('.')[0]
            val = data[1].split('.')[0][9:] + ' (at ' + data[-2] + ' seconds)'
            result[key] = val
            if key not in result_timestamps[0]:  # first time
                for i in range(num_timestamps):
                    result_timestamps[i][key] = float(data[1].split('.')[0][9:])
            else:
                for i in range(num_timestamps - 1, -1, -1):
                    if timestamps[i] < float(data[-2]):
                        break
                    result_timestamps[i][key] = float(data[1].split('.')[0][9:])
    for k, v in natsorted(result.items()):
        print(k.ljust(15), v)
    print('num_circuits (finished) =', num_finished)
    print('tot_gate =', tot_gate)
    if num_finished > 0:
        print('geomean_gatecount =', gate_product ** (1 / num_finished))
    print('tot_time =', tot_time)
    for k, v in natsorted(result.items()):  # easy paste to google doc
        if v.isnumeric():
            print(v)
        else:
            print(v.split(' ')[0])
    if len(result_timestamps[0]) == 26:
        result_timestamps_geomean_reduction = []
        result_timestamps_reduction = {}
        for i in range(num_timestamps):
            val = 1.0 / original_product
            assert len(result_timestamps[i]) == 26
            cnt = 0
            for k, v in natsorted(result_timestamps[i].items()):
                val *= v
                result_timestamps_reduction[key] = 1 - v / original_val[cnt]
                cnt += 1
            val = val ** (1.0 / 26)
            val = 1 - val
            result_timestamps_geomean_reduction.append(val)
        print(result_timestamps_geomean_reduction)
        print(result_timestamps_reduction)


def extract_results_from_file(filename):
    with open(filename) as f:
        content = f.readlines()
    extract_results(content)


def extract_results_from_files(prefix, max_timeout=86400):
    files = [f for f in os.listdir('.') if f.startswith(prefix) and f.endswith('log')]
    content = []
    for filename in files:
        with open(filename) as f:
            content += f.readlines()
    extract_results(content, max_timeout)


if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('Usage:')
        print('For final result: python extract_results.py [result file name (need to be a .txt file), e.g., scalability_32.txt]')
        print('For intermediate result: python extract_results.py [ECC set name, i.e., Nam_6_3/IBM_4_3/Rigetti_6_3] [Max running time (s) (default=86400)]')
        exit()
    if sys.argv[1].endswith('.txt'):
        extract_results_from_file(sys.argv[1])
    else:
        if len(sys.argv) == 3:
            extract_results_from_files(sys.argv[1], float(sys.argv[2]))
        else:
            extract_results_from_files(sys.argv[1])
