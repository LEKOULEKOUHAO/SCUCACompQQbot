from typing import TypeVar, Dict, Union

personalRecordsValueType = dict[
    str, dict[str, dict[str, str]]
]
userDetailValueType = Union[
    str, int, dict[str, personalRecordsValueType]
]
userDetailType = dict[
    str, userDetailValueType
]