# calculator_logic.py

import math
import re

# calculator_logic.py

import math
import re


class EngineeringCalculator:
    def __init__(self):
        self.precedence = {
            '+': 1, '-': 1, '*': 2, '/': 2, 'yroot': 3, '^': 3, '~': 4,
            '!': 5, 'sin': 5, 'cos': 5, 'tan': 5, 'log': 5, 'ln': 5,
            'sqrt': 5, 'cbrt': 5, 'exp': 5, 'tenpow': 5, 'recip': 5,
            '(': 0
        }
        self.unary_operators = {
            'sin', 'cos', 'tan', 'log', 'ln', 'sqrt', 'cbrt',
            'exp', 'tenpow', 'recip', '!', '~'
        }
        self.binary_operators = {'+', '-', '*', '/', '^', 'yroot'}
        self.is_degree_mode = True

    def toggle_angle_mode(self) -> str:
        self.is_degree_mode = not self.is_degree_mode
        return "Deg" if self.is_degree_mode else "Rad"

    def tokenize(self, expression: str) -> list:
        TOKEN_REGEX = re.compile(r"""
            (?P<NUMBER>    \d+(\.\d+)?(E-?\d+)?) |
            (?P<FUNCTION>  sin|cos|tan|log|ln|sqrt|cbrt|exp|tenpow|recip|yroot) |
            (?P<OPERATOR>  [+\-*/^!]) |
            (?P<LPAREN>    \() |
            (?P<RPAREN>    \))
        """, re.VERBOSE)
        expression = expression.replace(" ", "")
        tokens = []
        last_token_was_operator = True
        for match in TOKEN_REGEX.finditer(expression):
            kind, value = match.lastgroup, match.group()
            if kind == 'OPERATOR' and value == '-' and last_token_was_operator:
                tokens.append('~')
            elif kind == 'NUMBER':
                tokens.append(float(value))
                last_token_was_operator = False
            else:
                tokens.append(value)
                last_token_was_operator = kind in ('OPERATOR', 'LPAREN', 'FUNCTION')
        return tokens

    def to_postfix(self, tokens: list) -> list:
        postfix_stack, operator_stack = [], []
        for token in tokens:
            if isinstance(token, float):
                postfix_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    postfix_stack.append(operator_stack.pop())
                if operator_stack: operator_stack.pop()  # Pop '('
                if operator_stack and operator_stack[-1] in self.unary_operators:
                    postfix_stack.append(operator_stack.pop())
            else:
                while (operator_stack and operator_stack[-1] != '(' and
                       self.precedence.get(operator_stack[-1], -1) >= self.precedence.get(token, -1)):
                    postfix_stack.append(operator_stack.pop())
                operator_stack.append(token)
        while operator_stack:
            postfix_stack.append(operator_stack.pop())
        return postfix_stack

    def evaluate_postfix(self, postfix_tokens: list):
        calculator_stack = []
        for token in postfix_tokens:
            if isinstance(token, float):
                calculator_stack.append(token)
            elif token in self.binary_operators:
                if len(calculator_stack) < 2: raise ValueError("Invalid binary operation")
                op2, op1 = calculator_stack.pop(), calculator_stack.pop()
                if token == '+':
                    result = op1 + op2
                elif token == '-':
                    result = op1 - op2
                elif token == '*':
                    result = op1 * op2
                elif token == '^':
                    result = op1 ** op2
                elif token == 'yroot':
                    if op1 == 0: raise ValueError("0th root is undefined")
                    result = op2 ** (1 / op1)
                elif token == '/':
                    if op2 == 0: raise ZeroDivisionError("Division by zero")
                    result = op1 / op2
                calculator_stack.append(result)
            elif token in self.unary_operators:
                if len(calculator_stack) < 1: raise ValueError("Invalid unary operation")
                op = calculator_stack.pop()
                if token == '~':
                    result = -op
                elif token == '!':
                    if op < 0 or op != int(op): raise ValueError("Factorial is for non-negative integers")
                    result = float(math.factorial(int(op)))
                else:  # 모든 함수는 여기서 처리
                    if token in ['sin', 'cos', 'tan'] and self.is_degree_mode:
                        op = math.radians(op)

                    if token == 'sin':
                        result = math.sin(op)
                    elif token == 'cos':
                        result = math.cos(op)
                    elif token == 'tan':
                        result = math.tan(op)
                    elif token == 'log':
                        if op <= 0: raise ValueError("Log domain error")
                        result = math.log10(op)
                    elif token == 'ln':
                        if op <= 0: raise ValueError("Log domain error")
                        result = math.log(op)
                    elif token == 'sqrt':
                        if op < 0: raise ValueError("Sqrt domain error")
                        result = math.sqrt(op)
                    elif token == 'cbrt':
                        result = op ** (1 / 3) if op >= 0 else -(-op) ** (1 / 3)
                    elif token == 'exp':
                        result = math.exp(op)
                    elif token == 'tenpow':
                        result = 10 ** op
                    elif token == 'recip':
                        if op == 0: raise ZeroDivisionError("Division by zero")
                        result = 1 / op
                calculator_stack.append(result)
        if len(calculator_stack) != 1: raise ValueError("Malformed expression")
        return calculator_stack[0]

    def apply_percentage(self, expression: str) -> str:
        match = re.search(r'(?P<num1>[\d\.]+(E-?\d+)?)\s*(?P<op>[+\-*/])\s*(?P<num2>[\d\.]+(E-?\d+)?)$', expression)
        if match:
            num1, op, num2 = float(match.group('num1')), match.group('op'), float(match.group('num2'))
            prefix = expression[:match.start()]
            if op in ['+', '-']:
                result = num1 + (num1 * num2 / 100) if op == '+' else num1 - (num1 * num2 / 100)
            else:  # op in ['*', '/']
                result = num1 * (num2 / 100) if op == '*' else num1 / (num2 / 100)
            return prefix + str(result)
        match_single = re.fullmatch(r'([\d\.]+(E-?\d+)?)', expression)
        if match_single:
            return str(float(match_single.group(0)) / 100)
        return expression

    def toggle_last_number_sign(self, expression: str) -> str:
        match = re.search(r'(-?[\d\.]+(E-?\d+)?)$', expression)
        if match:
            last_number_str, start_pos = match.group(0), match.start(0)
            if float(last_number_str) == 0: return expression
            prefix_part = expression[:start_pos]
            new_number_part = last_number_str[1:] if last_number_str.startswith('-') else '-' + last_number_str
            return prefix_part + new_number_part
        return expression

    def calculate(self, expression: str):
        try:
            tokens = self.tokenize(expression)
            postfix_tokens = self.to_postfix(tokens)
            result = self.evaluate_postfix(postfix_tokens)
            return result
        except ZeroDivisionError:
            return "0으로 나눌 수 없음"
        except (ValueError, IndexError):
            return "수식 오류"
        except Exception:
            return "알 수 없는 오류"




if __name__ == '__main__':
    # 1. 계산기 로직 객체 생성
    calculator = EngineeringCalculator()

    # 2. 테스트해 볼 수식 목록 정의
    test_cases = [
        "5 + 3 * 2",  # 연산자 우선순위
        "5 * (3 + 2)",  # 괄호
        "10 / 2 - 3",  # 순차 계산
        "2^3",  # 거듭제곱
        "sin(90)",  # sin 함수 (Degree 모드)
        "cos(0)",  # cos 함수
        "log(100)",  # log 함수
        "-5 + 10",  # 단항 마이너스 (맨 앞)
        "10 * -2",  # 단항 마이너스 (중간)
        "sin(90) + cos(0)",  # 함수 조합
        "10 * (log(100) + 2)",  # 복잡한 수식
        "5 / 0",  # 0으로 나누기 오류
        "3 + * 5"  # 잘못된 수식
    ]

    print("--- 계산기 로직 테스트 시작 ---")

    # 3. 각 수식을 순서대로 계산하고 결과 출력
    for expression in test_cases:
        result = calculator.calculate(expression)
        # f-string 포매팅을 사용해 깔끔하게 출력
        print(f"입력: {expression:<25} 결과: {result}")

    print("--- 테스트 종료 ---")