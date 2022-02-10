from DataBaseEngine.Column import Column


class Table:
    def __init__(self, table_name):
        self.tableName = table_name
        self.columnsDic = self.generate_columns_from_schema()
        self.rowsList, self.rowsDic = self.generate_rows_from_table_data()

    def generate_columns_from_schema(self):
        columns = {}
        isTableColumns = False
        columns['id'] = Column('id UNIQUE INTEGER')
        with open('schema.txt', 'r') as schema:
            for line in schema:
                if line.strip() == self.tableName:
                    isTableColumns = True
                elif line == '\n':
                    isTableColumns = False
                else:
                    if isTableColumns:
                        column = Column(line)
                        columns[column.columnName] = column
        return columns

    def generate_rows_from_table_data(self):
        rowsList = []
        rowsDic = {}
        unique_columns_list = []
        for column in self.columnsDic.values():
            if column.isUnique:
                rowsDic[column.columnName] = {}
                unique_columns_list.append(column.columnName)
        firstLine = True
        columnNameList = None
        with open('DataBases/' + self.tableName + '.txt', 'r') as tableData:
            for line in tableData:
                if firstLine:
                    columnNameList = line.strip().split()
                    firstLine = False
                else:
                    row = {}
                    valuesList = line.strip().split()
                    for index, value in enumerate(valuesList):
                        columnName = columnNameList[index]
                        row[columnName] = value

                    rowIndex = len(rowsList)
                    rowsList.append(row)
                    for columnName in unique_columns_list:
                        rowsDic[columnName][row[columnName]] = rowIndex
        return rowsList, rowsDic

    def get_column_with_column_name(self, column_name):
        if column_name not in self.columnsDic.keys():
            raise Exception('Not valid column name')
        return self.columnsDic[column_name]

    def get_row_with_unique_key(self, column_name, unique_value):
        if unique_value not in self.rowsDic[column_name].keys():
            return None
        return self.rowsList[self.rowsDic[column_name][unique_value]]

    def get_sorted_keys_list(self):
        with open('DataBases/' + self.tableName + '.txt', 'r') as tableData:
            for line in tableData:
                return line.strip().split()[1:]