from DataBaseEngine.Expression import SimpleExpression
from DataBaseEngine.Table import Table
from DataBaseEngine.commonFunctions import convert_rows_list_to_rows_dic

index = 0
expDic = {}


def __is_row_matched_with_expression(row, expression):
    if expression.columnName not in row.keys():
        raise Exception(expression.columnName + 'is not a valid columnName for this table')
    if expression.isEqual:
        return row[expression.columnName] == expression.value
    return row[expression.columnName] != expression.value


def __get_all_matching_rows_with_expression(table_name, expression_text):
    expression = SimpleExpression(expression_text)
    table = Table(table_name)
    matching_rows_list = []
    for row in table.rowsList:
        if __is_row_matched_with_expression(row, expression):
            matching_rows_list.append(row)
    return matching_rows_list


def __apply_and_on_rows(rows1, rows2):
    rows2_dic = convert_rows_list_to_rows_dic(rows2)
    result_list = []
    for row in rows1:
        _id = row['id']
        if _id in rows2_dic.keys():
            result_list.append(row)
    return result_list


def __apply_or_on_rows(rows1, rows2):
    result_dic = {}
    for row in rows1:
        _id = row['id']
        if _id not in result_dic.keys():
            result_dic[_id] = row
    for row in rows2:
        _id = row['id']
        if _id not in result_dic.keys():
            result_dic[_id] = row
    return list(result_dic.values())


def __combine_new_rows_with_last_rows(matching_rows_list, exp_code, last_logic):
    global expDic
    last_rows = expDic[exp_code]
    if last_logic == 'AND':
        return __apply_and_on_rows(matching_rows_list, last_rows)
    elif last_logic == 'OR':
        return __apply_or_on_rows(matching_rows_list, last_rows)


def __recursive_get_rows_with_where_clause(table_name, where):
    global index
    global expDic
    while '(' in where:
        last_open_p_index = -1
        for ind, ch in enumerate(where):
            if ch == '(':
                last_open_p_index = ind
            if ch == ')':
                expCode = __recursive_get_rows_with_where_clause(
                    table_name,
                    where[last_open_p_index+1:ind],
                )
                rest = where[ind + 1:] if ind + 1 <= len(where) - 1 else ''
                where = where[:last_open_p_index] + expCode + rest
                break
    parts = where.split()
    lastLogic = None
    lastExpCode = None
    for part in parts:
        if part.lower() == 'and' or part.lower() == 'or':
            lastLogic = part.upper()
        else:
            if part[0] == '<':
                matching_rows_list = expDic[part]
            else:
                matching_rows_list = __get_all_matching_rows_with_expression(table_name, part)
            expCode = '<' + str(index) + '>'
            index += 1
            if lastLogic and lastExpCode:
                matching_rows_list = __combine_new_rows_with_last_rows(matching_rows_list, lastExpCode, lastLogic)
            expDic[expCode] = matching_rows_list
            lastExpCode = expCode
    return lastExpCode


def get_rows_with_where_clause(table_name, where):
    expCode = __recursive_get_rows_with_where_clause(table_name, where)
    return expDic[expCode]