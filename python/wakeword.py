import json
import pyaudio
import ctypes
from vosk import KaldiRecognizer, SetLogLevel


def wake_word(WW, modelo_stt):
    reconhecedor = KaldiRecognizer(modelo_stt, 16000, f'["{WW}", "[unk]"]')
    
    audio = pyaudio.PyAudio()
    
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
    stream.start_stream()
    
    print(f"\n{AZUL}[KWS]{RESET} Sistema dormente. Diga '{WW}' para acordar...")
    
    try:
        while True:
            dados = stream.read(2048, exception_on_overflow=False)
            
            if reconhecedor.AcceptWaveform(dados):
                resultado = json.loads(reconhecedor.Result())
                texto_captado = resultado.get("text", "")
                
                if WW in texto_captado:
                    print(f"{AZUL}[KWS]{RESET} '{WW}' detectado!")
                    stream.stop_stream()
                    stream.close()
                    audio.terminate()
                    
                    return True
                    
    except KeyboardInterrupt:
        print(f"\n{AMARELO}[SISTEMA]{RESET} Encerrando escuta.")
        stream.stop_stream()
        stream.close()
        audio.terminate()
        return True



AMARELO = '\033[93m'
AZUL = '\033[94m'
RESET = '\033[0m'



SetLogLevel(-1)

try:
    ERROR_HANDLER_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p)
    def py_error_handler(filename, line, function, err, fmt):
        pass
    c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
    asound = ctypes.cdll.LoadLibrary('libasound.so.2')
    asound.snd_lib_error_set_handler(c_error_handler)
except OSError:
    pass
