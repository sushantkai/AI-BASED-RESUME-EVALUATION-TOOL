export interface Candidate {
  id: number;
  name: string;
  email: string;
  phone?: string | null;
  skills: string[];
  experience_years: number;
  education?: string | null;
  summary?: string | null;
  created_at: string;
}

export interface CandidateDetail extends Candidate {
  resumes: { id: number; file_path: string; uploaded_at: string }[];
}

export interface Job {
  id: number;
  title: string;
  department: string;
  skills: string[];
  experience_required: number;
  description: string;
  improved_description?: string | null;
  created_at: string;
  updated_at: string;
}

export interface MatchResult {
  id: number;
  candidate_id: number;
  job_id: number;
  skill_match_pct: number;
  experience_match_pct: number;
  overall_score: number;
  explanation?: string | null;
  created_at: string;
}

export interface CandidateMatchView {
  candidate_id: number;
  candidate_name: string;
  job_id: number;
  job_title: string;
  skill_match_pct: number;
  experience_match_pct: number;
  overall_score: number;
  explanation?: string | null;
}

export interface JobMatchView {
  job_id: number;
  job_title: string;
  candidate_id: number;
  candidate_name: string;
  overall_score: number;
  skill_match_pct: number;
  experience_match_pct: number;
  explanation?: string | null;
}

export interface DashboardData {
  total_candidates: number;
  total_jobs: number;
  recent_candidates: { id: number; name: string; created_at: string }[];
  recent_jobs: { id: number; title: string; created_at: string }[];
}

