## Test Laxer output


PS C:\Users\Dell\Compiler Project\Compiler-Project> uv run pytest tests/test_lexer.py -v
================================================================= test session starts ==================================================================
platform win32 -- Python 3.13.7, pytest-9.0.3, pluggy-1.6.0 -- C:\Users\Dell\Compiler Project\Compiler-Project\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Dell\Compiler Project\Compiler-Project
configfile: pyproject.toml
collected 18 items                                                                                                                                      

tests/test_lexer.py::test_int_declaration PASSED                                                                                                  [  5%]
tests/test_lexer.py::test_string_declaration PASSED                                                                                               [ 11%]
tests/test_lexer.py::test_assignment_with_arithmetic PASSED                                                                                       [ 16%]
tests/test_lexer.py::test_string_literal_strips_quotes PASSED                                                                                     [ 22%]
tests/test_lexer.py::test_keywords PASSED                                                                                                         [ 27%]
tests/test_lexer.py::test_else_keyword PASSED                                                                                                     [ 33%]
tests/test_lexer.py::test_operators PASSED                                                                                                        [ 38%]
tests/test_lexer.py::test_parentheses_and_braces PASSED                                                                                           [ 44%]
tests/test_lexer.py::test_multiline_line_numbers PASSED                                                                                           [ 50%]
tests/test_lexer.py::test_column_tracking PASSED                                                                                                  [ 55%]
tests/test_lexer.py::test_empty_input PASSED                                                                                                      [ 61%]
tests/test_lexer.py::test_whitespace_only PASSED                                                                                                  [ 66%]
tests/test_lexer.py::test_numeric_literal_parsed_as_int PASSED                                                                                    [ 72%]
tests/test_lexer.py::test_identifier_with_underscore PASSED                                                                                       [ 77%]
tests/test_lexer.py::test_identifier_not_confused_with_keyword PASSED                                                                             [ 83%]
tests/test_lexer.py::test_string_concat_tokens PASSED                                                                                             [ 88%]
tests/test_lexer.py::test_invalid_character_raises PASSED                                                                                         [ 94%]
tests/test_lexer.py::test_unterminated_string_raises PASSED                                                                                       [100%]

================================================================== 18 passed in 0.06s ==================================================================



## Test Parser output

(compiler-project) PS C:\Users\Dell\Compiler Project\Compiler-Project> uv run pytest tests/test_parser.py -v
================================================================= test session starts ==================================================================
platform win32 -- Python 3.13.7, pytest-9.0.3, pluggy-1.6.0 -- C:\Users\Dell\Compiler Project\Compiler-Project\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Dell\Compiler Project\Compiler-Project
configfile: pyproject.toml
collected 16 items                                                                                                                                      

tests/test_parser.py::test_int_declaration PASSED                                                                                                 [  6%]
tests/test_parser.py::test_string_declaration PASSED                                                                                              [ 12%]
tests/test_parser.py::test_assignment_number PASSED                                                                                               [ 18%]
tests/test_parser.py::test_assignment_string_literal PASSED                                                                                       [ 25%]
tests/test_parser.py::test_assignment_identifier PASSED                                                                                           [ 31%]
tests/test_parser.py::test_binary_op_addition PASSED                                                                                              [ 37%]
tests/test_parser.py::test_chained_addition PASSED                                                                                                [ 43%]
tests/test_parser.py::test_string_concat PASSED                                                                                                   [ 50%]
tests/test_parser.py::test_multiple_statements PASSED                                                                                             [ 56%]
tests/test_parser.py::test_program_node_type PASSED                                                                                               [ 62%]
tests/test_parser.py::test_line_and_column_on_decl PASSED                                                                                         [ 68%]
tests/test_parser.py::test_empty_program PASSED                                                                                                   [ 75%]
tests/test_parser.py::test_missing_semicolon_raises PASSED                                                                                        [ 81%]
tests/test_parser.py::test_missing_assign_raises PASSED                                                                                           [ 87%]
tests/test_parser.py::test_unknown_token_raises PASSED                                                                                            [ 93%]
tests/test_parser.py::test_incomplete_expression_raises PASSED                                                                                    [100%]

================================================================== 16 passed in 0.07s ==================================================================


## Test Semantic output 


(compiler-project) PS C:\Users\Dell\Compiler Project\Compiler-Project> uv run pytest tests/test_semantic.py -v
================================================================= test session starts ==================================================================
platform win32 -- Python 3.13.7, pytest-9.0.3, pluggy-1.6.0 -- C:\Users\Dell\Compiler Project\Compiler-Project\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Dell\Compiler Project\Compiler-Project
configfile: pyproject.toml
collected 18 items                                                                                                                                      

tests/test_semantic.py::test_int_declaration_populates_symbol_table PASSED                                                                        [  5%]
tests/test_semantic.py::test_string_declaration_populates_symbol_table PASSED                                                                     [ 11%]
tests/test_semantic.py::test_int_assignment_passes PASSED                                                                                         [ 16%]
tests/test_semantic.py::test_string_assignment_passes PASSED                                                                                      [ 22%]
tests/test_semantic.py::test_int_addition_passes PASSED                                                                                           [ 27%]
tests/test_semantic.py::test_string_concat_passes PASSED                                                                                          [ 33%]
tests/test_semantic.py::test_assign_from_identifier_passes PASSED                                                                                 [ 38%]
tests/test_semantic.py::test_multiple_variables PASSED                                                                                            [ 44%]
tests/test_semantic.py::test_chained_int_addition PASSED                                                                                          [ 50%]
tests/test_semantic.py::test_undeclared_variable_assign_raises PASSED                                                                             [ 55%]
tests/test_semantic.py::test_undeclared_variable_in_expr_raises PASSED                                                                            [ 61%]
tests/test_semantic.py::test_duplicate_declaration_raises PASSED                                                                                  [ 66%]
tests/test_semantic.py::test_assign_string_to_int_raises PASSED                                                                                   [ 72%]
tests/test_semantic.py::test_assign_int_to_string_raises PASSED                                                                                   [ 77%]
tests/test_semantic.py::test_mixed_type_addition_raises PASSED                                                                                    [ 83%]
tests/test_semantic.py::test_assign_string_var_to_int_raises PASSED                                                                               [ 88%]
tests/test_semantic.py::test_semantic_error_has_line PASSED                                                                                       [ 94%]
tests/test_semantic.py::test_semantic_error_message_contains_variable_name PASSED                                                                 [100%]

================================================================== 18 passed in 0.06s ==================================================================