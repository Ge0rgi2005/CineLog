from django.urls import path
from .views import (
    ReviewCreateView,
    ReviewUpdateView,
    ReviewDeleteView,
    ReviewCommentCreateView,
)

app_name = 'reviews'

urlpatterns = [
    path('movie/<int:movie_pk>/create/', ReviewCreateView.as_view(), name='review-create'),
    path('<int:pk>/edit/', ReviewUpdateView.as_view(), name='review-update'),
    path('<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
    path('<int:review_pk>/comment/', ReviewCommentCreateView.as_view(), name='comment-create'),
]