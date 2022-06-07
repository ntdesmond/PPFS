from .users import Users
from .files import Files
from ..utils.lazy_object import LazyObject

get_user_factory = LazyObject(Users)
get_file_factory = LazyObject(Files)

