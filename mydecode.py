def mydecode(st):
    try:
        encoded_string=st
        encoded_string = encoded_string.replace('%20', ' ')
        encoded_string = encoded_string.replace('%21', '!')
        encoded_string = encoded_string.replace('%22', '"')
        encoded_string = encoded_string.replace('%23', '#')
        encoded_string = encoded_string.replace('%24', '$')
        encoded_string = encoded_string.replace('%25', '%')
        encoded_string = encoded_string.replace('%26', '&')
        encoded_string = encoded_string.replace('%27', "'")
        encoded_string = encoded_string.replace('%28', '(')
        encoded_string = encoded_string.replace('%29', ')')
        encoded_string = encoded_string.replace('%2A', '*')
        encoded_string = encoded_string.replace('%2B', '+')
        encoded_string = encoded_string.replace('%2C', ',')
        encoded_string = encoded_string.replace('%2D', '-')
        encoded_string = encoded_string.replace('%2E', '.')
        encoded_string = encoded_string.replace('%2F', '/')
        encoded_string = encoded_string.replace('%3A', ':')
        encoded_string = encoded_string.replace('%3B', ';')
        encoded_string = encoded_string.replace('%3C', '<')
        encoded_string = encoded_string.replace('%3D', '=')
        encoded_string = encoded_string.replace('%3E', '>')
        encoded_string = encoded_string.replace('%3F', '?')
        encoded_string = encoded_string.replace('%40', '@')
        encoded_string = encoded_string.replace('%5B', '[')
        encoded_string = encoded_string.replace('%5C', '\\')
        encoded_string = encoded_string.replace('%5D', ']')
        encoded_string = encoded_string.replace('%5E', '^')
        encoded_string = encoded_string.replace('%5F', '_')
        encoded_string = encoded_string.replace('%60', '`')
        encoded_string = encoded_string.replace('%7B', '{')
        encoded_string = encoded_string.replace('%7C', '|')
        encoded_string = encoded_string.replace('%7D', '}')
        encoded_string = encoded_string.replace('%7E', '~')
    except Exception as e:
        print(e)
    return encoded_string