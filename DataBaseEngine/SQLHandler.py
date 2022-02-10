from DataBaseEngine.DbCommands import select, update, insert, delete


def handle_query(query):
    parts = query.split()
    try:
        if parts[0] == 'SELECT':
            return select(parts[2], ' '.join(parts[4:]))
        if parts[0] == 'INSERT':
            return insert(parts[2], parts[4][1:-1])
        if parts[0] == 'UPDATE':
            valuesIndex = parts.index('VALUES')
            return update(parts[1], ' '.join(parts[3:valuesIndex]), parts[valuesIndex+1][1:-1])
        if parts[0] == 'DELETE':
            return delete(parts[2], ' '.join(parts[4:]))
    except Exception as exception:
        print(exception)
