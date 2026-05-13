Final AI Development Project

Overview
This project is a comprehensive Full-Stack E-Commerce Application integrated with an AI
Shopping Assistant.
The system is designed with a Layered Architecture to ensure scalability and
maintainability. It includes:
● High-performance FastAPI backend
● User-friendly Streamlit frontend
● Persistent MySQL database
● Full Docker orchestration

A main standout feature is the AI Chatbot (OpenAI-powered), which is context-aware and
uses real-time access to the store’s inventory to help users find products based on
availability and price.

Key Features
E-Commerce Functionality
● User Management: Secure Registration & Login (JWT/Session-based)
● Product Catalog: Browse with advanced filters (price range, stock)
● Smart Search: Search by name or multiple keywords
● Shopping Cart: Add/remove items, manage quantities, checkout
● Order History: Review past orders
● Favorites: Save products for later

AI Shopping Assistant

● Context-Aware: Access to real-time inventory, prices, and stock levels
● Smart Recommendations
Example: “Do you have a laptop under $1000?”
● Rate Limiting: Controls AI usage per session for cost management

Technical Highlights
● Dockerized Environment: One-command deployment with Docker Compose
● Process Management: supervisord handles both API + Frontend
● Security:
○ SHA256 password hashing
○ Parameterized SQL queries
○ Environment variable management

Tech Stack
Backend
● Language: Python 3.9
● Framework: FastAPI (Async I/O, high performance)
● ORM: Databases (async)
● Validation: Pydantic

Frontend
● Framework: Streamlit
● Communication: REST API via requests

Database & Infrastructure
● Database: MySQL 8.0
● Containerization: Docker & Docker Compose
● Cache: Redis (ready for future integration)

Architecture
A strict Layered Architecture is used:
Controller Layer (/Controller)
Handles HTTP requests, validates input, manages API routes.
Service Layer (/Service)
Contains business logic (e.g., stock validation, user authentication).
Repository Layer (/Repository)
Direct communication with the database through SQL queries.
Models (/Models)
Pydantic schemas defining data structures.

Installation & Setup
Prerequisites
● Docker & Docker Compose
● Valid OpenAI API Key

2. Configure Environment Variables
Create a .env file in the root directory:
MYSQL_USER=root
MYSQL_PASSWORD=root_password
MYSQL_DATABASE=main
MYSQL_HOST=db
MYSQL_PORT=3306
OPENAI_API_KEY=sk-proj-your-openai-key-here

3. Build and Run (Docker)
Run:
docker-compose up --build

The database initializes automatically using init.sql on first run.

Usage
Once running:
● Frontend (Store UI): http://localhost:8501
● Backend API (Swagger UI): http://localhost:8000/docs

Test Credentials
You may register a new account via the UI, or inspect the database for existing ones.

Project Structure
├── Controller/ # API Endpoints (Routes)
├── Service/ # Business Logic
├── Repository/ # Database Interactions (SQL)
├── Models/ # Pydantic Data Schemas

├── Streamlit_Frontend.py # User Interface
├── database.py # Database Connection
├── docker-compose.yaml # Docker Orchestration
├── Dockerfile # Container Definition
├── init.sql # SQL Schema Initialization
├── main.py # FastAPI Entry Point
└── supervisord.conf # Process Manager Configuration

Author
Negusu Demsash
