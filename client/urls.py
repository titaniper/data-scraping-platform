from django.urls import path, include

# NOTE: .로 찍어주는 것이 리팩토링 할때 편하다.
from . import views

# NOTE 패턴은 위에서부터 체크하기 때문에, 위부터 특별한 케이스를 넣어라.
urlpatterns = [
    # path('<int:pk>/', views.PostDetail.as_view()),
    # path('<category/<str:slug>/', views.categories_page),
    # path('<int:pk>/', views.views_single_page),
    # path('', views.index),
    path('', views.PipelineListView.as_view()),
]
