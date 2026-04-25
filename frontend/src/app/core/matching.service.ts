import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_BASE_URL } from './api.config';
import { CandidateMatchView, JobMatchView, MatchResult } from './models';

@Injectable({ providedIn: 'root' })
export class MatchingService {
  private readonly apiBase = `${API_BASE_URL}/matches`;

  constructor(private http: HttpClient) {}

  run(candidateId?: number | null, jobId?: number | null): Observable<MatchResult[]> {
    let params = new HttpParams();
    if (candidateId) {
      params = params.set('candidate_id', candidateId);
    }
    if (jobId) {
      params = params.set('job_id', jobId);
    }
    return this.http.post<MatchResult[]>(`${this.apiBase}/run`, {}, { params });
  }

  byCandidate(candidateId: number): Observable<CandidateMatchView[]> {
    return this.http.get<CandidateMatchView[]>(`${this.apiBase}/candidate/${candidateId}`);
  }

  byJob(jobId: number): Observable<JobMatchView[]> {
    return this.http.get<JobMatchView[]>(`${this.apiBase}/job/${jobId}`);
  }
}
