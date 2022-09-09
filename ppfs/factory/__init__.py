from ..utils.lazy_object import LazyObject
from .files import Files
from .users import Users

get_user_factory = LazyObject(Users)
get_file_factory = LazyObject(Files)
