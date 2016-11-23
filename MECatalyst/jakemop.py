import re
import struct

# Input filename to scan. Add directory if not in the same folder.
filename = 'PlayerProgressionData.txt'

# File to output the name, hashname, and maxvalue for the data to.
output_file = 'output_results.txt'

# The header for the data desired. The items have to match the data under this header.
desired_data = 'PamProgressionFlag'

# Items from the file to print out.
items_to_add = ['Name', 'NameHash', 'MaxValue']

with open(filename, mode='r') as f:
    line_list = [line for line in f.read().split('\n')]
    for x in range(0, len(line_list)):
        line_list[x] = re.sub(r"^[\w]+\s+", '', line_list[x])

re_items = '|'.join(items_to_add)
data_flag = False
results = []
result_tuple = []
for line in line_list:
    entries = re.split(r"\s", line)
    if entries[0] == 'Name' and len(entries) > 2:
        entries[1] = ' '.join(entries[1:])
    if not data_flag:
        if entries[0] == desired_data:
            data_flag = True
    else:
        if re.match(re_items, entries[0]):
            if entries[0] == 'NameHash':
                entries[1] = str(hex(struct.unpack('<I', struct.pack('>I', int(entries[1])))[0]))[2:].upper()
                if len(entries[1]) == 6:
                    entries[1] = '00' + entries[1]
            result_tuple.append('%s: %s' % (entries[0], entries[1]))
        if len(result_tuple) > len(items_to_add)-1:
            data_flag = False
            results.append(result_tuple)
            result_tuple = []

with open(output_file, mode='w') as f:
    for info in results:
        str_info = '\n'.join(info)
        f.write(str_info)
        f.write('\n\n')
