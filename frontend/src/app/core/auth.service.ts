import { Injectable, computed, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, tap } from 'rxjs';

import { API_BASE_URL } from './api.config';

interface LoginRequest {
  username: string;
  password: string;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
  role: 'Admin' | 'HR';
  username: string;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly apiBase = API_BASE_URL;
  private readonly tokenKey = 'ai_resume_token';
  private readonly roleKey = 'ai_resume_role';
  private readonly userKey = 'ai_resume_user';

  private tokenSignal = signal<string | null>(localStorage.getItem(this.tokenKey));
  private roleSignal = signal<string | null>(localStorage.getItem(this.roleKey));
  private userSignal = signal<string | null>(localStorage.getItem(this.userKey));

  readonly isLoggedIn = computed(() => !!this.tokenSignal());
  readonly role = computed(() => this.roleSignal());
  readonly username = computed(() => this.userSignal());

  constructor(private http: HttpClient, private router: Router) {}

  login(payload: LoginRequest): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.apiBase}/auth/login`, payload).pipe(
      tap((res) => {
        localStorage.setItem(this.tokenKey, res.access_token);
        localStorage.setItem(this.roleKey, res.role);
        localStorage.setItem(this.userKey, res.username);
        this.tokenSignal.set(res.access_token);
        this.roleSignal.set(res.role);
        this.userSignal.set(res.username);
      }),
    );
  }

  logout(): void {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.roleKey);
    localStorage.removeItem(this.userKey);
    this.tokenSignal.set(null);
    this.roleSignal.set(null);
    this.userSignal.set(null);
    this.router.navigate(['/login']);
  }

  getToken(): string | null {
    return this.tokenSignal();
  }
}
