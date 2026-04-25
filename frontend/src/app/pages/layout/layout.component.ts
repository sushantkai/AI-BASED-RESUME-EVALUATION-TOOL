import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { Router, RouterLink, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterOutlet],
  template: `
    <nav class="nav">
      <a routerLink="/dashboard">Dashboard</a>
      <a routerLink="/candidates">Candidates</a>
      <a routerLink="/jobs">Jobs</a>
      <a routerLink="/matches">Matching</a>
      <div class="spacer"></div>
      <button class="logout" type="button" (click)="logout()">Logout</button>
    </nav>
    <main class="page">
      <router-outlet></router-outlet>
    </main>
  `,
  styles: [
    `
      .nav { display: flex; gap: 12px; align-items: center; padding: 12px; background: #fff; border-bottom: 1px solid #ddd; }
      .nav a { text-decoration: none; color: #4a148c; font-weight: 600; }
      .spacer { flex: 1; }
      .logout { padding: 6px 12px; }
      .page { padding: 16px; }
    `,
  ],
})
export class LayoutComponent {
  constructor(private router: Router) {}

  logout() {
    localStorage.clear();
    this.router.navigate(['/login']);
  }
}