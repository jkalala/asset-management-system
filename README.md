# Asset Management System

A full-stack application for managing assets, built with FastAPI and React.

## Features

- Asset tracking and management
- Asset status monitoring
- Search and filter capabilities
- QR code generation and scanning
- User authentication and authorization

## Tech Stack

### Backend
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Python 3.8+

### Frontend
- React
- TypeScript
- Material-UI
- Axios

## Setup Instructions

### Backend Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Set up the database:
```bash
# Create a PostgreSQL database named 'asset_management'
# Update the database URL in backend/app/core/config.py if needed
```

4. Run the backend server:
```bash
cd backend
uvicorn app.main:app --reload --port 8003
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8003
- API Documentation: http://localhost:8003/docs

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 