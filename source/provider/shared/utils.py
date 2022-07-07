from typing import Mapping, Any, List, Union


# FIXME, meaningful name
def clear_from_ellipsis(
    kwargs: Union[Mapping, List] = {}
) -> Union[Mapping, List]:
    """
    Deletes all keys from dict where value is ellipsis(...), and it works recursively
    """
    if isinstance(kwargs, List):
        for i in range(len(kwargs)):
            filter = kwargs.pop(0)
            filter = clear_from_ellipsis(filter)
            kwargs.append(filter)
            return kwargs

    kwargs_without_ellipsis = {}
    for key, value in kwargs.items():
        if value is ...:
            continue

        kwargs_without_ellipsis[key] = value

        if type(value) is dict:
            kwargs_without_ellipsis[key] = clear_from_ellipsis(value)

    return kwargs_without_ellipsis
