import asyncio
import edge_tts
import os

def falar_texto(texto):
    voz = "pt-BR-AntonioNeural"
    arquivo_mp3 = "resposta.mp3"

    print(f"\n[SISTEMA] Conectando à rede neural de voz ({voz})...")
    
    async def _gerar_audio():
        comunicador = edge_tts.Communicate(
        text=texto, 
        voice=voz, 
        rate="+15%", 
        pitch="-5Hz"
    )
        await comunicador.save(arquivo_mp3)

    asyncio.run(_gerar_audio())
    
    print(f"[TTS] Falando: '{texto}'")
    os.system(f"mpg123 -q {arquivo_mp3}")

def ola_inicial(ola):
    falar_texto(ola)