import re

# epy style is not used in current libraries and
# therefore will not be further edited, because of lack of examples
def _find_hint_from_param_desc_epy_style(descriptions):
    pass


def _find_parameter_hint_string_epy_style(doc_string):
    """
    search epy text docstrings for parameters
    epy text examples:
    "@param(s) param_name: description"
    "@params param_name :description"
    """
    expr = r'@\s?params?\s(.+?)\s?:\s*(.+?)\n+'
    params = re.compile(expr, re.MULTILINE)

    if doc_string is None:
        return None

    p = params.findall(doc_string)
    if p != []:
        return p
    return None


def _find_hint_from_param_desc_google_style(descriptions):
    param_hints = {}
    if descriptions is None:
        return None

    # presort given information
    for item in descriptions:
        if len(item) == 3:
            if item[1] != '':
                param_hints[item[0]] = item[1]

    # remove unwanted string parts
    for param in param_hints:
        if param != 'Return':
            # remove brackets
            hint = param_hints[param].lstrip('(').rstrip(')')
            # cut optional part
            hint = re.split(r', optional', hint)[0]
            # split by ' or ' and ', '
            hint = re.split(r'(,| or )', hint)
            for item in hint:
                if (item == ',') or (item ==' or ') or (item == ''):
                    hint.remove(item)

            for i in range(len(hint)):
                # extract type from ...'type'...
                if '`' in hint[i]:
                    hint[i] = re.findall(r':.+?:`(.+?)`', hint[i])[0]
                # remove 'of ...'
                hint[i] = re.split(r' of ', hint[i])[0]
                # remove '/...'
                hint[i] = re.split(r'/', hint[i])[0]

        param_hints[param] = hint

    if param_hints != {}:
        return param_hints

    return None

# hints which are not marked as hints via brackets are ignored

def _find_parameter_hint_string_google_style(doc_string):
    """
    search NumpyDoc style docstrings for parameters
    This is an example of Google style.

    Args:
        param1: This is the first param.
        param2: This is a second param.

    Returns:
        This is a description of what is returned.

    Raises:
        KeyError: Raises an exception.
    """
    param_section = None
    # used keywords to references sections within the docstings
    wanted_sections = ["Args", "Arg", "Parameter", "Param", "Parameters"]
    unwanted_sections = ['Returns', 'Notes', 'See also', 'Examples', 'References', 'Yields', 'Raises', 'Warns']
    # create regex compiler
    expr = r'^\s*:?({}):?\n+'.format('|'.join(wanted_sections + unwanted_sections))
    sections = re.compile(expr, re.M | re.S)

    if doc_string is None:
        return None

    # isolate parameter section
    section = sections.split(doc_string)
    if section is not None:
        for i in range(len(section) - 1):
            if section[i] in wanted_sections:
                param_section = section[i + 1]

    # extract params
    if param_section is not None:
        expr = r'^\s+(.+?)\s?(\(.+?\))?:\s(.+)'  # type info in front of : within ()
        params = re.compile(expr, re.M)
        p = params.findall(param_section)
        return p

    return None


def _find_hint_from_param_desc_numpydoc_style(descriptions):
    param_hints = {}
    # presort given information
    for item in descriptions:
        if len(item) == 2:
            param = item[0]
            hint = item[1]
            # cut optional part
            hint = re.split(r', optional', hint)[0]
            # cut default part
            hint = re.split(r',? ?default', hint)[0]
            # cut of shape ... part
            hint = re.split(r' of shape', hint)[0]
            hint = re.split(r', shape', hint)[0]
            # cut limitations like >x, ...
            hint = re.split(r' ?[!<>=]+ ? [0-9]+', hint)[0]
            # handle {...} set of possible types/ strings/ ...
            braces = re.findall(r'\{(.+?)\}', hint)
            if braces != []:
                braces = re.split(r' ?[,\|] ', braces[0])
            strs = []
            for br in braces:
                if br.strip("'") != br:
                    strs.append(br)
            if strs != []:
                for s in strs:
                    braces.remove(s)
                braces.append('str')
            # print(braces)
            # split multi hints divided by ',' , '|' and 'or' in list
            hint = re.split(r'\{', hint)[0]
            hint = re.split(r'(, | \| | or )', hint)
            for hnt in hint:
                if (hnt == ', ') or (hnt == ' or ') or (hnt == ' | ') or (hnt == ''):
                    hint.remove(hnt)
            for br in braces:
                if br not in hint:
                    hint.append(br)

            # clean up hints
            for h in hint:
                h.strip(',')
                h.strip(' ')

        param_hints[param] = hint

    if param_hints != {}:
        return param_hints
    return None


def _find_parameter_hint_string_numpydoc_style(doc_string):
    """
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
    """
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
    for i in range(len(splits) - 1):
        if "Parameter" in splits[i]:
            # store found sections and contents in a dict
            param_section = splits[i + 1].lstrip('\n')

    # --- divide param_section in list of (param_name, type_info) touples---
    if param_section is not None:
        expr = r'\n*\s*(.+?) ?: (.*?)\n'
        params = re.compile(expr, re.MULTILINE)
        p = params.findall(param_section)
        return p
    return None


def _find_hint_from_param_desc_rest_style(descriptions):
    param_hints = {}
    for item in descriptions:
        param = item[0]

        if param != 'return_type':
            param_hints[param] = []

            # split text by 'or' to seperate multiple types
            splited = re.split(r' +or +', item[1])
            for sp in splited:
                if sp != '':
                    param_hints[param].append(sp)

    return param_hints


def _find_parameter_hint_string_rest_style(doc_string):
    """
    search reST style docstrings for parameters
    reSt style examples:
    ":param(s) param_name: description"
    ":params param_name :description"
    """
    expr = r':\s?params?\s(.+?)\s?:\s*(.+?)\n+'
    params = re.compile(expr, re.MULTILINE)

    if doc_string is None:
        return None

    p = params.findall(doc_string)
    if p != []:
        return p

    # extract type hint from defined position
    return None


def _get_param_hint_strings_from_doc_string(doc_string: str):

    if _find_parameter_hint_string_numpydoc_style(doc_string) is not None:
        descs = _find_parameter_hint_string_numpydoc_style(doc_string)
        print('// new func')
        print(descs)
        hint_list = _find_hint_from_param_desc_numpydoc_style(descs)
        print(hint_list)
        print()
        return hint_list

    elif _find_parameter_hint_string_google_style(doc_string) is not None:
        descs = _find_parameter_hint_string_google_style(doc_string)
        # print('// new func')
        # print(descs)
        hint_list = _find_hint_from_param_desc_google_style(descs)
        # print(hint_list)
        # print()
        return hint_list

    elif _find_parameter_hint_string_rest_style(doc_string) is not None:
        descs = _find_parameter_hint_string_rest_style(doc_string)
        # print('// new func')
        # print(descs)
        hint_list = _find_hint_from_param_desc_rest_style(descs)
        # print(hint_list)
        # print()
        return hint_list

    # epy style removed because it is not used and there are no examples to work on
    # elif _find_parameter_hint_string_epy_style(doc_string) is not None:
    #     descs = _find_parameter_hint_string_epy_style(doc_string)
    #     return _find_hint_from_param_desc_epy_style(descs)

    else:
        return None


def _find_parameter_hint_in_doc_string(doc_string: str):
    param_list = _get_param_hint_strings_from_doc_string(doc_string)
    if param_list is not None:
        # hints = _convert_hint_to_type(param_list)
        # return hints
        return param_list           # remove if str -> type conversion is implemented
    return None
