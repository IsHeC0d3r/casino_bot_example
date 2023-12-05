kb = [
    [
        'text1',
        'text2'
    ],
    [
        'text3'
    ]
]

# output = [
#     [
#         Data(text='text0', callback='callback0')
#         Data(text='text1', callback='callback1')
#     ],
#     [
#         Data(text='text2', callback='callback2')
#     ]
# ]
# for row in (row for sub in kb for row in sub):
#     print(f'text - {row[0]}, callback - {row[1]}')

class Data():
    def __init__(self, text, callback):
        pass

#output = [[Data(text=item[0], callback=item[1]) for item in row] for row in kb]

output = [[Data(text=item[0], callback='') for item in kb]]

print(output)