import speech_recognition as sr

def escutar_e_entender(classificador):
    reconhecedor = sr.Recognizer()
    
    with sr.Microphone() as fonte:
        print("\n[SISTEMA] Calibrando ruído... Fique em silêncio por 1 segundo.")
        reconhecedor.adjust_for_ambient_noise(fonte, duration=1)
        print("[SISTEMA] Pode falar o seu comando!")
        
        try:
            # Escuta até você parar de falar
            audio = reconhecedor.listen(fonte, timeout=5, phrase_time_limit=10)
            print("[SISTEMA] Processando áudio...")
            
            # Converte voz para texto
            texto_captado = reconhecedor.recognize_google(audio, language="pt-BR")
            print(f"\n[STT] Você disse: '{texto_captado}'")
            
            # Interpreta a intenção
            rotulos = ["ligar ar-condicionado", "desligar ar-condicionado", "ligar luz", "desligar luz", "pesquisar computador", "conversa casual ou palavra aleatória"]
            resultado = classificador(texto_captado, rotulos, multi_label=False, hypothesis_template="O usuário quer {}.")
            print(f"[NLP] Resultado da classificação: {resultado}")
            acao = resultado['labels'][0]
            confianca = resultado['scores'][0]
            
            if acao == "nenhuma ação" or confianca < 0.80:
                print("[SISTEMA] Nenhuma ação válida detectada ou confiança baixa.")
            else:
                print(f"[NLP] Ação identificada: -> {acao} <- (Confiança: {confianca:.2f})")
                
        except sr.WaitTimeoutError:
            print("[SISTEMA] Tempo esgotado. Ninguém falou.")
        except sr.UnknownValueError:
            print("[SISTEMA] Não consegui entender o que foi dito.")
