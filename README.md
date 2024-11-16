
# Genipapo Web

**Genipapo Web** is a lightweight web-based interface for the **Genipapo Parser**, enabling users to validate and process `.conllu` files directly in their browser. This repository simplifies the deployment of the Genipapo Parser's web version using Docker.

---

## Purpose

This project provides an accessible interface for the **Genipapo Parser**, allowing users to:

- **Validate and Parse** `.conllu` files directly in their web browser.
- **Easily Deploy** the parser via Docker, without requiring a complex local setup.

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

## Usage

1. **Upload `.conllu` Files**:
   - Navigate to the web interface.
   - Select a `.conllu` file to upload and process.
   - View validation results and download the parsed file.

2. **Explore Additional Pages**:
   - **About**: Learn more about the Genipapo Parser and its development.
   - **Contact Us**: Find details to get in touch or contribute.

---

## How It Works

The **Genipapo Web** project wraps the functionality of the **Genipapo Parser** into a Flask-based web interface. It uses Docker for a seamless deployment experience, allowing users to run the parser without installing Python or additional dependencies.

---

## Acknowledgments

- This work was carried out at the [Center for Artificial Intelligence of the University of São Paulo (C4AI)](http://c4ai.inova.usp.br/), supported by the São Paulo Research Foundation (FAPESP grant #2019/07665-4) and the IBM Corporation.
- The project was supported by the Ministry of Science, Technology and Innovation, with resources of Law N. 8.248, of October 23, 1991, within the scope of PPI-SOFTEX, coordinated by Softex and published as Residence in TIC 13, DOU 01245.010222/2022-44.
- **Genipapo** was developed using the [Stanza library](https://stanfordnlp.github.io/stanza/), courtesy of the Stanford NLP Group.

---

## References

For detailed information about the **Genipapo Parser**, visit the main repository:

[Genipapo Parser GitHub Repository](https://github.com/bryankhelven/genipapo)

---

## Contributing

We welcome contributions to improve this web interface. To contribute:

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Open a Pull Request.

---

## Contact

For inquiries, suggestions, or bug reports, reach out to:

- **Email**: [bryankhelven@ieee.org](mailto:bryankhelven@ieee.org)
- **Main Parser Repository**: [Genipapo Parser](https://github.com/bryankhelven/genipapo)
