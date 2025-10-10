import os
import streamlit as st
from dotenv import load_dotenv
from datetime import date

load_dotenv()

def get_admin_password():
    if "admin" in st.secrets:
        return st.secrets["admin"]["password"]
    return os.getenv("ADMIN_PASSWORD", "default124")


PESOS = {
    "p3": {"Excelente": 4, "Bom": 3, "Regular": 2, "Ruim": 1},   
    "p4": {"Excelente": 4, "Bom": 3, "Regular": 2, "Ruim": 1},
    "p5": {"Sim": 4, "Às vezes": 2, "Não": 1, "Nunca": 0},
    "p6": {"Sim": 4, "Às vezes": 2, "Não": 1, "Nunca": 0},
    "p7": {"Sim": 4, "Mais ou menos": 2, "Não": 1, "Nunca": 0},
    "p8": {"Sim": 4, "Mais ou menos": 2, "Não": 1, "Nunca": 0},
    "p9": {"Excelente": 4, "Boa": 3, "Regular": 2, "Ruim": 1},
    "p10": {"Sim": 4, "Mais ou menos": 2, "Não": 1, "Nunca": 0},
    "p11": {"Excelente": 4, "Boa": 3, "Regular": 2, "Ruim": 1}
}


SETORES = {
    "DIRETORIA": ["Francisco Arruda", "Ana Teresa", "July Arruda", "Francisco Filho"],
    "GERÊNCIA": ["Nilton Linhares", "Emiliano", "Otaciano"],
    "FINANCEIRO": ["André", "Alexandre", "Wellington", "David", "Paulo"],
    "RH": ["Carlos", "Eduardo"],
    "LOGÍSTICA": ["Aderson", "Antonio Carlos", "Antonio Carlos Felipe", "Gleiton", "Antonio Jorge", "Ariel",
        "Carlos André", "Carlos Eduardo", "Cesanildo", "Cicero Tome", "Denilson", "Edilando", "Cristian",
        "Eduardo Evanildo", "Emanuel", "Amaral", "Edmilson", "Inaldo", "Jackson", "Rosivaldo", "Gleilson",
        "Israel", "Jeová", "Joao Roberto", "Jose Antonio", "Artur", "Evandro", "Ribamar", "Willame",
        "Marcos Antonio", "Marcos Ianny", "Regis Almeida", "Alexandre", "Lusimar", "Bruno", "Carlos Cavalcante",
        "Carlos Alexandre", "Lucas Matias", "Cicero Leite", "Cosmo", "Eder", "Alfredo", "Aurivan",
        "Francisco Marcio", "João Silva", "Jose Eduardo", "Jose Joseni", "Leano", "Júlio Cesar", "Marcos Paulo",
        "Nilberto", "Raimundo Nonato", "Ricardo Cesar", "Rodrigo", "Bruno Silva", "Carlos Jose Carvalho",
        "Claudio Roberto", "Dayanne", "Ednardo", "Augustinho", "Cleudes", "Darcy", "Francisco das Chagas",
        "Francisco de Assis", "Flavio", "Francisco Jose", "Rafael Façanha", "Francisco Rafael", "Geffeson",
        "Idacelio", "Iramildo", "Jonas Soares", "Jose Ailton", "Aldair", "Jose Lopes", "Patrício", "Rafael Barbosa",
        "Marcio Moreira", "Rosa", "Raimundo Nonato Santos", "Roberto Firmino", "Samia", "Sergio", "Thiago",
        "Nilson", "Raimundo Alencar Goes", "Francisco Carlos", "Agnaldo", "David", "Ivanilson", "Assis Monteiro"
    ],
    "APOIO COMERCIAL": ["Carla", "Kaike", "Vitor", "Thales", "William"],
    "COZINHA": ["Camila", "Josimeire", "Limdberg", "Rafael", "Lusimar"],
    "OFICINA": ["Hezio", "Salustiano", "Juvenal", "Wellington Felinto", "Evaldo", "Diego", "Jorge Luiz", "Saylhon"],
    "TELEVENDAS": ["Elizangela", "Marli", "Socorro", "Rachel"],
    "COMERCIAL LIDERANÇA": ["Diego", "Marlon", "Genildo", "Arleilson", "Odizio", "Felipe", "Willam", "Fabio", "James",
                            "Edmundo", "Marcos Cesar", "Anderson", "Macedo"],
    "EMPOCOTAMENTO": ["Fabio Amaro", "Wagner", "Leonardo Mendes", "Carlos Alexandre Vital"],
    "MARKETING": ["João Carlos"],
    "MERCHANDISING": ["Wesley", "Andressa", "Emeson", "Magno", "Camila", "Vinicius", "Elane", "Ezequiel", "Felipe Melo",
                      "Bruno", "Douglas", "Ednardo", "Lucas", "Jessica", "Cristiano", "Jose Khaua", "Jose Mario",
                      "Joverlandia", "Nathalia", "Paulo Vitor", "Rafael Henrique", "Rayssa", "Rodrigo", "Rodrigo Silva",
                      "Vinicius Marreiro", "Micherlane"],
    "PORTARIA": ["Sr. Martins", "Fabio Fraga", "Claudeone"],
    "COBRANÇA": ["Luiz Edval Coelho"],
    "CONTABILIDADE": ["Aline"],
    "TI": ["Claudemir"]
}


AGENDA_SETORES = {
    ("2025-09-26", "2025-10-02"): ["DIRETORIA", "GERÊNCIA", "FINANCEIRO", "RH", "MARKETING"],
    ("2025-10-03", "2025-10-09"): ["APOIO COMERCIAL", "TELEVENDAS", "CONTABILIDADE", "COBRANÇA", "PORTARIA","TI"],
    ("2025-10-10", "2025-10-16"): ["COMERCIAL LIDERANÇA"],
    ("2025-10-18", "2025-10-24"): ["COZINHA", "EMPOCOTAMENTO", "OFICINA"],
    ("2025-10-25", "2025-10-31"): ["MERCHANDISING"],
    ("2025-11-01", "2025-11-07"): ["LOGÍSTICA"]
}


def setores_ativos_hoje():
    hoje = date.today()
    for (inicio, fim), setores in AGENDA_SETORES.items():
        if date.fromisoformat(inicio) <= hoje <= date.fromisoformat(fim):
            return setores
    return []


def agenda_atual():
    hoje = date.today()
    for (inicio, fim), setores in AGENDA_SETORES.items():
        data_inicio = date.fromisoformat(inicio)
        data_fim = date.fromisoformat(fim)
        if data_inicio <= hoje <= data_fim:
            return (data_inicio, data_fim, setores)
    return (None, None, [])
