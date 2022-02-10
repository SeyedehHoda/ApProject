from DataBaseEngine.Table import Table
from DataBaseEngine.whereClauseDispatcher import get_rows_with_where_clause
from DataBaseEngine.commonFunctions import generate_table_line_from_values_str,\
    validate_unique_column_on_update, convert_rows_list_to_rows_dic


def insert(table_name, values_str):
    table = Table(table_name)
    line = generate_table_line_from_values_str(table, values_str)
    with open('DataBases/' + table_name + '.txt', 'a') as tableFile:
        tableFile.write('\n' + line)


def select(table_name, where_clause):
    return get_rows_with_where_clause(table_name, where_clause)


def update(table_name, where_clause, values_str):
    rows_list = get_rows_with_where_clause(table_name, where_clause)
    table = Table(table_name)
    validate_unique_column_on_update(len(rows_list), table)
    with open('DataBases/' + table_name + '.txt', 'r') as file:
        data = file.readlines()
    for row in rows_list:
        _id = int(row['id'])
        rowsCount = len(table.rowsList)
        isLastRow = _id == rowsCount
        line = generate_table_line_from_values_str(table, values_str, _id)
        if not isLastRow:
            line += '\n'
        data[_id] = line
    with open('DataBases/' + table_name + '.txt', 'w') as file:
        file.writelines(data)


def delete(table_name, where_clause):
    rows_list = get_rows_with_where_clause(table_name, where_clause)
    deleted_ids = list(map(int, list(convert_rows_list_to_rows_dic(rows_list).keys())))
    table = Table(table_name)
    finalRowCount = len(table.rowsList) - len(deleted_ids)
    with open('DataBases/' + table_name + '.txt', 'r') as file:
        data = file.readlines()
    newData = []
    currentId = 1
    for index, line in enumerate(data):
        if index == 0:
            newData.append(line)
            continue
        if index in deleted_ids:
            continue
        written_data = str(currentId) + ' ' + ' '.join(line.split()[1:])
        if currentId != finalRowCount:
            written_data += '\n'
        newData.append(written_data)
        currentId += 1
    with open('DataBases/' + table_name + '.txt', 'w') as file:
        file.writelines(newData)
