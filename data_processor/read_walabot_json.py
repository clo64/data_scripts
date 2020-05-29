"""
Quick practice script to learn how to use ijson

Goal is to read very large JSON files without loading into
memory

note: ijson likes files opened in binary format
"""

import ijson

# rb flag opens file in binary
json_to_parse = open('../data/raw/wala_1.json', 'rb')

test_object = ijson.items(json_to_parse, '55')

for o in test_object:
    wala_data_array = o

print(str(wala_data_array[0]))

    
    


