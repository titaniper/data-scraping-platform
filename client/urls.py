from django.urls import path, include
from django.contrib.auth import views as auth_views

# NOTE: .로 찍어주는 것이 리팩토링 할때 편하다.
from . import views

app_name = 'client'

urlpatterns = [
    path('pipelines/<int:pk>/', views.PipelineDetail.as_view()),
    path('pipelines/category/<str:slug>/', views.show_category_pipelines),
    path('pipelines/tag/<str:slug>/',views.show_tag_pipelines),
    path('pipelines/create_pipeline/', views.PipelineCreate.as_view()),
    path('pipelines/<int:pk>/update_pipeline/', views.PipelineUpdate.as_view()),
    path('pipelines/<int:pk>/addcomment/', views.addComment),
    path('pipelines/', views.PipelineList.as_view()),

    path('pipelines/<int:pk>/add-stage/', views.addStage),

    path('stages/<int:pk>/add-request/', views.addRequest),
    path('stages/<int:pk>/', views.StageDetail.as_view()),

    path('requests/<int:pk>/action/', views.execRequest),
    path('requests/<int:pk>/', views.request_detail),

    path('request-histories/<int:pk>/', views.HistoryDetail.as_view()),
    path('request-histories/', views.HistoryList.as_view()),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.index),
]
# NOTE 패턴은 위에서부터 체크하기 때문에, 위부터 특별한 케이스를 넣어라.
