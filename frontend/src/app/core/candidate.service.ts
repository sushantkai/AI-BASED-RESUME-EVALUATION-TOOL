import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_BASE_URL } from './api.config';
import { Candidate, CandidateDetail } from './models';

@Injectable({ providedIn: 'root' })
export class CandidateService {
  private readonly apiBase = `${API_BASE_URL}/candidates`;

  constructor(private http: HttpClient) {}

  create(payload: { name: string; email: string; phone?: string | null }): Observable<Candidate> {
    return this.http.post<Candidate>(this.apiBase, payload);
  }

  list(filters: { skills?: string; min_experience?: number | null }): Observable<Candidate[]> {
    let params = new HttpParams();
    if (filters.skills) {
      params = params.set('skills', filters.skills);
    }
    if (filters.min_experience !== null && filters.min_experience !== undefined) {
      params = params.set('min_experience', String(filters.min_experience));
    }
    return this.http.get<Candidate[]>(this.apiBase, { params });
  }

  detail(id: number): Observable<CandidateDetail> {
    return this.http.get<CandidateDetail>(`${this.apiBase}/${id}`);
  }

  uploadResume(candidateId: number, file: File): Observable<{ message: string }> {
    const formData = new FormData();
    formData.append('resume_file', file);
    return this.http.post<{ message: string }>(`${this.apiBase}/${candidateId}/resume`, formData);
  }
}
