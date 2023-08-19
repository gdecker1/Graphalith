from collections import deque

class Expression: 
    ######################################
    #            CONSTANTS               #
    ######################################
    DELIMITERS = {"<": ">", 
                  "(":")", 
                  "{": "}", 
                  "[":"]"}
    
    ######################################
    #            PRIVATE METHODS         #
    ######################################
    
    def __init__(self, **kwargs):
        self.name =  kwargs.get('name', "default")
        self.value = kwargs.get('value', "").strip()
        self.type = kwargs.get('type', None)

        self.simplified = self.__is_simplified()
        self.valid = self.__is_valid_expression()

        if self.type is None:
            self.type = self.__determine_type()

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
            return "numeric"

        if self.value.isalpha():
            return "alpha"
        
        if self.value in Expression.DELIMITERS.keys():
            return "open_delimiter"
        
        if self.value in Expression.DELIMITERS.values():
            return "closed_delimiter"
        
        return "unknown"
        
    def __get_corresponding_delimiter(self) -> str:
        if self.type == "open_delimiter":
            if self.value not in Expression.DELIMITERS:
                raise TypeError("__get_corresponding_delimiter: Open delimiter type error")
            return Expression.DELIMITERS[self.value]
        
        if self.type == "closed_delimiter":
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
            if ch_expression.expression_get_type() == "open_delimiter":
                stack.append(ch_expression)
            elif ch_expression.expression_get_type() == "closed_delimiter":
                if stack.pop() != self.__get_corresponding_delimiter(ch_expression):
                    return False
                
        return len(stack) == 0

    def __is_valid_expression(self) -> bool:
        return self.__is_delimiter_balanced()
    
    def __evaluate_expression(self, expression):
        return None
       
       


    ######################################
    #                 API                #
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
    

    


