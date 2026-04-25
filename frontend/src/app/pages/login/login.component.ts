import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import { AuthService } from '../../core/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="page">
      <h2>AI Resume Tool - Login</h2>
      <form (ngSubmit)="submit()" class="card">
        <label>Username</label>
        <input type="text" [(ngModel)]="username" name="username" required />
        <label>Password</label>
        <input type="password" [(ngModel)]="password" name="password" required />
        <button type="submit" [disabled]="!username || !password || loading">
          {{ loading ? 'Loading...' : 'Login' }}
        </button>
      </form>
      <p class="help">Demo users: admin/admin123 (Admin), hr/hr123 (HR)</p>
      <p class="error" *ngIf="error">{{ error }}</p>
    </div>
  `,
  styles: [
    `
      .page { max-width: 420px; margin: 40px auto; font-family: Arial, sans-serif; }
      .card { border: 1px solid #d7d7d7; padding: 16px; display: grid; gap: 8px; }
      input { padding: 10px; border: 1px solid #ccc; border-radius: 4px; font-size: 14px; }
      input:focus { outline: none; border-color: #2196F3; box-shadow: 0 0 4px rgba(33, 150, 243, 0.3); }
      button {
        padding: 10px 16px;
        background-color: #2196F3;
        color: white;
        border: none;
        border-radius: 4px;
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        transition: background-color 0.2s;
      }
      button:hover:not(:disabled) { background-color: #1976D2; }
      button:active:not(:disabled) { background-color: #1565C0; }
      button:disabled { background-color: #ccc; cursor: not-allowed; opacity: 0.6; }
      .error { color: #b00020; font-size: 14px; margin-top: 8px; }
      .help { color: #555; font-size: 13px; }
      label { font-weight: 600; font-size: 14px; }
    `,
  ],
})
export class LoginComponent {
  username = '';
  password = '';
  loading = false;
  error = '';

  constructor(private auth: AuthService, private router: Router) {}

  submit(): void {
    if (!this.username || !this.password) {
      this.error = 'Please enter both username and password';
      return;
    }
    this.error = '';
    this.loading = true;
    this.auth.login({ username: this.username, password: this.password }).subscribe({
      next: () => {
        this.loading = false;
        this.router.navigate(['/dashboard']);
      },
      error: (err) => {
        this.loading = false;
        this.error = err?.error?.detail ?? 'Login failed';
      },
    });
  }
}
