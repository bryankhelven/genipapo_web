import os
import requests
import hashlib
import sys

def download_genipapo_model():
    # Direct download URL from GitHub Releases
    model_url = 'https://github.com/bryankhelven/genipapo/releases/download/Publishing/genipapo.pt'
    model_dir = os.path.join('models')
    model_path = os.path.join(model_dir, 'genipapo.pt')

    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    if os.path.exists(model_path):
        print("Genipapo model already exists. Verifying checksum...")
        with open(model_path, 'rb') as f:
            data = f.read()
            checksum = hashlib.md5(data).hexdigest()
        if checksum == model_checksum:
            print("Checksum verified. Model is ready to use.")
            return
        else:
            print("Checksum mismatch. Redownloading the model...")
            os.remove(model_path)

    print("Downloading Genipapo model...")
    response = requests.get(model_url, stream=True)
    if response.status_code != 200:
        print("Failed to download the model. Please check the URL.")
        sys.exit(1)
    with open(model_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    print("Download completed. Model is ready to use.")


# Diretório onde os recursos serão salvos
RESOURCE_DIR = "stanza_resources"
LANGUAGE = "pt"

# Mapear os componentes necessários com os URLs corrigidos
REQUIRED_COMPONENTS = {
    "backward_charlm": "https://huggingface.co/stanfordnlp/stanza-pt/resolve/main/models/backward_charlm/oscar2023.pt",
    "forward_charlm": "https://huggingface.co/stanfordnlp/stanza-pt/resolve/main/models/forward_charlm/oscar2023.pt",
    "pretrain": "https://huggingface.co/stanfordnlp/stanza-pt/resolve/main/models/pretrain/conll17.pt",
}

# Função para baixar arquivos com progresso
def download_file(url, dest_path):
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(dest_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

# Função para baixar recursos específicos
def download_specific_resources():
    if not os.path.exists(RESOURCE_DIR):
        os.makedirs(RESOURCE_DIR)

    # Baixar o arquivo `resources.json`
    resources_url = "https://raw.githubusercontent.com/stanfordnlp/stanza-resources/main/resources_1.6.0.json"
    resources_path = os.path.join(RESOURCE_DIR, "resources.json")
    print("Baixando resources.json...")
    download_file(resources_url, resources_path)

    # Caminho base para os recursos do idioma
    lang_dir = os.path.join(RESOURCE_DIR, LANGUAGE)
    if not os.path.exists(lang_dir):
        os.makedirs(lang_dir)

    # Baixar os componentes necessários
    for component, url in REQUIRED_COMPONENTS.items():
        component_dir = os.path.join(lang_dir, component)
        os.makedirs(component_dir, exist_ok=True)
        component_path = os.path.join(component_dir, "model.pt")
        print(f"Baixando {component}...")
        download_file(url, component_path)
        print(f"{component} baixado para {component_path}")

    print("Download concluído. Recursos disponíveis em:", RESOURCE_DIR)



if __name__ == '__main__':
    download_genipapo_model()
    download_specific_resources()

