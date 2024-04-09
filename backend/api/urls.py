from django.urls import path
from api.views import CreateProjectView, CreateSkillView, CreateUserView, ResetPasswordView, DeleteSkillView, SendCollaborationRequestView, ViewOpenProjectsView, UpdateProjectView, UserStatisticsView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('user/register/', CreateUserView.as_view(), name="register"),
    path('user/reset-password/<int:pk>', ResetPasswordView.as_view(), name="reset-password"),
    path('token/', TokenObtainPairView.as_view(), name="get_token"),
    path('token/refresh', TokenRefreshView.as_view(), name="refresh"),
    path('skills/', CreateSkillView.as_view(), name="skills"),
    path('skills/<int:pk>', DeleteSkillView.as_view(), name="delete-skill"),
    path('projects/', CreateProjectView.as_view(), name='projects'),
    path('projects/<int:pk>', UpdateProjectView.as_view(), name='update-project'),
    path('projects/open', ViewOpenProjectsView.as_view(), name='open_projects'),
    path('requests/', SendCollaborationRequestView.as_view(), name='collaboration_requests'),
    path('statistics/', UserStatisticsView.as_view(), name='statistics')
]
