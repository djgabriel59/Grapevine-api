from rest_framework import generics
from .serializers import CollaborationRequestSerializer, ProjectSerializer, ResetPasswordSerializer, SkillSerializer, UserSerializer, UserStatisticsSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CollaborationRequest, Project, Skill
from django.db.models import Count, F
from rest_framework.views import Response
# Create your views here.
class CreateUserView(generics.ListCreateAPIView):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class ResetPasswordView(generics.RetrieveUpdateAPIView):
    User = get_user_model()
    serializer_class = ResetPasswordSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    
class CreateSkillView(generics.ListCreateAPIView):
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Skill.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        skills = Skill.objects.filter(user=self.request.user)
        if (skills.count() < 3):
            if serializer.is_valid():
                serializer.save(user=self.request.user)
        else:
            print("Too many skills")


class DeleteSkillView(generics.DestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


class CreateProjectView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(owner=self.request.user)


class ViewOpenProjectsView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    projects_with_collaborator_count = Project.objects.annotate(collaborator_count=Count('collaborators'))
    projects_with_less_collaborators = projects_with_collaborator_count.filter(collaborator_count__lt=F('maximum_collaborators'))
    queryset = projects_with_less_collaborators


class SendCollaborationRequestView(generics.ListCreateAPIView):
    serializer_class = CollaborationRequestSerializer
    permission_classes = [IsAuthenticated]
        
    def get_queryset(self):
        projects = Project.objects.filter(owner=self.request.user)
        return CollaborationRequest.objects.filter(project__in=projects)


class UpdateProjectView(generics.RetrieveUpdateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()

    def perform_update(self, serializer):
        if self.request.user == self.get_object().owner:
            serializer.save()

class UserStatisticsView(generics.RetrieveAPIView):
    serializer_class = UserStatisticsSerializer
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        projects_created = Project.objects.filter(owner=user).count()
        projects_contributed = Project.objects.filter(collaborators=user).count()
        serializer = self.serializer_class(
            {
                'projects_created': projects_created,
                'projects_contributed': projects_contributed
            }
        )
        return Response(serializer.data)
