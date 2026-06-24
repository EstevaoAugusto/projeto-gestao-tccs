import argparse
import os
import random
from itertools import cycle

import django
from django.db import transaction

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tcc_project.settings")
django.setup()

from core.models import Aluno, Curso, Departamento, Professor, TCC, UnidadeAcademica


UNIDADES = [
    ("Escola de Ciencias Agrarias de Lavras", "ESAL"),
    ("Escola de Engenharia", "EENG"),
    ("Faculdade de Ciencias da Saude", "FCS"),
    ("Faculdade de Ciencias Sociais Aplicadas", "FCSA"),
    ("Faculdade de Filosofia, Ciencias Humanas, Educacao e Letras", "FAELCH"),
    ("Faculdade de Zootecnia e Medicina Veterinaria", "FZMV"),
    ("Instituto de Ciencia, Tecnologia e Inovacao", "ICTIN"),
    ("Instituto de Ciencias Exatas e Tecnologicas", "ICET"),
    ("Instituto de Ciencias Naturais", "ICN"),
]

DEPARTAMENTOS = [
    ("Computacao Aplicada", "DAC", "ICET"),
    ("Ciencia da Computacao", "DCC", "ICET"),
    ("Estatistica", "DES", "ICET"),
    ("Matematica e Matematica Aplicada", "DMM", "ICET"),
    ("Educacao em Ciencias Fisicas e Matematica", "DFM", "ICET"),
    ("Engenharia", "DEG", "EENG"),
    ("Ciencias Humanas", "DCH", "FAELCH"),
    ("Biologia", "DBI", "ICN"),
    ("Administracao e Economia", "DAE", "FCSA"),
    ("Medicina Veterinaria", "DMV", "FZMV"),
]

CURSOS = [
    ("Ciencia da Computacao", "BCC", "G010"),
    ("Sistemas de Informacao", "BSI", "G014"),
    ("Matematica", "MAT", "G015"),
    ("Fisica", "FIS", "G018"),
    ("Engenharia de Software", "ESW", "G021"),
    ("Administracao", "ADM", "G030"),
    ("Biologia", "BIO", "G040"),
]

PROFESSORES = [
    "Ana Paula Ribeiro",
    "Carlos Eduardo Mendes",
    "Fernanda Oliveira Souza",
    "Ricardo Alves Pereira",
    "Juliana Martins Costa",
    "Marcos Vinicius Teixeira",
    "Patricia Gomes Andrade",
    "Roberto Nogueira Silva",
    "Camila Fernandes Rocha",
    "Eduardo Henrique Batista",
    "Luciana Carvalho Dias",
    "Gustavo Ribeiro Matos",
    "Daniela Pires Lopes",
    "Felipe Augusto Santana",
    "Renata Farias Moraes",
    "Andre Luiz Cardoso",
    "Tatiane Rodrigues Barros",
    "Paulo Sergio Almeida",
    "Vanessa Monteiro Braga",
    "Leonardo Torres Nascimento",
    "Helena Duarte Fonseca",
    "Bruno Azevedo Campos",
    "Marina Lopes Figueiredo",
    "Rafael Moreira Tavares",
]

ALUNOS = [
    "Lucas Almeida Santos",
    "Maria Clara Ferreira",
    "Joao Pedro Costa",
    "Ana Beatriz Martins",
    "Pedro Henrique Oliveira",
    "Larissa Gomes Ribeiro",
    "Gabriel Alves Souza",
    "Isabela Carvalho Lima",
    "Matheus Pereira Rocha",
    "Julia Fernandes Barros",
    "Rafael Nogueira Mendes",
    "Bruna Teixeira Andrade",
    "Guilherme Batista Moraes",
    "Amanda Rodrigues Dias",
    "Daniel Martins Silva",
    "Carolina Farias Costa",
    "Thiago Monteiro Rocha",
    "Beatriz Cardoso Alves",
    "Leonardo Santana Ribeiro",
    "Camila Torres Oliveira",
    "Victor Matos Pereira",
    "Leticia Andrade Gomes",
    "Felipe Costa Barros",
    "Natalia Ferreira Santos",
    "Igor Mendes Carvalho",
    "Mariana Alves Dias",
    "Renan Oliveira Teixeira",
    "Paula Batista Rocha",
    "Gabriela Pires Costa",
    "Andre Fernandes Lima",
    "Joana Ribeiro Mendes",
    "Diego Cardoso Silva",
    "Luana Teixeira Santos",
    "Bruno Monteiro Dias",
    "Larissa Carvalho Rocha",
    "Mateus Farias Costa",
    "Vitoria Gomes Lima",
    "Gustavo Mendes Santos",
    "Bianca Rocha Pereira",
    "Arthur Santana Dias",
    "Eduarda Batista Lima",
    "Caio Fernandes Costa",
    "Alice Andrade Rocha",
    "Rodrigo Matos Silva",
    "Helena Carvalho Dias",
    "Ruan Monteiro Lima",
    "Sophia Teixeira Rocha",
    "Pedro Lucas Mendes",
    "Livia Santana Costa",
    "Rafaela Batista Lima",
]

