from Database import DataBase
import numpy
import datetime



try:
    id_log = DataBase.callFunction('get_max_id_log')
    if id_log[0][0] == None:
        id_log = [[0]]
    id_res = DataBase.callFunction('get_max_id_slau')
    if id_res[0][0] == None:
        id_res = [[0]]
    max_id = max(id_res[0][0], id_log[0][0]) + 1
except Exception as error:
    print(f'Error of calling database procedure: {error}!')
    exit(1)





print('Enter file name: ', end='')
FileName = input()

try:
    file = open(FileName, 'r')
except BaseException:
    print(f'Error opening file {FileName}!')
    exit(1)

matrix = []
for line in file:
    tm_line = line.split(' ')
    tm_arr = []
    for item in tm_line:
        if not item.isspace() and (item != ''):
            tm_arr.append(float(item))
    matrix.append(tm_arr)

file.close()


b = []
try:
    for i1 in matrix:
        b.append(i1[i1.__len__() - 1])
        i1.pop(i1.__len__() - 1)
except Exception as error:
    print(error)
    exit(1)


result = None
try:
    result = numpy.linalg.solve(matrix, b)
except Exception as error:
    try:
        if DataBase.callFunction('find', str(matrix), str(b), '-') == []:
            DataBase.callFunction('add_log', max_id, f'Error of solve matrix equation: {error}!', datetime.datetime.now())
            DataBase.callFunction('add_result', str(max_id), str(matrix), str(b), '-')
    except Exception as error:
        print(f'Error of calling database procedure: {error}!')
    exit(2)

try:
    if DataBase.callFunction('find', str(matrix), str(b), str(result)) == []:
        DataBase.callFunction('add_log', str(max_id), 'Equation was solved!', datetime.datetime.now())
        DataBase.callFunction('add_result', str(max_id), str(matrix), str(b), str(result))
except Exception as error:
    print(f'Error of calling database procedure: {error}!')
    exit(1)



