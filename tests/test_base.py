from graphalith.base import*

STANDARD_TEST_CASES = ["2 + 3 - 1",
                  "4 * 3 / 2",
                  "(2 + 3) * 4",
                  "((2 + 3) * 4) - (6 / 2)",
                  "((2 + 3) * (4 - 1)) / 5",
                  "[2 * (3 + 1)] - 5",
                  "[(2 + 3) * {4 - 1}] / 5",
                  "{[(2 + 3) * (6 - 3)] / [2 + (8 / 2)]}",
                  "-3 * (4 - 6)",
                  "(2 * 3) + (4 / 2) - (5 + 1)",
                  "1000 / (7 + 3)",
                  "[(2 + 3) * (4 - 1)] / {5 + (6 / 2)}",
                  "7"]

ERROR_TEST_CASES = [ "5 / 0", 
                "",
                "(2 + 3",
                "(2 + [3 - 1))",
                "2 + @ * 3"]

def test_expression_evaluate_standard():
    for case in STANDARD_TEST_CASES:
        eval_exp = Expression(value = case).expression_evaluate()

        translation_table = str.maketrans("[]{}", "()()")
        eval_case = case.translate(translation_table)

        assert float(eval_exp.expression_get_value()) == eval(eval_case), case
        assert eval_exp.expression_get_type() == ExpressionType.NUMERIC, case
        
def test_expression_evaluate_special():
    #TODO: Implement test for failing error cases
    for case in ERROR_TEST_CASES:
        assert True
    assert True

def test_expression_get_value():
    for case in STANDARD_TEST_CASES:
        assert Expression(value = case).expression_get_value() == case, case