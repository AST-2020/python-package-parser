import re

def _find_parameter_hint_epy_style(doc_string):
    '''
    search epy text docstrings for parameters
    epy text examples:
    "@param(s) param_name: description"
    "@params param_name :description"
    '''
    expr = r'@\s?params?\s(.+?)\s?:\s*(.+?)\n+'
    params = re.compile(expr, re.MULTILINE)

    if doc_string is None:
        return None

    p = params.findall(doc_string)
    if p != []:
        return p
    return None

def _find_parameter_hint_google_style(doc_string):
    '''
    search NumpyDoc style docstrings for parameters
    This is an example of Google style.

    Args:
        param1: This is the first param.
        param2: This is a second param.

    Returns:
        This is a description of what is returned.

    Raises:
        KeyError: Raises an exception.
    '''
    param_section = None
    # used keywords to references sections within the docstings
    wanted_sections = ["Args", "Arg", "Parameter", "Param", "Parameters"]
    unwanted_sections = ['Returns', 'Notes', 'See also', 'Examples', 'References', 'Yields', 'Raises', 'Warns']
    # create regex compiler
    expr = r'\s*({}):?\n+'.format('|'.join(wanted_sections+unwanted_sections))
    sections = re.compile(expr, re.M|re.S)

    if doc_string is None:
        return None

    # isolate parameter section
    section = sections.split(doc_string)
    if section is not None:
        for i in range(len(section)-1):
            if section[i] in wanted_sections:
                param_section = section[i+1]

    # extract params
    if param_section is not None:
        expr = r'^\s+(.+?)\s?:\s(.+)'
        params = re.compile(expr, re.M)
        p = params.findall(param_section)
        return p

    return None

def _find_parameter_hint_numpydoc_style(doc_string):
    '''
    search NumpyDoc style docstrings for parameters
    example:
        "Parameter(s)
        --------------
        first : array_like
            the 1st param name `first`
        second :
            the 2nd param
        third : {'value', 'other'}, optional
            the 3rd param, by default 'value'"
    '''
    # --- isolate parameter section ---
    param_section = None
    # used keywords to references sections within the docstings
    keywords = ['Parameters', 'Parameter', 'Returns', 'Notes', 'See also', 'Examples', 'References', 'Yields', 'Raises',
                'Warns']
    # create regex compiler
    expr = r'\n*\s*({})\n\s*-+\n'.format('|'.join(keywords))
    sections = re.compile(expr, re.M)

    # if doc_string is not empty, split by keywords in text sections
    if doc_string is None:
        return None

    splits = sections.split(doc_string)
    for i in range(len(splits)-1):
        if "Parameter" in splits[i]:
            # store found sections and contents in a dict
            param_section = splits[i + 1].lstrip('\n')

    # --- divide param_section in list of (param_name, type_info) touples---
    if param_section is not None:
        expr = r'\n*\s*(.+?) ?: ?(.*?)\n'
        params = re.compile(expr, re.MULTILINE)
        p = params.findall(param_section)
        return p
    return None

def _find_parameter_hint_rest_style(doc_string):
    '''
    search reST style docstrings for parameters
    reSt style examples:
    ":param(s) param_name: description"
    ":params param_name :description"
    '''
    expr = r':\s?params?\s(.+?)\s?:\s*(.+?)\n+'
    params = re.compile(expr, re.MULTILINE)

    if doc_string is None:
        return None

    p = params.findall(doc_string)
    if p != []:
        return p
    return None

def _find_parameter_hint_in_doc_string(doc_string: str):
    param_list = None

    param_list = _find_parameter_hint_numpydoc_style(doc_string)
    # if  not numpydoc style
    if param_list is None:
        param_list = _find_parameter_hint_rest_style(doc_string)

    # if not reST doc style
    if param_list is None:
        param_list = _find_parameter_hint_epy_style(doc_string)

    # if not epy doc style
    if param_list is None:
        param_list = _find_parameter_hint_google_style(doc_string)

    # if not google doc style
    if param_list is None:
        return None

    # call function to extract type and default from param_list here