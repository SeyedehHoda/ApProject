def convert_rows_list_to_rows_dic(rows_list):
    rows_dic = {}
    for row in rows_list:
        rows_dic[row['id']] = row
    return rows_dic


def typeValidationCheck(column, value):
    if value == 'null' and not column.isUnique:
        return
    if column.columnType == 'INTEGER':
        try:
            int(value)
        except:
            raise Exception(value + ' is not integer')
    if column.columnType == 'CHAR':
        if len(value) > column.columnLimit:
            raise Exception(value + ' length is greater than columnLimit')
    if column.columnType == 'BOOLEAN':
        value = value.lower()
        if value != 'true' and value != 'false':
            raise Exception(value + ' is not a boolean')
    if column.columnType == 'TIMESTAMP':
        parts = value.split('-')
        if len(parts) != 3:
            raise Exception(value + ' is not a valid date')
        for index, part in enumerate(parts):
            try:
                int_part = int(part)
            except:
                raise Exception(value + ' is not a valid date')
            if int_part < 1:
                raise Exception(value + ' is not a valid date')
            if (index == 1 and int_part > 12) or (index == 2 and int_part > 31):
                raise Exception(value + ' is not a valid date')


def isItValidToAddThisColumnToTableRow(table, column_name, value, newId):
    column = table.get_column_with_column_name(column_name)
    typeValidationCheck(column, value)
    if column.isUnique:
        row = table.get_row_with_unique_key(column.columnName, value)
        if row:
            if int(row['id']) != int(newId):
                raise Exception('Already have a row with ' + column_name + "=" + value + " in " + table.tableName + " table")


def generate_table_line_from_values_str(table, values_str, _id=None):
    newId = _id if _id else (len(table.rowsList) + 1)
    line = str(newId) + ' '
    values_list = values_str.split(',')
    keys_list = table.get_sorted_keys_list()
    if len(values_list) < len(keys_list):
        raise Exception('less arguments than keys')
    if len(values_list) > len(keys_list):
        raise Exception('more arguments than keys')
    for key, value in zip(keys_list, values_list):
        isItValidToAddThisColumnToTableRow(table, key, value, newId)
        line += value + ' '
    return line


def validate_unique_column_on_update(rows_count, table):
    containUniqueColumn = False
    for columnName, column in table.columnsDic.items():
        if columnName == 'id':
            continue
        if column.isUnique:
            containUniqueColumn = True
            break
    if containUniqueColumn and rows_count > 1:
        raise Exception('unique values rule have been broken')
