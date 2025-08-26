# calculator_logic.py

import math
import re


class EngineeringCalculator:
    def __init__(self):
        # 확장된 연산자 우선순위 딕셔너리
        self.precedence = {
            '+': 1, '-': 1, '*': 2, '/': 2, '^': 3, '~': 4,  # '~'는 단항 마이너스
            'sin': 5, 'cos': 5, 'tan': 5, 'log': 5, 'ln': 5,  # 함수들은 가장 높은 우선순위
            '(': 0
        }
        # 단항 연산자(함수)와 이항 연산자(사칙연산)를 구분하기 위한 집합
        self.unary_operators = {'sin', 'cos', 'tan', 'log', 'ln', '~'}
        self.binary_operators = {'+', '-', '*', '/', '^'}

    def toggle_last_number_sign(self, expression: str) -> str:
        """
        Tokenizer를 믿고, 단순히 마지막 숫자의 부호 문자열만 반전시킵니다.
        """
        # 문자열 끝에서 '음수 부호가 있을 수도 있는 숫자' 패턴을 찾습니다.
        match = re.search(r'(-?\d+(\.\d+)?)$', expression)

        if match:
            last_number_str = match.group(0)
            start_pos = match.start(0)
            prefix_part = expression[:start_pos]

            if float(last_number_str) == 0:
                return expression

            if last_number_str.startswith('-'):
                new_number_part = last_number_str[1:]  # 음수 -> 양수
            else:
                new_number_part = '-' + last_number_str  # 양수 -> 음수

            return prefix_part + new_number_part

        # 숫자를 찾지 못하면 원본 반환
        return expression


    def tokenize(self, expression: str) -> list:
        # 이전에 만들었던 토큰화 함수
        TOKEN_REGEX = re.compile(r"""
            (?P<NUMBER>    \d+(\.\d+)?) |
            (?P<FUNCTION>  sin|cos|tan|log|ln) |
            (?P<OPERATOR>  [+\-*/^]) |
            (?P<LPAREN>    \() |
            (?P<RPAREN>    \))
        """, re.VERBOSE)

        expression = expression.replace(" ", "")
        tokens = []
        last_token_was_operator = True  # 시작은 연산자 뒤로 간주

        for match in TOKEN_REGEX.finditer(expression):
            kind = match.lastgroup
            value = match.group()

            if kind == 'OPERATOR' and value == '-' and last_token_was_operator:
                # 단항 마이너스 처리: '-'를 '~'로 변환
                tokens.append('~')
                last_token_was_operator = True
            elif kind == 'NUMBER':
                if '.' in value:
                    tokens.append(float(value))
                else:
                    tokens.append(int(value))
                last_token_was_operator = False
            else:
                tokens.append(value)
                if kind in ('OPERATOR', 'LPAREN'):
                    last_token_was_operator = True
                else:
                    last_token_was_operator = False
        return tokens

    def to_postfix(self, tokens: list) -> list:
        """중위 표기법 토큰 리스트를 후위 표기법으로 변환합니다."""
        postfix_stack = []
        operator_stack = []

        for token in tokens:
            # 토큰이 숫자인 경우 (기존 parse_input 대체)
            if isinstance(token, (int, float)):
                postfix_stack.append(token)
            # 토큰이 함수인 경우
            elif token in self.precedence and self.precedence[token] == 5:
                operator_stack.append(token)
            # 토큰이 여는 괄호인 경우
            elif token == '(':
                operator_stack.append(token)
            # 토큰이 닫는 괄호인 경우
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    postfix_stack.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()  # '(' 제거
                # 괄호 바로 앞이 함수였다면 함수도 pop
                if operator_stack and operator_stack[-1] in self.unary_operators:
                    postfix_stack.append(operator_stack.pop())

            # 토큰이 연산자인 경우
            else:
                while (operator_stack and
                       self.precedence.get(operator_stack[-1], -1) >= self.precedence.get(token, -1)):
                    postfix_stack.append(operator_stack.pop())
                operator_stack.append(token)

        # 스택에 남은 모든 연산자를 결과에 추가
        while operator_stack:
            postfix_stack.append(operator_stack.pop())

        return postfix_stack

    # calculator_logic.py 파일의 EngineeringCalculator 클래스 내부

    def evaluate_postfix(self, postfix_tokens: list):
        """후위 표기법 리스트를 계산하여 결과를 반환합니다."""
        calculator_stack = []

        for token in postfix_tokens:
            if isinstance(token, (int, float)):
                calculator_stack.append(token)
            else:  # 토큰이 연산자 또는 함수인 경우
                if token in self.binary_operators:
                    if len(calculator_stack) < 2: raise ValueError("Invalid expression")
                    op2 = calculator_stack.pop()
                    op1 = calculator_stack.pop()
                    if token == '+':
                        calculator_stack.append(op1 + op2)
                    elif token == '-':
                        calculator_stack.append(op1 - op2)
                    elif token == '*':
                        calculator_stack.append(op1 * op2)
                    elif token == '^':
                        calculator_stack.append(op1 ** op2)
                    elif token == '/':
                        if op2 == 0: raise ZeroDivisionError("Division by zero")
                        calculator_stack.append(op1 / op2)

                elif token in self.unary_operators:
                    if len(calculator_stack) < 1: raise ValueError("Invalid expression")
                    op = calculator_stack.pop()
                    if token == '~':
                        calculator_stack.append(-op)
                    # Degrees to Radians 변환이 필요한 삼각함수
                    elif token == 'sin':
                        calculator_stack.append(math.sin(math.radians(op)))
                    elif token == 'cos':
                        calculator_stack.append(math.cos(math.radians(op)))
                    elif token == 'tan':
                        calculator_stack.append(math.tan(math.radians(op)))
                    # Hyperbolic 함수 (Radian 불필요)
                    elif token == 'sinh':
                        calculator_stack.append(math.sinh(op))
                    elif token == 'cosh':
                        calculator_stack.append(math.cosh(op))
                    elif token == 'tanh':
                        calculator_stack.append(math.tanh(op))
                    # 로그 함수 (math.log10은 밑이 10인 상용로그, math.log는 밑이 e인 자연로그)
                    elif token == 'log':  # <<< 수정된 부분
                        if op <= 0: raise ValueError("Math Domain Error")
                        calculator_stack.append(math.log10(op))
                    elif token == 'ln':  # <<< 수정된 부분
                        if op <= 0: raise ValueError("Math Domain Error")
                        calculator_stack.append(math.log(op))

        if len(calculator_stack) != 1: raise ValueError("Invalid expression")
        return calculator_stack[0]

    def calculate(self, expression: str):
        """전체 계산 과정을 총괄하는 메인 메소드."""
        try:
            tokens = self.tokenize(expression)
            postfix_tokens = self.to_postfix(tokens)
            result = self.evaluate_postfix(postfix_tokens)
            return result
        except ZeroDivisionError:
            return "0으로 나눌 수 없음"
        except (ValueError, IndexError):  # IndexError는 스택 pop 오류 방지
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