TITULOS = [
    "Sistema Web para Gestao Academica",
    "Machine Learning na Previsao de Desempenho Escolar",
    "Sistema de Recomendacao de Livros com Inteligencia Artificial",
    "Analise de Dados Educacionais com Python",
    "Aplicacao Web com Django para Gestao Universitaria",
    "Automacao de Processos Administrativos com Python",
    "Sistema IoT para Monitoramento de Sensores",
    "Deep Learning para Reconhecimento de Imagens",
    "Chatbot Educacional com Processamento de Linguagem Natural",
    "Sistema de Gestao de Biblioteca Universitaria",
    "Analise de Sentimentos em Redes Sociais",
    "Aplicacao Web para Gerenciamento de Projetos",
    "Sistema de Recomendacao de Filmes",
    "Uso de Big Data na Educacao",
    "Plataforma Web para Ensino de Programacao",
    "API REST para Sistemas Educacionais",
    "Sistema Inteligente de Controle de Estoque",
    "Visualizacao Interativa de Dados com Dash",
    "Aplicacao de NLP em Analise de Textos",
    "Sistema de Agendamento Online",
    "Plataforma de Ensino Adaptativo",
    "Analise de Dados de Trafego Urbano",
    "Sistema de Reconhecimento Facial",
    "Redes Neurais para Diagnostico Medico",
    "Jogo Educacional para Ensino de Logica",
    "Sistema Web para Gestao de Eventos",
    "Analise de Dados Financeiros com Python",
    "Plataforma de Cursos Online",
    "Sistema de Recomendacao de Musicas",
    "Blockchain em Sistemas de Votacao",
    "Sistema de Monitoramento Ambiental",
    "Analise de Dados de Saude Publica",
    "Aplicacao Web para Controle de Tarefas",
    "Sistema de Gestao de Clinicas",
    "Inteligencia Artificial na Agricultura",
    "Plataforma de Compartilhamento de Conhecimento",
    "Sistema de Deteccao de Fraudes",
    "IoT para Casas Inteligentes",
    "Sistema de Gestao de Transporte",
    "Analise de Dados Climaticos",
    "Sistema de Gestao de Restaurantes",
    "Rede Social Academica",
    "Sistema Inteligente de Controle de Acesso",
    "Data Mining Aplicado a Educacao",
    "Plataforma de Monitoramento de Atividades Fisicas",
    "Sistema de Gestao de Projetos Academicos",
    "IA Aplicada ao Diagnostico por Imagem",
    "Sistema de Recomendacao de Cursos",
    "Plataforma de Avaliacao de Professores",
    "Sistema de Gestao de TCC",
]

PALAVRAS_CHAVE = [
    "inteligencia artificial, aprendizado de maquina, analise de dados",
    "sistemas web, django, desenvolvimento backend",
    "ciencia de dados, python, visualizacao",
    "mineracao de dados, educacao, analise",
    "engenharia de software, arquitetura, sistemas",
    "redes neurais, deep learning, imagens",
    "internet das coisas, sensores, monitoramento",
    "seguranca digital, criptografia, autenticacao",
    "processamento de linguagem natural, texto, classificacao",
    "big data, analise, armazenamento",
]


def reset_database():
    TCC.objects.all().delete()
    Aluno.objects.all().delete()
    Professor.objects.all().delete()
    Curso.objects.all().delete()
    Departamento.objects.all().delete()
    UnidadeAcademica.objects.all().delete()


def seed_unidades():
    unidades = {}
    for nome, sigla in UNIDADES:
        unidade, _ = UnidadeAcademica.objects.update_or_create(
            sigla=sigla,
            defaults={"nome": nome},
        )
        unidades[sigla] = unidade
    return unidades


def seed_departamentos(unidades):
    departamentos = {}
    for nome, sigla, unidade_sigla in DEPARTAMENTOS:
        departamento, _ = Departamento.objects.update_or_create(
            sigla=sigla,
            defaults={"nome": nome, "unidade_academica": unidades[unidade_sigla]},
        )
        departamentos[sigla] = departamento
    return departamentos


