import os
import warnings


warnings.filterwarnings("ignore")
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"


from python.wakeword import wake_word
from python.fala import ola_inicial
from python.nlp_core import escutar_e_entender


WW = "sistema"                  # Palavra de ativação do sistema
feedback_WW = "Pois não?"       # Resposta de ativação do sistema


VERMELHO = '\033[91m'
VERDE = '\033[92m'
AMARELO = '\033[93m'
AZUL = '\033[94m'
RESET = '\033[0m'


def inicializar_modelo():
    from transformers.utils import logging as hf_logging
    import huggingface_hub.utils as hub_utils

    hf_logging.set_verbosity_error()
    # hf_logging.disable_progress_bar()       
    hub_utils.logging.set_verbosity_error()

    from transformers import pipeline

    return pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")


if __name__ == "__main__":
    os.system("clear")
    print(f"{AMARELO}[SISTEMA]{RESET} Carregando modelo NLP...")
    modelo_nlp = inicializar_modelo()

    print(f"{AMARELO}[SISTEMA]{RESET} Carregando motor de despertar...")
    while True:
        if(wake_word(WW)):
            ola_inicial(feedback_WW)

            escutar_e_entender(modelo_nlp)

            break