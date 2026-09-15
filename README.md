# Company Document RAG Practice

A FastAPI-based backend for a Retrieval-Augmented Generation (RAG) agent with the ability to ingest various types of unstructured documents and answer user questions accordingly. The system includes guardrails to ensure high-quality responses from the AI agent.

## Overview

This project demonstrates a production-ready RAG system that combines document retrieval with generative AI capabilities. It allows users to upload different document types, create a searchable knowledge base, and query it using natural language questions. The system includes safety guardrails to ensure reliable and accurate responses.

## Features

- 📄 **Multi-format Document Ingestion**: Support for various unstructured document types (PDFs, text files, etc.)
- 🔍 **Semantic Search**: Vector-based document retrieval for accurate context matching
- 🤖 **RAG Agent**: Intelligent agent that combines retrieval and generation for question answering
- 🛡️ **Guardrails**: Safety mechanisms to ensure response quality and reliability
- ⚡ **FastAPI Backend**: Async, high-performance REST API
- 📝 **Structured Data Models**: Well-defined schemas for requests and responses
- 🗄️ **Persistent Storage**: Database integration for storing documents and conversation history

## Tech Stack

- **Framework**: [FastAPI]
- **Language**: Python 3
- **Database**: Configured in `db/` module
- **API Documentation**: Auto-generated OpenAPI/Swagger UI
- **Project Management**: UV (ultra-fast Python package installer)

## Project Structure

```
company_doc_rag_practice/
├── db/                    # Database models and connections
├── routes/                # API route handlers
├── schema/                # Pydantic data models
├── services/              # Business logic and RAG implementation
├── templates/             # HTML templates (if UI included)
├── main.py                # Application entry point
├── pyproject.toml         # Project configuration and dependencies
├── uv.lock                # Dependency lock file
├── .python-version        # Python version specification
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

### Directory Details

- **db/** - Database setup, models, and ORM configuration
- **routes/** - FastAPI route definitions and endpoint handlers
- **schema/** - Pydantic models for request/response validation
- **services/** - Core business logic including RAG pipeline, document processing, and agent orchestration
- **templates/** - HTML templates for web interface (if applicable)



**Happy coding!** 🚀