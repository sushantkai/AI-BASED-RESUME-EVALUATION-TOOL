import { CommonModule } from '@angular/common';
import { Component, OnInit, inject } from '@angular/core';
import { FormBuilder, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';

import { CandidateService } from '../../core/candidate.service';
import { Candidate, CandidateDetail } from '../../core/models';

@Component({
  selector: 'app-candidates',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, FormsModule],
  template: `
    <h2>Candidates</h2>

    <form [formGroup]="createForm" (ngSubmit)="createCandidate()" class="box">
      <h3>Create Candidate</h3>
      <div class="row">
        <input placeholder="Name" formControlName="name" />
        <input placeholder="Email" formControlName="email" />
        <input placeholder="Phone" formControlName="phone" />
        <button type="submit" [disabled]="createForm.invalid">Create</button>
      </div>
      <p class="msg" [ngClass]="createMessage.includes('success') ? 'success' : 'error'" *ngIf="createMessage">{{ createMessage }}</p>
    </form>

    <div class="box">
      <h3>Filters</h3>
      <div class="row">
        <input [(ngModel)]="skillsFilter" placeholder="Skills (comma separated)" />
        <input type="number" [(ngModel)]="minExperience" placeholder="Min experience" />
        <button (click)="loadCandidates()">Apply Filters</button>
      </div>
    </div>

    <table>
      <tr>
        <th>ID</th><th>Name</th><th>Email</th><th>Skills</th><th>Experience</th><th>Action</th>
      </tr>
      <tr *ngFor="let c of candidates">
        <td>{{ c.id }}</td>
        <td>{{ c.name }}</td>
        <td>{{ c.email }}</td>
        <td>{{ c.skills.join(', ') }}</td>
        <td>{{ c.experience_years }}</td>
        <td><button (click)="selectCandidate(c.id)">View</button></td>
      </tr>
    </table>

    <div *ngIf="selected" class="box">
      <h3>Candidate Detail - {{ selected.name }}</h3>
      <p><b>Summary:</b> {{ selected.summary || '-' }}</p>
      <p><b>Education:</b> {{ selected.education || '-' }}</p>
      <p><b>Skills:</b> {{ selected.skills.join(', ') || '-' }}</p>
      <p><b>Experience:</b> {{ selected.experience_years }} years</p>

      <div class="row">
        <input type="file" (change)="onFileChange($event)" />
        <button (click)="uploadResume()" [disabled]="!selectedFile">Upload Resume</button>
      </div>
      <p>{{ message }}</p>
    </div>
  `,
  styles: [
    `
      .box { border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; }
      .row { display: flex; gap: 8px; flex-wrap: wrap; }
      input, button { padding: 6px; }
      table { width: 100%; border-collapse: collapse; margin-top: 8px; }
      th, td { border: 1px solid #ddd; padding: 6px; }
      .msg { margin-top: 8px; padding: 8px; border-radius: 4px; }
      .msg.success { background: #d4edda; color: #155724; }
      .msg.error { background: #f8d7da; color: #721c24; }
    `,
  ],
})
export class CandidatesComponent implements OnInit {
  private fb = inject(FormBuilder);

  candidates: Candidate[] = [];
  selected: CandidateDetail | null = null;
  selectedFile: File | null = null;
  message = '';
  createMessage = '';

  skillsFilter = '';
  minExperience: number | null = null;

  createForm = this.fb.group({
    name: ['', Validators.required],
    email: ['', [Validators.required, Validators.email]],
    phone: [''],
  });

  constructor(private candidateService: CandidateService) {}

  ngOnInit(): void {
    this.loadCandidates();
  }

  loadCandidates(): void {
    this.candidateService
      .list({ skills: this.skillsFilter || undefined, min_experience: this.minExperience })
      .subscribe((res) => (this.candidates = res));
  }

  createCandidate(): void {
    if (this.createForm.invalid) {
      this.createMessage = 'Please fill in all required fields';
      return;
    }
    this.createMessage = '';
    const raw = this.createForm.getRawValue();
    this.candidateService
      .create({
        name: raw.name ?? '',
        email: raw.email ?? '',
        phone: raw.phone ?? '',
      })
      .subscribe({
        next: () => {
          this.createMessage = 'Candidate created successfully';
          this.createForm.reset();
          this.loadCandidates();
          setTimeout(() => (this.createMessage = ''), 3000);
        },
        error: (err) => {
          this.createMessage = err?.error?.detail ?? 'Failed to create candidate';
        },
      });
  }

  selectCandidate(id: number): void {
    this.message = '';
    this.selectedFile = null;
    this.candidateService.detail(id).subscribe((res) => (this.selected = res));
  }

  onFileChange(event: Event): void {
    const target = event.target as HTMLInputElement;
    this.selectedFile = target.files?.[0] ?? null;
  }

  uploadResume(): void {
    if (!this.selected || !this.selectedFile) {
      return;
    }
    this.candidateService.uploadResume(this.selected.id, this.selectedFile).subscribe((res) => {
      this.message = res.message;
      this.selectCandidate(this.selected!.id);
      this.loadCandidates();
    });
  }
}
