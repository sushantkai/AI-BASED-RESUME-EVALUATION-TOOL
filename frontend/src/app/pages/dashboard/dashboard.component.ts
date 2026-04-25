import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';

import { DashboardService } from '../../core/dashboard.service';
import { DashboardData } from '../../core/models';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h2>Dashboard</h2>
    <div class="stats" *ngIf="data">
      <div class="card">Total Candidates: <b>{{ data.total_candidates }}</b></div>
      <div class="card">Total Jobs: <b>{{ data.total_jobs }}</b></div>
    </div>

    <div class="grid" *ngIf="data">
      <div>
        <h3>Recent Candidates</h3>
        <table>
          <tr><th>ID</th><th>Name</th><th>Created</th></tr>
          <tr *ngFor="let c of data.recent_candidates">
            <td>{{ c.id }}</td>
            <td>{{ c.name }}</td>
            <td>{{ c.created_at | date:'short' }}</td>
          </tr>
        </table>
      </div>
      <div>
        <h3>Recent Jobs</h3>
        <table>
          <tr><th>ID</th><th>Title</th><th>Created</th></tr>
          <tr *ngFor="let j of data.recent_jobs">
            <td>{{ j.id }}</td>
            <td>{{ j.title }}</td>
            <td>{{ j.created_at | date:'short' }}</td>
          </tr>
        </table>
      </div>
    </div>
  `,
  styles: [
    `
      .stats { display: flex; gap: 12px; margin-bottom: 12px; }
      .card { border: 1px solid #ddd; padding: 8px 12px; }
      .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
      table { width: 100%; border-collapse: collapse; }
      th, td { border: 1px solid #ddd; padding: 6px; text-align: left; }
    `,
  ],
})
export class DashboardComponent implements OnInit {
  data: DashboardData | null = null;

  constructor(private dashboardService: DashboardService) {}

  ngOnInit(): void {
    this.dashboardService.getData().subscribe((res) => (this.data = res));
  }
}

