from collections import deque
from enum import Enum

class ExpressionType(Enum):
        UNKNOWN = 0
        NUMERIC = 1
        ALPHA = 2
        DELIMITER_OPEN = 3
        DELIMITER_CLOSED  = 4
        OPERATOR_ADD = 5
        OPERATOR_SUBTRACT = 6
        OPERATOR_MULTIPLY = 7
        OPERATOR_DIVIDE = 8


class Expression: 

    ######################################
    #            CONSTANTS               #
    ######################################

    DELIMITERS = {"<": ">", 
                  "(":")", 
                  "{": "}", 
                  "[":"]"}
    
    OPERATORS = {"+": ExpressionType.OPERATOR_ADD, 
                 "-": ExpressionType.OPERATOR_SUBTRACT, 
                 "*": ExpressionType.OPERATOR_MULTIPLY, 
                 "/": ExpressionType.OPERATOR_DIVIDE}

    
    ######################################
    #            PRIVATE METHODS         #
    ######################################
    
    def __init__(self, **kwargs):
        self.name =  kwargs.get('name', "default")
        self.value = kwargs.get('value', "").strip()
        self.type = self.__determine_type(kwargs.get('type', None))

        self.simplified = self.__is_simplified()
        self.valid = self.__is_valid_expression()

    def __repr__(self):
        return f"""name: {self.name}
                   value: {self.value} 
                   type: {self.type}"""

    def __eq__(self, other) -> bool:
        if not isinstance(other, Expression):
            return False
        
        if not (self.simplified and other.simplified):
            raise AttributeError("__eq__: Expressions must be simplified before checking equality")
        
        return (self.value, self.type) == (other.value, other.type)


    def __determine_type(self) -> str:

        if self.value.isnumeric():
            return ExpressionType.NUMERIC

        if self.value.isalpha():
            return ExpressionType.ALPHA
        
        if self.value in Expression.DELIMITERS.keys():
            return ExpressionType.DELIMITER_OPEN
        
        if self.value in Expression.DELIMITERS.values():
            return ExpressionType.DELIMITER_CLOSED
        
        if self.value in Expression.OPERATORS.keys():
            return Expression.OPERATORS[self.value]
        
        return ExpressionType.UNKNOWN
        
    def __get_corresponding_delimiter(self) -> str:
        if self.type == ExpressionType.DELIMITER_OPEN:
            if self.value not in Expression.DELIMITERS:
                raise TypeError("__get_corresponding_delimiter: Open delimiter type error")
            return Expression.DELIMITERS[self.value]
        
        if self.type == ExpressionType.DELIMITER_CLOSED:
            REVERSED_DELIMITERS = {Expression.DELIMITERS[key]:key for key in Expression.DELIMITERS.keys()}
            if self.value not in Expression.DELIMITERS.values():
                raise TypeError("__get_corresponding_delimiter: Closed delimiter type error")
            return REVERSED_DELIMITERS[self.value]
        
        raise TypeError("__get_corresponding_delimiter: not a delimiter")

    def __is_simplified(self) -> bool:
        # TODO: Implement expression simplification
        return True
    
    def __is_delimiter_balanced(self) -> bool:
        stack = deque()

        for ch in self.value:
            ch_expression = Expression(value = ch)
            if ch_expression.expression_get_type() == ExpressionType.DELIMITER_OPEN:
                stack.append(ch_expression)
            elif ch_expression.expression_get_type() == ExpressionType.DELIMITER_CLOSED:
                if stack.pop() != self.__get_corresponding_delimiter(ch_expression):
                    return False
                
        return len(stack) == 0

    def __is_valid_expression(self) -> bool:
        return self.__is_delimiter_balanced()
    

    # ((3 - 2) + 1)/2
    def __evaluate_expression(self, expression):
        if self.type == ExpressionType.NUMERIC:
            return Expression(value = self.value)
     


    ######################################
    #                 API               #
    ######################################
    
    ## Evaluation
    def expression_evaluate(self):
        if not self.valid: 
            raise TypeError("Not a valid a expression.")
        return self.__evaluate_expression()
    

    ## GETTERS

    def expression_get_value(self):
        return self.value
    
    def expression_get_type(self):
        return self.type
    

    


