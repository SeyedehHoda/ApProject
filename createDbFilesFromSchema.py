firstLine = True
newFile = None
with open('schema.txt', 'r') as schema:
    for line in schema:
        if firstLine:
            newFile = open('DataBases/' + line.strip() + '.txt', 'w')
            newFile.write('id ')
            firstLine = False
        elif line == '\n':
            firstLine = True
        else:
            columnName = line.split()[0]
            newFile.write(columnName + ' ')
