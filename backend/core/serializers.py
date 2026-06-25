from rest_framework import serializers
from .models import UnidadeAcademica, Departamento, Curso, Aluno, Professor, TCC

class UnidadeAcademicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadeAcademica
        fields = '__all__'

class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = '__all__'

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'

class TCCSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    idioma_display = serializers.CharField(source='get_idioma_display', read_only=True)

    class Meta:
        model = TCC
        fields = '__all__'

    def validate_arquivo(self, arquivo):
        if not arquivo:
            return arquivo

        nome_arquivo = arquivo.name.lower()
        content_type = getattr(arquivo, 'content_type', None)

        if not nome_arquivo.endswith('.pdf') or (content_type and content_type != 'application/pdf'):
            raise serializers.ValidationError('O arquivo enviado deve ser um PDF.')

        return arquivo
