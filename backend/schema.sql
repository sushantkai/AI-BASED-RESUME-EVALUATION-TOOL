CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS candidates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL,
    phone VARCHAR(50),
    skills_text TEXT,
    experience_years FLOAT NOT NULL DEFAULT 0,
    education TEXT,
    summary TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS resumes (
    id SERIAL PRIMARY KEY,
    candidate_id INT NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    file_path VARCHAR(500) NOT NULL,
    raw_text TEXT,
    uploaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    department VARCHAR(120) NOT NULL,
    skills_text TEXT NOT NULL,
    experience_required FLOAT NOT NULL DEFAULT 0,
    description TEXT NOT NULL,
    improved_description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS matches (
    id SERIAL PRIMARY KEY,
    candidate_id INT NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    job_id INT NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    skill_match_pct FLOAT NOT NULL,
    experience_match_pct FLOAT NOT NULL,
    overall_score FLOAT NOT NULL,
    explanation TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_candidate_job UNIQUE (candidate_id, job_id)
);

CREATE TABLE IF NOT EXISTS ai_data (
    id SERIAL PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL,
    entity_id INT NOT NULL,
    data_type VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

