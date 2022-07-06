"""
Simple recursive deserializer from Dict[str, Any] to a given type.
Supports nested dictionaries and lists.
"""

from typing import Any, Dict, Type

class Deserializer:
    @staticmethod
    def from_dict(data: Dict[str, Any], t: Type) -> Any:
        """
        recursive function to convert dictionary to an object of type T.
        recursion entry:
        1) if attribute is an object
        2) if attribute is a list (for each item of the list)
        """
        if data is None or len(data) == 0:
            return None

        i = t()
        for attr, val in data.items():
            if isinstance(val, list):
                Deserializer._handle_list(i, attr, val)
            else:
                Deserializer._handle_field(i, attr, val)
        return i

    @staticmethod
    def _handle_list(i: Any, attr: str, val: Any) -> None:
        # determine type of the typed list:
        inner_t = type(getattr(i, attr)).__args__[0]
        # build items in the list
        v_list = [Deserializer.from_dict(x, inner_t) if isinstance(x, dict) else x for x in val]
        setattr(i, attr, v_list)

    @staticmethod
    def _handle_field(i: Any, attr: str, val: Any) -> None:
        # 1. if dict - enter recursion to build the object
        # 2. if plain - set attribute value
        if isinstance(val, dict):
            inner_t = type(getattr(i, attr))
            setattr(i, attr, Deserializer.from_dict(val, inner_t))
        else:
            setattr(i, attr, val)