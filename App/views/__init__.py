from .user import user_views
from .index import index_views
from .auth import auth_views
from .admin import setup_admin
from .employer import employer_views
from .position import position_views
from .shortlist import shortlist_views
from .staff import staff_views
from .student import student_view

views = [
    user_views, index_views, auth_views,
    employer_views, position_views, shortlist_views,
    staff_views, student_view
]
