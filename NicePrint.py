"""
Provide easy-to-use, minimal typing required
overlay for using Colorama in CLI.
Designed with black command line background in mind.
"""

from colorama import init
from colorama import Fore
from colorama import Back
from colorama import Style

# Remember whether the newest message should begin from a new line or not.
last_continuous = False

# Remember whether Colorama has been initialized.
initialized = False

def _init():
    """ Initialize the module. Required for Colorama. Called automatically. """
    init()
    initialized = True

def nice_print(code, message):
    """
    Provide shorthand for printing colored messages with colorama.

    Code should include any number of the following characters:
    e = error
    w = warn
    h = help
    i - info
    s = success
    x = whitespace

    c = continuous (don't break line afterwards)
    v = variable (highlight)

    Usage example:
        nice_print('ec', 'Beginning of a long ')
        nice_print('ec', 'error message with a ')
        nice_print('ecv' 'highlighted ')
        nice_print('e' value in the middle of the text.')
    """
    if not initialized:
        _init()
    
    global last_continuous
    color = ''
    
    if 'e' in code:
        color = Back.RED
    elif 'w' in code:
        color = Back.YELLOW
        if 'v' not in code:
            color += Fore.BLACK
    elif 'h' in code:
        color = Fore.YELLOW
    elif 'i' in code:
        color = Fore.CYAN
    elif 's' in code:
        color = Fore.GREEN
    elif 'x' in code:
        color = Back.WHITE

    if 'v' in code:
        color += Style.BRIGHT

    if not last_continuous:
        print('  ', end='')
        
    if 'c' in code:
        print(color + message + Style.RESET_ALL, end='')
        last_continuous = True
    else:
        print(color + message + Style.RESET_ALL)
        last_continuous = False

def smart_print(code, message):
    """
    Provide shorthand for using the shorthand when
    interspersed with variables/highlighted values.

    Usage example:
        smart_print('e', '%Short%, but with %a lot% of very %important% stuff.')
    """
    if not initialized:
        _init()
        
    if 'v' in code:
        raise ValueError("'v' is unsupported in smart_print!")
    highlighted = False
    msgs = message.split('%')
    for i in range(len(msgs)):
        msg_code = code
        msg_code += 'v' if highlighted else ''
        msg_code += 'c' if i < len(msgs) - 1 else ''
        nice_print(msg_code, msgs[i])
        highlighted = not highlighted
