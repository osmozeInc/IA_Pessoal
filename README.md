1. Lógica e Inteligência Artificial (Python)

    Configurar o ambiente virtual e instalar dependências.

    Implementar o modelo zero-shot do Hugging Face recebendo uma string de teste para extrair a intenção (ligar/desligar) e o alvo (ar-condicionado/luz).

    Estruturar a saída da IA em um formato padronizado e rigoroso para evitar falhas de tipagem, como um dicionário ou JSON.

2. Síntese de Voz (TTS)

    Instalar o Coqui TTS no ambiente Python.

    Gerar áudios de confirmação de testes (ex: "Ar-condicionado ligado") para validar a naturalidade da voz e o tempo de processamento isoladamente.

3. Comunicação de Rede (MQTT)

    Levantar um broker MQTT local (como o Eclipse Mosquitto) no seu computador.

    Adicionar uma biblioteca cliente (como paho-mqtt) ao script Python para publicar as ações em tópicos específicos (ex: quarto/ar/set).

4. Hardware e Atuadores (ESP32 em C)

    Programar a conexão Wi-Fi da placa.

    Implementar um cliente MQTT em C para se inscrever nos tópicos do broker.

    Mapear o payload recebido para o controle de hardware (portas GPIO, emissores infravermelhos ou relés).

5. Captação de Áudio e Integração

    Adicionar um módulo de Speech-to-Text (STT) para captar a fala real pelo microfone e converter na string inicial.

    Unificar o loop: Áudio -> STT -> Hugging Face -> Publicação MQTT -> Ação na ESP32 -> Resposta em voz pelo Coqui TTS.