def seed_cursos():
    cursos = {}
    for nome, sigla, codigo in CURSOS:
        curso, _ = Curso.objects.update_or_create(
            codigo=codigo,
            defaults={"nome": nome, "sigla": sigla},
        )
        cursos[codigo] = curso
    return cursos


def seed_professores(departamentos):
    professores = []
    departamentos_cycle = cycle(departamentos.values())
    for nome in PROFESSORES:
        professor, _ = Professor.objects.update_or_create(
            nome=nome,
            defaults={"departamento": next(departamentos_cycle)},
        )
        professores.append(professor)
    return professores


def seed_alunos(cursos, total):
    alunos = []
    nomes = [ALUNOS[index % len(ALUNOS)] for index in range(total)]
    curso_cycle = cycle(cursos.values())
    for index, nome in enumerate(nomes, start=1):
        aluno, _ = Aluno.objects.update_or_create(
            matricula=f"2024{index:04d}",
            defaults={"nome": nome, "curso": next(curso_cycle)},
        )
        alunos.append(aluno)
    return alunos


def make_resumo(titulo, curso_nome):
    return (
        f"Este trabalho apresenta {titulo.lower()} no contexto do curso de "
        f"{curso_nome}. A proposta organiza informacoes academicas, apoia a "
        "tomada de decisao e demonstra o uso de tecnologias aplicadas a "
        "problemas reais."
    )


def escolher_banca(professores, orientador):
    disponiveis = [professor for professor in professores if professor != orientador]
    primeiro_membro, segundo_membro = random.sample(disponiveis, 2)
    return primeiro_membro, segundo_membro


def seed_tccs(alunos, professores):
    tipos = [choice[0] for choice in TCC.TIPO_CHOICES]
    idiomas = [choice[0] for choice in TCC.IDIOMA_CHOICES]
    status_opcoes = [choice[0] for choice in TCC.STATUS_CHOICES]
    semestres = [choice[0] for choice in TCC.SEMESTRE_CHOICES]

    for index, aluno in enumerate(alunos):
        titulo_base = TITULOS[index % len(TITULOS)]
        titulo = titulo_base if index < len(TITULOS) else f"{titulo_base} {index + 1}"
        orientador = professores[index % len(professores)]
        primeiro_membro, segundo_membro = escolher_banca(professores, orientador)
        coorientador = random.choice(
            [professor for professor in professores if professor not in {orientador, primeiro_membro}]
        )
        if index % 3 == 0:
            coorientador = None

        TCC.objects.update_or_create(
            aluno=aluno,
            defaults={
                "titulo": titulo,
                "resumo": make_resumo(titulo, aluno.curso.nome),
                "palavras_chave": PALAVRAS_CHAVE[index % len(PALAVRAS_CHAVE)],
                "tipo": tipos[index % len(tipos)],
                "idioma": idiomas[index % len(idiomas)],
                "orientador": orientador,
                "coorientador": coorientador,
                "presidente": orientador,
                "primeiro_membro": primeiro_membro,
                "segundo_membro": segundo_membro,
                "semestre_letivo_defesa": semestres[index % len(semestres)],
                "status": status_opcoes[index % len(status_opcoes)],
            },
        )


def print_summary():
    print("Seed concluido:")
    print(f"- Unidades academicas: {UnidadeAcademica.objects.count()}")
    print(f"- Departamentos: {Departamento.objects.count()}")
    print(f"- Cursos: {Curso.objects.count()}")
    print(f"- Professores: {Professor.objects.count()}")
    print(f"- Alunos: {Aluno.objects.count()}")
    print(f"- TCCs: {TCC.objects.count()}")


@transaction.atomic
def seed(total_tccs, reset=False, random_seed=42):
    random.seed(random_seed)
    if reset:
        reset_database()

    unidades = seed_unidades()
    departamentos = seed_departamentos(unidades)
    cursos = seed_cursos()
    professores = seed_professores(departamentos)
    alunos = seed_alunos(cursos, total_tccs)
    seed_tccs(alunos, professores)
    print_summary()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Popula o banco de dados com dados academicos de exemplo."
    )
    parser.add_argument(
        "--tccs",
        type=int,
        default=50,
        help="Quantidade de alunos e TCCs a criar ou atualizar. Padrao: 50.",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Remove os dados existentes dos modelos da app core antes de popular.",
    )
    parser.add_argument(
        "--random-seed",
        type=int,
        default=42,
        help="Semente para reproducibilidade dos professores e bancas. Padrao: 42.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    seed(total_tccs=args.tccs, reset=args.reset, random_seed=args.random_seed)
