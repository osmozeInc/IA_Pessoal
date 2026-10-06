import speech_recognition as sr

def escutar_e_entender(classificador):
    reconhecedor = sr.Recognizer()
    
    with sr.Microphone() as fonte:
        reconhecedor.adjust_for_ambient_noise(fonte, duration=.2)
        
        try:
            print(f"\n{VERDE}[STT]{RESET} Escutando...")
            audio = reconhecedor.listen(fonte, timeout=5, phrase_time_limit=10)
            
            texto_captado = reconhecedor.recognize_google(audio, language="pt-BR")
            print(f"{VERDE}[STT]{RESET} Você disse: '{texto_captado}'")
            
            rotulos = [
                "ligar ar-condicionado", 
                "desligar ar-condicionado", 
                "ligar luz", "desligar luz", 
                "pesquisar computador", 
                "conversa casual", 
                "palavra aleatória"
            ]

            resultado = classificador(
                texto_captado, 
                rotulos, 
                multi_label=False, 
                hypothesis_template="O usuário quer {}."
            )

            acao = resultado['labels'][0]
            confianca = resultado['scores'][0]
            
            if acao == "nenhuma ação" or confianca < 0.80:
                print(f"\n{AMARELO}[SISTEMA]{RESET} Nenhuma ação válida detectada ou confiança baixa.")
            else:
                print(f"\n{LARANJA}[NLP]{RESET} Ação identificada: -> {acao} <- (Confiança: {confianca:.2f})")
                
        except sr.WaitTimeoutError:
            print(f"\n{AMARELO}[SISTEMA]{RESET} Tempo esgotado. Ninguém falou.")
        except sr.UnknownValueError:
            print(f"\n{AMARELO}[SISTEMA]{RESET} Não consegui entender o que foi dito.")



VERDE = '\033[92m'
AMARELO = '\033[93m'
LARANJA = '\033[95m'
RESET = '\033[0m'
