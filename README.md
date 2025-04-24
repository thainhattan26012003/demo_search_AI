# Demo Search Application

This project is a FastAPI-based application that allows users to generate, upload, and search persona data using Qdrant as the vector database.

## Features

- **Generate Persona Data**: Create sample persona data with random attributes.
- **Upload Data**: Upload persona data in CSV format and store it in Qdrant.
- **Search Persona**: Search for similar personas based on input data.

---

## Getting Started

### Prerequisites

- Python 3.10+
- Docker and Docker Compose

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/demo_search.git
   cd demo_search

2. install and start uvicorn services
   ```bash
   docker compose up --build

3 How to use each endpoint
  ```bash
  1. /generate_data: input the number of samples you want to generate (fake data) and it will be automated save in generation_data folder
  2. /upload_data: choose the created .csv file in the generate data, it will be uploaded to vector database Qdrant (cloud and can be use with AWS later)
  3. /search: input the information you want to search, then retrieve 3 results with the highest score of relationship vector search
