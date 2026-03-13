import os
from dotenv import load_dotenv

load_dotenv()

PASTA_MAPA_DIGITAIS = os.getenv("PASTA_MAPA_DIGITAIS")
PASTA_INDICES = os.getenv("PASTA_INDICES")
DOCKER_HOST = os.getenv("DOCKER_HOST")
MCCSDK = os.getenv("MCCSDK")