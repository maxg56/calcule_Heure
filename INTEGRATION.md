# Frontend-Backend Integration Guide

This document explains how the Next.js frontend and FastAPI backend are integrated in the Calcule Heure application.

## Architecture Overview

The application consists of three main components:

1. **Backend (FastAPI)** - RESTful API server (Port 8000)
2. **Frontend (Next.js)** - Modern React-based UI (Port 3000)
3. **Database (SQLite)** - Persistent data storage

## Quick Start

### Prerequisites

- Node.js 20+ and npm
- Python 3.11+
- Docker and Docker Compose (optional)

### Option 1: Development with Docker Compose (Recommended)

```bash
# Start both frontend and backend
docker-compose up

# Access the application:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Documentation: http://localhost:8000/docs
```

### Option 2: Manual Development Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.example .env.local

# Run the frontend
npm run dev
```

The frontend will be available at `http://localhost:3000`

## API Integration

### API Client Library

The frontend uses a centralized API client located at `frontend/src/lib/api.ts`. This client provides:

- Type-safe API calls using TypeScript
- Centralized error handling
- Automatic JSON serialization/deserialization
- Request/response interceptors

Example usage:

```typescript
import { api } from '@/lib/api';

// Get all schedules
const schedules = await api.getSchedules();

// Create a new schedule
const newSchedule = await api.createSchedule({
  heure_debut: '09:00',
  heure_debut_pause: '12:00',
  heure_fin_pause: '13:00',
});

// Get statistics
const stats = await api.getStatistics();
```

### Available Endpoints

#### Schedules API

- `GET /api/schedules/` - Get all schedules
- `GET /api/schedules/{id}` - Get schedule by ID
- `POST /api/schedules/` - Create new schedule
- `PUT /api/schedules/{id}` - Update schedule
- `DELETE /api/schedules/{id}` - Delete schedule

#### Statistics API

- `GET /api/statistics/` - Get summary statistics
- `GET /api/statistics/charts` - Get chart data

#### Config API

- `GET /api/config/` - Get current configuration
- `PUT /api/config/` - Update configuration
- `POST /api/config/reset` - Reset to defaults

## Data Flow

1. **User Action** → User interacts with the Next.js frontend
2. **API Call** → Frontend makes HTTP request via API client
3. **Backend Processing** → FastAPI receives request, validates data
4. **Database Operation** → SQLAlchemy ORM interacts with SQLite database
5. **Response** → Backend sends JSON response
6. **UI Update** → Frontend updates the UI with new data

## Environment Variables

### Backend (.env)

```env
DATABASE_URL=sqlite:///./data/horaires.db
DEBUG=false
CORS_ORIGINS=http://localhost:3000,http://localhost:8501
APP_NAME=Calcule Heure API
APP_VERSION=1.0.0
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:3000` (Next.js frontend)
- `http://localhost:8501` (Legacy Streamlit app)

CORS settings are configured in `backend/app/config.py`.

## Type Safety

The application uses TypeScript on the frontend and Pydantic on the backend to ensure type safety:

### Frontend Types (`frontend/src/types/index.ts`)

```typescript
export interface Schedule {
  id: string;
  date_saisie: string;
  heure_debut: string;
  heure_debut_pause: string;
  heure_fin_pause: string;
  heure_depart_calculee: string;
  duree_pause_minutes?: number;
}
```

### Backend Schemas (`backend/app/schemas/schedule.py`)

```python
class ScheduleResponse(BaseModel):
    id: int
    date_saisie: datetime
    heure_debut: time
    heure_debut_pause: time
    heure_fin_pause: time
    heure_depart_calculee: time
    duree_pause_minutes: int
```

## Database Schema

The SQLite database includes the following tables:

### Schedules Table

| Column                | Type     | Description                |
|-----------------------|----------|----------------------------|
| id                    | INTEGER  | Primary key                |
| date_saisie           | DATETIME | Entry date                 |
| heure_debut           | TIME     | Start time                 |
| heure_debut_pause     | TIME     | Break start time           |
| heure_fin_pause       | TIME     | Break end time             |
| heure_depart_calculee | TIME     | Calculated departure time  |
| created_at            | DATETIME | Creation timestamp         |
| updated_at            | DATETIME | Last update timestamp      |

### Config Table

| Column                 | Type     | Description                     |
|------------------------|----------|---------------------------------|
| id                     | INTEGER  | Primary key (always 1)          |
| duree_travail_heures   | INTEGER  | Work duration (hours)           |
| duree_travail_minutes  | INTEGER  | Work duration (minutes)         |
| seuil_pause_minutes    | INTEGER  | Minimum recommended break (min) |
| updated_at             | DATETIME | Last update timestamp           |

## Error Handling

### Frontend

The API client throws `ApiError` exceptions which include:
- HTTP status code
- Error message
- Additional error details

Example error handling:

```typescript
try {
  await api.createSchedule(data);
} catch (error) {
  if (error instanceof ApiError) {
    console.error(`API Error ${error.status}: ${error.message}`);
  }
}
```

### Backend

FastAPI automatically handles validation errors and returns appropriate HTTP status codes:
- `400 Bad Request` - Validation errors
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Invalid data format
- `500 Internal Server Error` - Server errors

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Production Deployment

### Building for Production

#### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend
npm run build
npm start
```

### Docker Production Deployment

```bash
# Build and run in production mode
docker-compose -f docker-compose.prod.yml up -d
```

## Troubleshooting

### Frontend can't connect to backend

1. Check that backend is running on port 8000
2. Verify `NEXT_PUBLIC_API_URL` in `.env.local`
3. Check CORS settings in `backend/app/config.py`

### Database errors

1. Ensure the `data` directory exists
2. Check file permissions for SQLite database
3. Run database initialization: `python -c "from backend.app.database import init_db; init_db()"`

### CORS errors

1. Verify frontend URL is in `CORS_ORIGINS` list
2. Check browser console for specific CORS error
3. Ensure backend is configured to allow credentials

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
