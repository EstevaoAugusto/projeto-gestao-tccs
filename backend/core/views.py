from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import connection
from django.db.models import Count
from .models import UnidadeAcademica, Departamento, Curso, Aluno, Professor, TCC
from .serializers import (
    UnidadeAcademicaSerializer, DepartamentoSerializer, CursoSerializer,
    AlunoSerializer, ProfessorSerializer, TCCSerializer
)


@api_view(['GET'])
def health_check(request):
    database_ok = False
    database_message = 'Banco de dados indisponivel.'

    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            cursor.fetchone()
        database_ok = True
        database_message = 'PostgreSQL conectado e respondendo.'
    except Exception as exc:
        database_message = f'Falha ao consultar o banco de dados: {exc}'

    http_status = status.HTTP_200_OK if database_ok else status.HTTP_503_SERVICE_UNAVAILABLE
    payload = {
        'status': 'healthy' if database_ok else 'unhealthy',
        'services': {
            'backend': {
                'status': 'healthy',
                'message': 'Django REST Framework respondendo.',
            },
            'database': {
                'status': 'healthy' if database_ok else 'unhealthy',
                'message': database_message,
            },
        },
    }

    print(
        f"[health] backend=healthy database={payload['services']['database']['status']}",
        flush=True,
    )
    return Response(payload, status=http_status)

class UnidadeAcademicaViewSet(viewsets.ModelViewSet):
    queryset = UnidadeAcademica.objects.all()
    serializer_class = UnidadeAcademicaSerializer

class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'matricula']

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']

class TCCViewSet(viewsets.ModelViewSet):
    queryset = TCC.objects.all()
    serializer_class = TCCSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['titulo', 'resumo']

    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        total_tccs = TCC.objects.count()
        
        # Agregações
        por_status = TCC.objects.values('status').annotate(total=Count('id'))
        por_tipo = TCC.objects.values('tipo').annotate(total=Count('id'))
        por_idioma = TCC.objects.values('idioma').annotate(total=Count('id'))
        por_semestre = TCC.objects.values('semestre_letivo_defesa').annotate(total=Count('id'))
        
        por_orientador = TCC.objects.values('orientador__nome').annotate(total=Count('id'))
        por_coorientador = TCC.objects.exclude(coorientador__isnull=True).values('coorientador__nome').annotate(total=Count('id'))
        por_curso = TCC.objects.values('aluno__curso__nome').annotate(total=Count('id'))
        por_departamento = TCC.objects.values('orientador__departamento__nome').annotate(total=Count('id'))
        por_unidade = TCC.objects.values('orientador__departamento__unidade_academica__nome').annotate(total=Count('id'))

        # Dicionários de mapeamento para os labels das escolhas (choices)
        status_map = dict(TCC.STATUS_CHOICES)
        tipo_map = dict(TCC.TIPO_CHOICES)
        idioma_map = dict(TCC.IDIOMA_CHOICES)

        return Response({
            'total_geral': total_tccs,
            'por_status': {status_map.get(item['status'], item['status']): item['total'] for item in por_status},
            'por_tipo': {tipo_map.get(item['tipo'], item['tipo']): item['total'] for item in por_tipo},
            'por_idioma': {idioma_map.get(item['idioma'], item['idioma']): item['total'] for item in por_idioma},
            'por_semestre': {item['semestre_letivo_defesa']: item['total'] for item in por_semestre if item['semestre_letivo_defesa']},
            'por_orientador': {item['orientador__nome']: item['total'] for item in por_orientador},
            'por_coorientador': {item['coorientador__nome']: item['total'] for item in por_coorientador},
            'por_curso': {item['aluno__curso__nome']: item['total'] for item in por_curso},
            'por_departamento': {item['orientador__departamento__nome']: item['total'] for item in por_departamento},
            'por_unidade_academica': {item['orientador__departamento__unidade_academica__nome']: item['total'] for item in por_unidade}
        })
