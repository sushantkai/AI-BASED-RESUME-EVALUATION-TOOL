import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { CandidateService } from '../../core/candidate.service';
import { JobService } from '../../core/job.service';
import { MatchingService } from '../../core/matching.service';
import { Candidate, CandidateMatchView, Job, JobMatchView } from '../../core/models';

@Component({
  selector: 'app-matches',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <h2>Matching</h2>
    <div class="box">
      <button (click)="runMatch()">Run Full Matching</button>
    </div>

    <div class="grid">
      <div class="box">
        <h3>Candidate-Centric View</h3>
        <select [(ngModel)]="selectedCandidateId">
          <option [ngValue]="null">Select Candidate</option>
          <option *ngFor="let c of candidates" [ngValue]="c.id">{{ c.name }}</option>
        </select>
        <button (click)="loadCandidateView()">Load</button>
        <table>
          <tr><th>Job</th><th>Skill %</th><th>Exp %</th><th>Overall</th></tr>
          <tr *ngFor="let row of candidateView">
            <td>{{ row.job_title }}</td>
            <td>{{ row.skill_match_pct }}</td>
            <td>{{ row.experience_match_pct }}</td>
            <td>{{ row.overall_score }}</td>
          </tr>
        </table>
      </div>

      <div class="box">
        <h3>Job-Centric Ranked List</h3>
        <select [(ngModel)]="selectedJobId">
          <option [ngValue]="null">Select Job</option>
          <option *ngFor="let j of jobs" [ngValue]="j.id">{{ j.title }}</option>
        </select>
        <button (click)="loadJobView()">Load</button>
        <table>
          <tr><th>Candidate</th><th>Overall</th><th>Skill %</th><th>Exp %</th></tr>
          <tr *ngFor="let row of jobView">
            <td>{{ row.candidate_name }}</td>
            <td>{{ row.overall_score }}</td>
            <td>{{ row.skill_match_pct }}</td>
            <td>{{ row.experience_match_pct }}</td>
          </tr>
        </table>
      </div>
    </div>
  `,
  styles: [
    `
      .box { border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; }
      .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
      table { width: 100%; border-collapse: collapse; margin-top: 8px; }
      th, td { border: 1px solid #ddd; padding: 6px; text-align: left; }
      select, button { padding: 6px; margin-right: 6px; }
    `,
  ],
})
export class MatchesComponent implements OnInit {
  candidates: Candidate[] = [];
  jobs: Job[] = [];
  selectedCandidateId: number | null = null;
  selectedJobId: number | null = null;
  candidateView: CandidateMatchView[] = [];
  jobView: JobMatchView[] = [];

  constructor(
    private matchingService: MatchingService,
    private candidateService: CandidateService,
    private jobService: JobService,
  ) {}

  ngOnInit(): void {
    this.candidateService.list({}).subscribe((res) => (this.candidates = res));
    this.jobService.list().subscribe((res) => (this.jobs = res));
  }

  runMatch(): void {
    this.matchingService.run().subscribe(() => {
      this.loadCandidateView();
      this.loadJobView();
    });
  }

  loadCandidateView(): void {
    if (!this.selectedCandidateId) {
      this.candidateView = [];
      return;
    }
    this.matchingService.byCandidate(this.selectedCandidateId).subscribe((res) => (this.candidateView = res));
  }

  loadJobView(): void {
    if (!this.selectedJobId) {
      this.jobView = [];
      return;
    }
    this.matchingService.byJob(this.selectedJobId).subscribe((res) => (this.jobView = res));
  }
}

