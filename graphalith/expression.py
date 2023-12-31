from collections import deque
from enum import Enum
from typing import Callable as function
from graphalith.node import*
import re

class ExpressionType(Enum):
        #TODO: Add nested expression types 

        """Enum class for expression types"""
        UNKNOWN = 0
        NUMERIC = 1
        ALPHA = 2
        ALPHANUMERIC = 3
        DELIMITER_OPEN = 4
        DELIMITER_CLOSED  = 5
        OPERATOR_ADD = 6
        OPERATOR_SUBTRACT = 7
        OPERATOR_MULTIPLY = 8
        OPERATOR_DIVIDE = 9
        

class Expression: 
    """Class for representing mathematical expressions"""

    ######################################
    #            CONSTANTS               #
    ######################################

    DELIMITERS = {"<": ">", "(":")", "{": "}",  "[":"]"}
    
    OPERATORS = {"+": ExpressionType.OPERATOR_ADD, 
                 "-": ExpressionType.OPERATOR_SUBTRACT, 
                 "*": ExpressionType.OPERATOR_MULTIPLY, 
                 "/": ExpressionType.OPERATOR_DIVIDE}

  
    ######################################
    #            PRIVATE METHODS         #
    ######################################
    
    def __init__(self, **kwargs):
        self.name =  kwargs.get('name', "default")
        self.value = kwargs.get('value', "")

        self.auto_format = kwargs.get('auto_format', False)
        if self.auto_format:
            self.__format_value()

        self.type = self.__determine_type()
        self.auto_eval = kwargs.get('auto_eval', False)
        self.evaluation = None

        self.valid = self.__is_valid_expression()
        self.simplified = self.__is_simplified()


    def __repr__(self):
        """Returns a string representation of the expression"""

        evaluation = ""
        if self.evaluation is not None:
            evaluation = self.evaluation.value
        else:
            evaluation = "None"
            
        return f"""\nValue: {self.value}\nType: {self.type}\nValid: {self.valid}\nEvaluation: {evaluation}"""

    def __eq__(self, other) -> bool:
        """Checks if two expressions are equal"""
        if not isinstance(other, Expression):
            return False
        
        if not (self.simplified and other.simplified):
            raise AttributeError("__eq__: Expressions must be simplified before checking equality")
        
        return (self.value, self.type) == (other.value, other.type)
    
    def __format_value(self) -> 'str':
        """Preprocesses the expression string"""

        # Remove all white spaces
        self.value = re.sub('[ ]', '', self.value)

        # Wrap parantheses around multiplication/divison if not already wrapped
        self.value = re.sub(r'([0-9]+)([*/])([0-9]+)', r'(\1\2\3)', self.value)

        # Replace -- with +
        self.value = re.sub(r'--', '+', self.value)

        # Replace ++ with +
        self.value = re.sub(r'\+\+', '+', self.value)

        # Replace -+ with -
        self.value = re.sub(r'-\+', '-', self.value)

        # Replace +- with -
        self.value = re.sub(r'\+-', '-', self.value)


    def __determine_type(self) -> ExpressionType:
        """Determines the type of the expression"""
        # TODO: Use regex to determine raw expression
        remove_chars = "-/+*()[]<>{}"
        raw_exp = "".join([ch for ch in self.value if ch not in remove_chars and ch != " "])

        try:
            float(self.value)
            return ExpressionType.NUMERIC
        except:
            pass

        if self.value.isalpha():
            return ExpressionType.ALPHA
        
        if raw_exp.isalnum():
            return ExpressionType.ALPHANUMERIC
        
        if self.value in Expression.DELIMITERS.keys():
            return ExpressionType.DELIMITER_OPEN
        
        if self.value in Expression.DELIMITERS.values():
            return ExpressionType.DELIMITER_CLOSED
        
        if self.value in Expression.OPERATORS.keys():
            return Expression.OPERATORS[self.value]
        
        return ExpressionType.UNKNOWN
        
    def __get_corresponding_delimiter(self) -> 'Expression':
        """Returns the corresponding delimiter for the expression"""
        if self.type == ExpressionType.DELIMITER_OPEN:
            if self.value not in Expression.DELIMITERS:
                raise TypeError("__get_corresponding_delimiter: Open delimiter type error")
            return Expression(value = Expression.DELIMITERS[self.value])
        
        if self.type == ExpressionType.DELIMITER_CLOSED:
            REVERSED_DELIMITERS = {Expression.DELIMITERS[key]:key for key in Expression.DELIMITERS.keys()}
            if self.value not in Expression.DELIMITERS.values():
                raise TypeError("__get_corresponding_delimiter: Closed delimiter type error")
            return Expression(value = REVERSED_DELIMITERS[self.value])
        
        raise TypeError("__get_corresponding_delimiter: not a delimiter")

    def __is_simplified(self) -> bool:
        """Determines if the expression is simplified
        Returns: Boolean"""

        # TODO: Implement expression simplification
        return True
    
    def __is_operable(self) -> bool:
        """Determines if the expression is operable (can be operated on immediately)
        Returns: Boolean"""
        return self.type in [ExpressionType.NUMERIC]
    
    def __is_delimiter_balanced(self) -> bool:
        """Determines if the expression has balanced delimiters"""
        if len(self.value) == 0:
            return True
        
        if len(self.value) == 1:
            return self.type != ExpressionType.DELIMITER_OPEN and self.type != ExpressionType.DELIMITER_CLOSED 
        
        stack = deque()  # type: deque[Expression]

        for ch in self.value:
            ch_expression = Expression(value = ch)
            if ch_expression.type == ExpressionType.DELIMITER_OPEN:
                stack.append(ch_expression)
            elif ch_expression.type == ExpressionType.DELIMITER_CLOSED:
                if stack.pop() != ch_expression.__get_corresponding_delimiter():
                    return False
                
        return len(stack) == 0

    def __is_valid_expression(self) -> bool:
        """Determines if the expression is valid for evaluation"""
        if not self.__is_delimiter_balanced():
            return False
        
        if self.auto_eval:
            try:
                self.evaluation = self.__evaluate_expression()
                return True
            except:
                return False
        
        #TODO: Implement expression validation w/o evaluation
        return True
    
    def __perform_operation(self, other: 'Expression', operator: function) -> 'Expression':
        """Performs an operation on two expressions"""
        if not (self.__is_operable() and other.__is_operable()):
            raise TypeError("__perform_expression: Expressions must be operable to perform operation")
        
        if self.type == ExpressionType.NUMERIC and other.type == ExpressionType.NUMERIC:
            new_value = operator(float(self.value), float(other.value))
            return Expression(value = str(new_value))
        
        return None
    
    def __is_operator(self) -> bool:
        """Determines if the expression is an operator"""
        if self is None:
            return False
        return self.type in [ExpressionType.OPERATOR_ADD, ExpressionType.OPERATOR_SUBTRACT, ExpressionType.OPERATOR_MULTIPLY, ExpressionType.OPERATOR_DIVIDE]
    
    def __is_delimiter(self) -> bool:
        """Determines if the expression is a delimiter"""
        if self is None:
            return False
        return self.type in [ExpressionType.DELIMITER_OPEN, ExpressionType.DELIMITER_CLOSED]
    
    
    def __add(x1: float, x2: float) -> float:
        """Adds two expressions together (x1 + x2)"""
        return x1 + x2
    
    def __subtract(x1: float, x2: float) -> 'float':
        """Subtracts two expressions (x1 - x2)"""
        return x1 - x2
    
    def __multiply(x1: float, x2: float) -> 'float':
        """Multiplies two expressions (x1 * x2)"""
        return x1*x2
    
    def __divide(x1: float, x2: float) -> 'float':
        """Divides two expressions (x1 / x2)"""
        return x1/x2
    
    def __join_expressions(self, expressions: list['Expression'], split: str = "") -> 'Expression':
        """Joins a list of expressions together"""
        return Expression(value = split.join([exp.value for exp in expressions]))
    
    def __outermost_delimiter_indicies(self) -> tuple[int, int]:
        """Returns the indices of the FIRST outermost delimiter in an expression"""
        exp_lst = self.__construct_expression_list()
        return Expression.__outermost_delimiter_indicies(exp_lst)
    
    def __outermost_delimiter_indicies(expressions: list['Expression']) -> tuple[int, int]:
        """Returns the indices of the FIRST outermost delimiter in an expression list"""
        #TODO: Implement a more efficient algorithm + generalize
        stack = deque() # type: deque[int]

        start_index = None
        i = 0
        while i < len(expressions):
            if expressions[i].type == ExpressionType.DELIMITER_OPEN:
                if len(stack) == 0:
                    start_index = i
                stack.append(i)
            elif expressions[i].type == ExpressionType.DELIMITER_CLOSED:
                open_delim_index = stack.pop()
                assert expressions[open_delim_index] == expressions[i].__get_corresponding_delimiter() 
                
                if len(stack) == 0:
                    break
            i += 1

        return (start_index, i)
    
    def __construct_expression_list(self) -> list['Expression']:
        """Constructs a list of expressions from the expression
        EX: 3 - 2 * (5 + 1) -> [3, -, 2, *, (, 5, +, 1, )]"""
        #TODO: ADD SUPPORT FOR UNARY OPERATORS

        # Base Case: Expression is a number or None
        if self.value is None or self.type == ExpressionType.NUMERIC:
            return [self]
        
        # split the expression by operators and delimiters
        SPLITS = list(Expression.DELIMITERS.keys()) + list(Expression.DELIMITERS.values()) + list(Expression.OPERATORS.keys())

        # Combine the split points into a regex pattern
        split_pattern = "|".join(map(re.escape, SPLITS)) + "|[^" + "".join(map(re.escape, SPLITS)) + "]+"

        result = re.findall(split_pattern, self.value)
        result = [Expression(value = x) for x in result if len(x) > 0 and x != ' ']

        return result
    
    def __construct_expression_tree(self) -> Node:
        """Constructs an expression tree from the expression
        Runtime: O(n^2)
        Space Comlexity: O(n)

        TODO: Implement O(n) solution using stack
        """
        # Base Case: Expression is a number or None
        if self.value is None or self.type == ExpressionType.NUMERIC:
            return Node(val = self)
        
        # Construct expression list from expression
        exp_lst = self.__construct_expression_list()
        assert len(exp_lst) >= 3

        #TODO: Collapase Case 1 and Case 2 to reduce code
       
        # Case 1: Expression is a single number. Return the number operated with remaining expression
        if exp_lst[0].type == ExpressionType.NUMERIC:
            # Ensure next item is an operator
            # TODO: Add support for multiplication without * (ex: 3(2+1))
            assert exp_lst[1].__is_operator()
            parent = Node(val = exp_lst[1])

            left_child = Node(val = exp_lst[0])
            right_child = self.__join_expressions(exp_lst[2:]).__construct_expression_tree()

            parent.left = left_child
            parent.right = right_child

            return parent
        
        # Case 2: Expression is a single delimiter. Construct tree with expression inside delimiter
        if exp_lst[0].__is_delimiter():
            i = Expression.__outermost_delimiter_indicies(exp_lst)[1]

            new_exp = self.__join_expressions(exp_lst[1:i])  # type: Expression
            new_exp = new_exp.__construct_expression_tree() # type: Node

            # If no other expressions, return the tree from the expression inside the delimiter
            if i >= len(exp_lst) - 1:
                return new_exp
            
            # Otherwise, construct tree with remaining expression
            # TODO: Add support for multiplication without * (ex: 3(2+1))
            assert exp_lst[i+1].__is_operator() 

            parent = Node(val = exp_lst[i+1])
            parent.left = new_exp
            parent.right = self.__join_expressions(exp_lst[i+2:]).__construct_expression_tree() # type: Node
            return parent
        

        if exp_lst[0].__is_operator():
            # TODO: Implement unary operators (e.g. -5, -3*(2+1), -(3+2), +3 + 5)
            
            raise NotImplementedError("Expression.__construct_expression_tree: Unary operators not implemented")

        
    def __collapse_expression_tree(head: Node) -> Node:
        """Collapses an expression tree into a single expression node (evaluates the expression)"""
        # Base Case: Head is None
        if head is None:
            return None
        
        # Base Case: Head is a number
        if head.val.type == ExpressionType.NUMERIC:
            assert head.left is None and head.right is None
            return head

        if head.val.__is_operator():
            # Collapse left and right subtrees
            left_tree = Expression.__collapse_expression_tree(head.left)
            assert left_tree is not None 
            left_exp = left_tree.val
            assert left_exp.type == ExpressionType.NUMERIC
   
            right_tree = Expression.__collapse_expression_tree(head.right)
            assert right_tree is not None 
            right_exp = right_tree.val
            assert right_exp.type == ExpressionType.NUMERIC
     
            # Construct new expression with collapsed subtrees + operator
            OPERATOR_TO_FUNC = {ExpressionType.OPERATOR_ADD: Expression.__add,
                                ExpressionType.OPERATOR_SUBTRACT: Expression.__subtract,
                                ExpressionType.OPERATOR_MULTIPLY: Expression.__multiply,
                                ExpressionType.OPERATOR_DIVIDE: Expression.__divide}
            new_exp = left_exp.__perform_operation(right_exp, OPERATOR_TO_FUNC[head.val.type])

            assert new_exp is not None
            return Node(val = new_exp)
    
        raise RuntimeError("Head value should be operator or number")
    
    def __evaluate_expression(self) -> 'Expression':
        # Construct expression tree
        root = self.__construct_expression_tree()

        # Evaluate expression tree
        root = Expression.__collapse_expression_tree(root)

        return root.val


    ######################################
    #                 API                #
    ######################################
    
    ## Evaluation
    def expression_evaluate(self) ->'Expression':
        """Evaluates the expression
        Returns: Evaluated Expression Object"""
        if self.evaluation is not None:
            return self.evaluation
        
        if not self.valid: 
            raise RuntimeError("Not a valid a expression.")
        
        return self.__evaluate_expression()


    ## GETTERS
    def expression_get_value(self) -> str:
        """Returns the value of the expression
        Returns: String"""
        return self.value
    
    def expression_get_type(self) -> ExpressionType:
        """Returns the type of the expression
        Returns: ExpressionType"""
        return self.type
    

    


