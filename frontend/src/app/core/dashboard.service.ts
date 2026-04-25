import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_BASE_URL } from './api.config';
import { DashboardData } from './models';

@Injectable({ providedIn: 'root' })
export class DashboardService {
  private readonly apiBase = `${API_BASE_URL}/dashboard`;

  constructor(private http: HttpClient) {}

  getData(): Observable<DashboardData> {
    return this.http.get<DashboardData>(this.apiBase);
  }
}
