from django.urls import path
from .views import user_profile, read_content, send_content, update_content, delete_content, special_page, success_page, \
    your_view_function, index, note_detail,delete

urlpatterns = [
    # path('', special_page),
    # path('', your_view_function, name="notes"),
    path('', index, name='notes'),
    path('profile/', user_profile),
    path('send/', send_content),
    path('update/', update_content),
    path('delete/', delete_content),
    path('success_page/', success_page),
    path('note/<int:note_id>/', note_detail, name='note_detail'),
    path('note/<int:note_id>/delete/', delete, name='delete'),
]
