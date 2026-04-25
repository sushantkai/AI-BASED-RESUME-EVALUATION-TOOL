import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_BASE_URL } from './api.config';
import { Job } from './models';

@Injectable({ providedIn: 'root' })
export class JobService {
  private readonly apiBase = `${API_BASE_URL}/jobs`;

  constructor(private http: HttpClient) {}

  create(payload: Omit<Job, 'id' | 'created_at' | 'updated_at' | 'improved_description'>): Observable<Job> {
    return this.http.post<Job>(this.apiBase, payload);
  }

  list(): Observable<Job[]> {
    return this.http.get<Job[]>(this.apiBase);
  }

  update(id: number, payload: Omit<Job, 'id' | 'created_at' | 'updated_at' | 'improved_description'>): Observable<Job> {
    return this.http.put<Job>(`${this.apiBase}/${id}`, payload);
  }

  delete(id: number): Observable<{ message: string }> {
    return this.http.delete<{ message: string }>(`${this.apiBase}/${id}`);
  }
}
