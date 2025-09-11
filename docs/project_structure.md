rag-mcp-assistant/
├── README.md
├── requirements.txt
├── setup.py
├── .env.example
├── .gitignore
├── LICENSE
├── CONTRIBUTING.md
├── docs/
│   ├── SYSTEM_DESIGN.md
│   ├── API_REFERENCE.md
│   ├── DEPLOYMENT.md
│   └── architecture_diagram.png
├── src/
│   ├── `__init__`.py
│   ├── agent/
│   │   ├── `__init__`.py
│   │   ├── rag_agent.py
│   │   ├── mcp_client.py
│   │   └── orchestrator.py
│   ├── mcp_server/
│   │   ├── `__init__`.py
│   │   ├── server.py
│   │   ├── search_tools.py
│   │   └── config.py
│   ├── utils/
│   │   ├── `__init__`.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   └── logger.py
│   └── api/
│       ├── `__init__`.py
│       └── server.py
├── tests/
│   ├── `__init__`.py
│   ├── test_rag_agent.py
│   ├── test_mcp_server.py
│   └── test_orchestrator.py
├── examples/
│   ├── basic_usage.py
│   ├── advanced_usage.py
│   └── cli_demo.py
├── data/
│   ├── sample_documents/
│   │   └── sample.txt
│   └── vector_db/
└── docker/
    ├── Dockerfile
    ├── docker-compose.yml
    └── requirements-docker.txt