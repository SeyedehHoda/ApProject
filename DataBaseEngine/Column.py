class Column:
    def __init__(self, line):
        parts = line.strip().split()
        self.columnName = parts[0]
        self.isUnique = len(parts) == 3
        columnType = parts[-1]
        if 'CHAR' in columnType:
            self.columnType = 'CHAR'
            self.columnLimit = int(columnType.split('(')[-1][:-1])
        else:
            self.columnType = columnType
