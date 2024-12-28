# Genipapo Web

**Genipapo Web** is a lightweight web-based interface for the **Genipapo Parser**, enabling users to validate and process `.conllu` files directly in their browser. This repository simplifies the deployment of the Genipapo Parser's web version using Docker.

---

## Purpose

This project provides an accessible interface for the **Genipapo Parser**, allowing users to:

- **Validate and Parse** `.conllu` files directly in their web browser.
- **Easily Deploy** the parser via Docker, without requiring a complex local setup.
- **Build a local API version** of the parser, allowing local requisitions in a faster manner.

For details on the **Genipapo Parser** itself, visit the main repository:

[Genipapo Parser GitHub Repository](https://github.com/bryankhelven/genipapo)

---

## Features

1. **Web-Based Interface**:
   - Upload `.conllu` files for validation and parsing.
   - Download parsed files with updated dependency relations.
   - View warnings and errors for `.conllu` file validation.

2. **Dockerized Deployment**:
   - Simplified setup with a single Docker command.
   - No local installation of dependencies required.

3. **Reference to Genipapo Parser**:
   - Built on the Genipapo Parser, a multigenre dependency parser for Brazilian Portuguese.

---

## Prerequisites

- **Docker**: Ensure Docker is installed on your system. [Download Docker](https://www.docker.com/products/docker-desktop)
- **Python 3.7+** (only needed to prepare resources before building the Docker image)

---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/bryankhelven/genipapo_web.git
cd genipapo_web
```

### 2. Download Resources

Run the following script to download the necessary resources and models:

```bash
python download_resources.py
```

This will place the resources and model files in their respective folders:
- `stanza_resources/`
- `models/`

### 3. Build the Docker Image

Build the Docker image using the following command:

```bash
docker build -t genipapo-web .
```

### 4. Run the Docker Container

Run the container and expose the application on port `8000`:

```bash
docker run -it -p 8000:8000 genipapo-web
```

### 5. Access the Application

Open your browser and navigate to:

```text
http://localhost:8000/
```

---

## API Usage

### Endpoints

- **POST /api/process** - Process a `.conllu` file.
- **POST /api/process/json** - Process raw `.conllu` content in JSON format.

### 1. Process a File

Use the `/api/process` endpoint to upload a `.conllu` file.

#### Parameters:

- **response_format** (optional): Set to `json` to return processed content as JSON. Defaults to `file`.

#### Example: Returning a File

When `response_format` is set to `file`, the processed content is returned as a downloadable `.conllu` file.

```bash
curl -X POST -H "Content-Type: multipart/form-data" \
-F "file=@example.conllu" \
"https://genipapo-parser.azurewebsites.net/api/process?response_format=file" \
--output processed_example.conllu
```

#### Example: Returning JSON

When `response_format` is set to `json`, the processed content is returned in JSON format.

```bash
curl -X POST -H "Content-Type: multipart/form-data" \
-F "file=@example.conllu" \
"https://genipapo-parser.azurewebsites.net/api/process?response_format=json"
```

Example JSON Response:

```json
{
    "status": "success",
    "warnings": [],
    "processed_content": "# sent_id = FOLHA_DOC000123_SENT016\n# text = O Capit\u00e3o Am\u00e9rica tamb\u00e9m bajulou o tucano.\n1\tO\to\tDET\t_\tDefinite=Def|Gender=Masc|Number=Sing|PronType=Art\t2\tdet\t_\t_\n2\tCapit\u00e3o\tCapit\u00e3o\tPROPN\t_\t_\t5\tnsubj\t_\t_\n3\tAm\u00e9rica\tAm\u00e9rica\tPROPN\t_\t_\t2\tflat:name\t_\t_\n4\ttamb\u00e9m\ttamb\u00e9m\tADV\t_\t_\t5\tadvmod\t_\t_\n5\tbajulou\tbajular\tVERB\t_\tMood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin\t0\troot\t_\t_\n6\to\to\tDET\t_\tDefinite=Def|Gender=Masc|Number=Sing|PronType=Art\t7\tdet\t_\t_\n7\ttucano\ttucano\tNOUN\t_\tGender=Masc|Number=Sing\t5\tobj\t_\tSpaceAfter=No\n8\t.\t.\tPUNCT\t_\t_\t5\tpunct\t_\tSpaceAfter=No\n"
}
```

### 2. Process Raw Content

Use the `/api/process/json` endpoint to send raw CoNLL-U content as JSON.

#### Example:

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"content": "# sent_id = FOLHA_DOC000123_SENT016\n# text = O Capit\u00e3o Am\u00e9rica tamb\u00e9m bajulou o tucano.\n1\tO\to\tDET\t_\tDefinite=Def|Gender=Masc|Number=Sing|PronType=Art\t_\t_\t_\t_\n2\tCapit\u00e3o\tCapit\u00e3o\tPROPN\t_\t_\t_\t_\t_\t_\n3\tAm\u00e9rica\tAm\u00e9rica\tPROPN\t_\t_\t_\t_\t_\t_\n4\ttamb\u00e9m\ttamb\u00e9m\tADV\t_\t_\t_\t_\t_\t_\n5\tbajulou\tbajular\tVERB\t_\tMood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin\t_\t_\t_\t_\n6\to\to\tDET\t_\tDefinite=Def|Gender=Masc|Number=Sing|PronType=Art\t_\t_\t_\t_\n7\ttucano\ttucano\tNOUN\t_\tGender=Masc|Number=Sing\t_\t_\t_\tSpaceAfter=No\n8\t.\t.\tPUNCT\t_\t_\t_\t_\t_\tSpaceAfter=No"}' \
"https://genipapo-parser.azurewebsites.net/api/process/json"
```

Example JSON Response:

```json
{
    "status": "success",
    "warnings": [],
    "processed_content": "# sent_id = FOLHA_DOC000123_SENT016\n# text = O Capit\u00e3o Am\u00e9rica tamb\u00e9m bajulou o tucano.\n1\tO\to\tDET\t_\tDefinite=Def|Gender=Masc|Number=Sing|PronType=Art\t2\tdet\t_\t_\n2\tCapit\u00e3o\tCapit\u00e3o\tPROPN\t_\t_\t5\tnsubj\t_\t_\n3\tAm\u00e9rica\tAm\u00e9rica\tPROPN\t_\t_\t2\tflat:name\t_\t_\n4\ttamb\u00e9m\ttamb\u00e9m\tADV\t_\t_\t5\tadvmod\t_\t_\n5\tbajulou\tbajular\tVERB\t_\tMood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin\t0\troot\t_\t_\n6\to\to\tDET\t_\tDefinite=Def|Gender=Masc|Number=Sing|PronType=Art\t7\tdet\t_\t_\n7\ttucano\ttucano\tNOUN\t_\tGender=Masc|Number=Sing\t5\tobj\t_\tSpaceAfter=No\n8\t.\t.\tPUNCT\t_\t_\t5\tpunct\t_\tSpaceAfter=No\n"
}
```

---

## Acknowledgments

- This work was carried out at the [Center for Artificial Intelligence of the University of São Paulo (C4AI)](http://c4ai.inova.usp.br/), supported by the São Paulo Research Foundation (FAPESP grant #2019/07665-4) and the IBM Corporation.
- The project was supported by the Ministry of Science, Technology and Innovation, with resources of Law N. 8.248, of October 23, 1991, within the scope of PPI-SOFTEX, coordinated by Softex and published as Residence in TIC 13, DOU 01245.010222/2022-44.
- **Genipapo** was developed using the [Stanza library](https://stanfordnlp.github.io/stanza/), courtesy of the Stanford NLP Group.

---

## Contact

For inquiries, suggestions, or bug reports, reach out to:

- **Email**: [bryankhelven@ieee.org](mailto:bryankhelven@ieee.org)
- **Main Parser Repository**: [Genipapo Parser](https://github.com/bryankhelven/genipapo)
