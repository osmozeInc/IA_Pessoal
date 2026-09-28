from transformers import pipeline
from TTS.api import TTS
import json
import os
from vosk import Model, KaldiRecognizer
import pyaudio

def executar_comando(acao, tts):
    # Formata a string que será falada pelo sistema
    mensagem = f"Comando validado. Executando: {acao.replace('-', ' ')}"
    print(f"\n[SISTEMA] {mensagem}")
    falar(tts, mensagem)
    # Futuramente, a chamada MQTT para a ESP32 entra aqui

def inicializar_modelo_nlp():
    print("Carregando modelo NLP...")
    return pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")

def inicializar_tts():
    print("Carregando modelo TTS (isso baixará os arquivos na primeira vez)...")
    # Modelo VITS focado na língua portuguesa
    return TTS(model_name="tts_models/pt/cv/vits", progress_bar=False, gpu=False)

def falar(tts, texto):
    caminho_audio = "resposta.wav"
    # Gera o arquivo de áudio
    tts.tts_to_file(text=texto, file_path=caminho_audio)
    # Executa o áudio no terminal de forma silenciosa
    os.system(f"aplay -q {caminho_audio}") 

def extrair_intencao(classificador, texto):
    rotulos = ["ligar ar-condicionado", "desligar ar-condicionado", "ligar luz", "desligar luz", "pesquisar computador", "nenhuma ação"]
    
    resultado = classificador(
        texto, 
        rotulos, 
        multi_label=True, 
        hypothesis_template="O usuário quer {}."
    )    
    saida = {
        "comando_bruto": texto,
        "acao_identificada": resultado['labels'][0],
        "grau_confianca": round(resultado['scores'][0], 4)
    }
    return saida

def ouvir_comando():
    # Carrega o modelo offline extraído na pasta local
    modelo_stt = Model("modelo_vosk")
    reconhecedor = KaldiRecognizer(modelo_stt, 16000)

    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    print("\n[SISTEMA] Microfone aberto. Fale um comando...")

    # Loop infinito que escuta até o Vosk detectar uma frase completa
    while True:
        dados = stream.read(4096, exception_on_overflow=False)
        if reconhecedor.AcceptWaveform(dados):
            resultado = json.loads(reconhecedor.Result())
            texto_captado = resultado.get("text", "")

            if texto_captado:
                print(f"\n[STT] Você disse: {texto_captado}")
                # Encerra o hardware de áudio para evitar vazamento de memória e travamento no ALSA
                stream.stop_stream()
                stream.close()
                audio.terminate()
                return texto_captado

if __name__ == "__main__":
    modelo_nlp = inicializar_modelo_nlp()
    modelo_tts = inicializar_tts()

    # A execução agora fica bloqueada aqui aguardando a sua voz
    comando_captado = ouvir_comando()

    dados_processados = extrair_intencao(modelo_nlp, comando_captado)

    if dados_processados["acao_identificada"] == "nenhuma ação":
        print("\n[SISTEMA] Apenas comentário detectado. Ignorando.")
    elif dados_processados["grau_confianca"] >= 0.60:
        executar_comando(dados_processados["acao_identificada"], modelo_tts)
    else:
         print("\n[SISTEMA] Confiança baixa. Nenhuma ação será executada.")

    print(json.dumps(dados_processados, indent=2, ensure_ascii=False))