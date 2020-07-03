import re
from collections import OrderedDict

from src.library.convert_string_to_type import convert_string_to_type

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
            # split by ' or ' and ', ' and '|' and '/'
            hint = re.split(r'([,\|/]| or )', hint)
            hint = [item for item in hint if not ((item == ',') or (item ==' or ') or (item == '') or (item == '|') or (item == '/'))]

            # reattatch sliced parts within brackets .+[.+]
            h = []
            i = 0
            while i in range(len(hint)):
                if '[' in hint[i]:
                    j = i
                    while ']' not in hint[j]:
                        j += 1
                    if ']' in hint[j]:
                        h.append(','.join(hint[i:j+1]))
                        i = j
                    i += 1
                else:
                    h.append(hint[i])
                    i += 1
            hint = h
            '''
            to_remove = []
            for i in range(len(hint)):
                if '[' in hint[i] and ']' not in hint:
                    hint_to_add = hint[i]
                    to_remove.append(i)
                    j = i+1
                    while j < len(hint) and ']' not in hint[j]:
                        to_remove.append(j)
                        hint_to_add = hint_to_add + ',' + hint[j]

                    hint.append(hint_to_add)
            # remove the unwanted parts
            for i in to_remove[::-1]:
                hint.pop(i)'' \
            '''
            for i in range(len(hint)):
                # extract type from ...'type'...
                # remove 'of ...'
                hint[i] = re.split(r' of ', hint[i])[0]
                # remove '/...'
                hint[i] = re.split(r'/', hint[i])[0]

                hint[i] = hint[i].strip(' ,~/\\')
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
        expr = r'^\s+(.+?)\s?(\(.+?\))?:\s(.+)'  # type info in front of : , within ()
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
            hint = re.split(r',? \(?optional\)?', hint)[0]
            # cut default part
            hint = re.split(r',? ?default', hint)[0]
            # cut of shape ... part
            hint = re.split(r' of ', hint)[0]
            hint = re.split(r', (shape)', hint)[0]
            # cut limitations like >x,  greater than, equals, ...
            hint = re.split(r' ?[!<>=]+ ? [0-9a-z]+', hint)[0]
            hint = re.split(r' (greater|equal|less)s? ', hint)[0]
            # handle {...} set of possible types/ strings/ ...
            braces = re.findall(r'\{(.+?)\}', hint)
            if braces != []:
                braces = re.split(r' ?[,/\|] ?', braces[0])
            strs = []
            for br in braces:
                if "'" in br:
                    strs.append(br)
            if strs != []:
                for s in strs:
                    braces.remove(s)
                braces.append('str')
            # split multi hints divided by ',' , '|' and 'or' in list
            hint = re.split(r'\{', hint)[0]
            hint = re.split(r'(, | \| | or |/)', hint)
            contains_strs = False
            to_remove = []
            to_add = []
            for hnt in hint:
                # slice by ' in ' :
                if re.split(r' in ', hnt)[0] != hnt:
                    to_remove.append(hnt)
                    hnt = re.split(r' in ', hnt)[0]
                    to_add.append(hnt)
                # find slicing mistakes to remove
                if ((hnt == ', ') or (hnt == ' or ') or (hnt == ' | ') or (hnt == '') or (hnt == '/')) and hnt not in to_remove:
                    to_remove.append(hnt)
                # find strings to replace with 'str'
                if "'" in hnt and hnt not in to_remove:
                    to_remove.append(hnt)
                    if 'str' not in to_add:
                        to_add.append('str')
            for item in to_remove:
                hint.remove(item)
            for item in to_add:
                if (item == 'str' and 'string' not in hint) or (item != 'str' and item not in hint):
                    hint.append(item)
            for br in braces:
                if br not in hint:
                    hint.append(br)

            # clean up hints
            for i in range(len(hint)):
                hint[i] = hint[i].strip(', ')

        # params like '.. asdfe' are comments so ignore them
        if '.. ' not in param:
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

    # divide param_section in list of (param_name, type_info) tuples
    if param_section is not None:
        expr = r'\n*\s*(.+?) ?: ?(.*?)?\n'
        params = re.compile(expr, re.MULTILINE)
        p = params.findall(param_section)
        return p
    return None


def _find_hint_from_param_desc_rest_style(descriptions):
    param_hints = {}
    for item in descriptions:
        param = item[0]
        desc = item[1]

        if 'return' not in param:
            param_hints[param] = []

            # if (...): then there lies the type hint
            if re.search(r'\(.+\):', desc):
                hint = re.split(r'\((.+)\):', desc)[1]
                # change that to description for further analysis
                desc = hint
            # cut 'of shape ...' and ',if ...'
            desc = re.split(r'[ ,]of ', desc)[0]
            desc = re.split(r'[ ,]if ', desc)[0]

            # split text by 'or' to seperate multiple types
            hints = re.split(r' +or +', desc)
            for h in hints:
                # strip a/the normalized ... object
                hnt = re.split(r'object ?\.?', h)[0]
                hnt = re.split(r' ?a ', hnt)[-1]
                hnt = re.split(r' ?the ', hnt)[-1]
                hnt = re.split(r' ?normalized ', hnt)[-1]
                hnt = re.split(r' ?\(OPTIONAL\) ', hnt)[-1]

                # remove , . whitespaces
                hnt = hnt.strip()
                hnt = hnt.strip(',.')
                if hnt != '':
                    param_hints[param].append(hnt)

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

    return None


def _get_param_hint_strings_from_doc_string(doc_string: str):

    if _find_parameter_hint_string_numpydoc_style(doc_string) is not None:
        # print('numpy')
        descs = _find_parameter_hint_string_numpydoc_style(doc_string)
        print(descs)
        hint_list = _find_hint_from_param_desc_numpydoc_style(descs)
        print(hint_list)
        return hint_list

    elif _find_parameter_hint_string_google_style(doc_string) is not None:
        descs = _find_parameter_hint_string_google_style(doc_string)
        hint_list = _find_hint_from_param_desc_google_style(descs)
        return hint_list

    elif _find_parameter_hint_string_rest_style(doc_string) is not None:
        descs = _find_parameter_hint_string_rest_style(doc_string)
        hint_list = _find_hint_from_param_desc_rest_style(descs)
        return hint_list

    # epy style removed because it is not used and there are no examples to work on
    # elif _find_parameter_hint_string_epy_style(doc_string) is not None:
    #     descs = _find_parameter_hint_string_epy_style(doc_string)
    #     return _find_hint_from_param_desc_epy_style(descs)

    else:
        return None


def _find_parameter_hint_in_doc_string(param_names, doc_string: str):
    type_hints = OrderedDict()
    param_list = _get_param_hint_strings_from_doc_string(doc_string)
    if param_list is not None:
        for param in param_list:
            param_name = param
            param_hints = param_list[param]

            if param_name in param_names:
                for i in range(len(param_hints)):
                    hint = param_hints[i]
                    # change strings to str
                    if "'" in hint:
                        hint = 'str'
                    # remove outer whitespace
                    hint = hint.strip(',')
                    hint = hint.strip(' ')
                    # remove numbers
                    hint = re.split(r'[0-9]+-*', hint)[-1]
                    # print(hint)
                    hint = convert_string_to_type(hint)
                    param_hints[i] = hint
                    # print(hint)

            if param_hints == []:
                param_hints = None

            type_hints[param_name] = param_hints
        return [type_hints]
    return None
