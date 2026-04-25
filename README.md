# AI-Based Resume & Candidate Evaluation Tool

Full-stack application using:
- Frontend: Angular 18 (standalone components)
- Backend: FastAPI (Python)
- Database: PostgreSQL
- Architecture: MVC (`controllers -> services -> repositories`)

## Project Structure

```text
AI-Based -Resume/
  backend/
    app/
      controllers/
      services/
      repositories/
      models/
      schemas/
      core/
    uploads/
    schema.sql
    requirements.txt
    .env.example
  frontend/
    src/app/
      core/
      pages/
```

## 1. Backend Setup (FastAPI)

```bash
cd backend
uv venv -p 3.13 .venv
.venv\Scripts\activate
uv pip install -r requirements.txt
copy .env.example .env
```

Create PostgreSQL DB:
- DB name in default config: `ai_resume`
- Update `DATABASE_URL` in `.env` if needed.

Run API:

```bash
uvicorn main:app --reload --port 8001
```

API docs:
- [http://localhost:8001/docs](http://localhost:8001/docs)

Default users (seeded on startup):
- `admin / admin123` (Admin)
- `hr / hr123` (HR)

## 2. Frontend Setup (Angular 18)

```bash
cd frontend
npm install
npm start
```

App URL:
- [http://localhost:4200](http://localhost:4200)

## 3. Database Schema

SQL schema file:
- `backend/schema.sql`

Tables:
- `users`
- `candidates`
- `resumes`
- `jobs`
- `matches`
- `ai_data`

## 4. API Endpoints

### Auth
- `POST /api/auth/login`

### Candidates
- `POST /api/candidates`
- `GET /api/candidates?skills=python,angular&min_experience=2`
- `GET /api/candidates/{candidate_id}`
- `POST /api/candidates/{candidate_id}/resume` (multipart file upload)

### Jobs
- `POST /api/jobs`
- `GET /api/jobs`
- `PUT /api/jobs/{job_id}`
- `DELETE /api/jobs/{job_id}` (Admin only)

### Matching
- `POST /api/matches/run`
- `GET /api/matches/candidate/{candidate_id}`
- `GET /api/matches/job/{job_id}`

### Dashboard
- `GET /api/dashboard`

## 5. Implemented Feature Notes

- JWT login/logout with role-based checks.
- Angular route protection with auth guard + role guard.
- Candidate CRUD-lite flow (create/list/detail) + resume upload.
- Resume raw text extraction (mock decode) + AI mock parsing (skills/experience/education).
- Candidate summary generation (AI mock).
- Job CRUD + AI-improved description.
- Matching engine:
  - Skill Match % = `(matching skills / required skills) * 100`
  - Experience Match % capped at 100
  - Overall Score = `0.7 * skill + 0.3 * experience`
- Match explanation generation (AI mock).
- Dashboard totals + recent records.
