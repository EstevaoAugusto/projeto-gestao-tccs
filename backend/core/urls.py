from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UnidadeAcademicaViewSet, DepartamentoViewSet, CursoViewSet, 
    AlunoViewSet, ProfessorViewSet, TCCViewSet, health_check
)

router = DefaultRouter()
router.register(r'unidades-academicas', UnidadeAcademicaViewSet)
router.register(r'departamentos', DepartamentoViewSet)
router.register(r'cursos', CursoViewSet)
router.register(r'alunos', AlunoViewSet)
router.register(r'professores', ProfessorViewSet)
router.register(r'tccs', TCCViewSet)

urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('', include(router.urls)),
]
