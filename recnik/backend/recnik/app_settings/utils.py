from configparser import ConfigParser
from itertools import chain
import logging
import os
from django.core.exceptions import ImproperlyConfigured


log = logging.getLogger()


def read_variable(file_name, variable_name, silent=False):
    """
    Reads a variable value from the given config file.
    """
    parser = ConfigParser()
    try:
        with open(file_name) as lines:
            lines = chain(("[top]",), lines)
            parser.read_file(lines)
        var = parser['top'][variable_name]
        if var.upper in ('TRUE', 'FALSE'):
            return bool(var.capitalize())
        return parser['top'][variable_name]
    except IOError as ex:
        if not silent:
            log.fatal(ex)
        return None
    except KeyError as ex:
        if not silent:
            log.fatal(ex)
        raise ImproperlyConfigured(f'Variable not found: {variable_name}')


def get_variable(variable_name, default_value=None):
    """
    Reads a variable value from OS environment.
    """
    if variable_name in os.environ:
        value = os.environ[variable_name]
        log.info(f"Reading variable {variable_name} from environment: {value}")
        return value
    else:
        log.info(f"Using default for variable {variable_name}: {default_value}")
        return default_value


def read_or_get(file_name, variable_name, default_value=None):
    """
    Attempts to read a config variable first from the given file, and if not found then from OS environment.
    """
    try:
        value = read_variable(file_name, variable_name, True)
        if not value:
            value = get_variable(variable_name, default_value)
        return value
    except ImproperlyConfigured:
        return default_value
