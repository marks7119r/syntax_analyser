import re

# Token categories
IDENTIFIER = 'IDENTIFIER'
NUMBER = 'NUMBER'
OPERATOR = 'OPERATOR'
ASSIGN = 'ASSIGN'
LPAREN = "LPAREN"
RPAREN = "RPAREN"
DATATYPE = "DATATYPE"
EOF = 'EOF'

# Tokenization Regex
tokensRegex = [
    (r'\b(int|float|string|char|bool)\b', DATATYPE),  #---> put it first to catch the first match
    (r'[a-zA-Z_][a-zA-Z_0-9]*', IDENTIFIER),  # Identifiers (e.g., var, x, test1)
    (r'\d+(\.\d*)?|\.\d+', NUMBER),  # Numbers (e.g., 123, 45.67, .23)
    (r'[+\-*/%~!]', OPERATOR),  # Operators (+, -, *, /, %)
    (r'=', ASSIGN),
    (r'\(', LPAREN),    # Left parenthesis
    (r'\)', RPAREN),    # Right parenthesis
    (r'\s+', None),  # Skip whitespace
]

# Tokenization (Lexical Analyzer)
def tokenize(input_string):
    tokens = []
    position = 0
    while position < len(input_string):
        match = None
        for pattern, token in tokensRegex:
            regex = re.compile(pattern)
            match = regex.match(input_string, position)
            if match:
                value = match.group(0)
                if token:  # Skip None types (whitespace)
                    tokens.append((token, value))
                position = match.end()
                break
        if not match:
            raise SyntaxError(f"Illegal character at position {position}")
    tokens.append((EOF, ''))  # indicate end of input
    return tokens

def parse(tokens):
    # Start by parsing assignments
    node = parse_assignment(tokens)
    
    if tokens and tokens[0][0] != EOF:
        raise SyntaxError(f"Unexpected tokens at the end: {tokens}")
    
    return node
def parse_assignment(tokens):
    # Expect a data type (optional)
    checkDataType = False
    dataType = None
    if tokens and tokens[0][0] == DATATYPE:  # Check if there's a data type
        token_type, dataType = tokens.pop(0)
        checkDataType = True  # Set to True to indicate that a data type was found

    # Expect an identifier, an assignment operator, and an expression
    token_type, value = tokens.pop(0)
    if token_type != IDENTIFIER:
        raise SyntaxError(f"Expected identifier, got {value}")

    left = {'type': 'Identifier', 'name': value}

    token_type, value = tokens.pop(0)
    if token_type != ASSIGN:
        raise SyntaxError(f"Expected '=', got {value}")
    
    right = parse_expression(tokens)

    # if there is a data type
    if checkDataType:
        return {'Data Type': dataType, 'type': 'Assignment', 'left': left, 'right': right}

    return {'type': 'Assignment', 'left': left, 'right': right}

# Parse tree nodes
def parse_expression(tokens):
    # Parse a term (number or identifier)
    left = parse_term(tokens)
    
    # While we have an operator, continue parsing
    while tokens and tokens[0][0] == OPERATOR and tokens[0][1] in ('+', '-','%'):
        operator = tokens.pop(0)[1]  # Get the operator
        right = parse_term(tokens)
        left = {'type': 'BinaryOperation', 'operator': operator, 'left': left, 'right': right}
    
    return left

def parse_term(tokens):
    # Parse a factor (number or identifier)
    left = parse_factor(tokens)
    
    # While we have an operator, continue parsing
    while tokens and tokens[0][0] == OPERATOR and tokens[0][1] in ('*', '/'):
        operator = tokens.pop(0)[1]  # Get the operator
        right = parse_factor(tokens)
        left = {'type': 'BinaryOperation', 'operator': operator, 'left': left, 'right': right}
    
    return left

def parse_factor(tokens):
    # Get the first token
    token_type, value = tokens.pop(0)

    # Handle unary operators
    if token_type == OPERATOR and value in ('-', '!', '~'):
        operand = parse_factor(tokens)  # Recursively parse the operand
        return {'type': 'UnaryOperation', 'operator': value, 'operand': operand}
    
    # Handle parentheses
    elif token_type == LPAREN:
        expr = parse_expression(tokens)  # Parse the expression inside the parentheses
        token_type, value = tokens.pop(0)
        if token_type != RPAREN:
            raise SyntaxError(f"Expected ')', got {value}")
        return expr
    
    # Handle numbers and identifiers
    elif token_type == NUMBER:
        return {'type': 'Number', 'value': value}
    elif token_type == IDENTIFIER:
        return {'type': 'Identifier', 'name': value}
    else:
        raise SyntaxError(f"Unexpected token '{value}' of type '{token_type}'" )




