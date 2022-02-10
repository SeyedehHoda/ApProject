class SimpleExpression:
    def __init__(self, expression_text):
        if '==' in expression_text:
            parts = expression_text.split('==')
            self.isEqual = True
        elif '!=' in expression_text:
            parts = expression_text.split('!=')
            self.isEqual = False
        else:
            raise Exception('Not Valid Expression')
        self.columnName = parts[0]
        self.value = parts[1]
