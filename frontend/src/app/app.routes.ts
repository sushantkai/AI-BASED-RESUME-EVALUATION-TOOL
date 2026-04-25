import { Routes } from '@angular/router';

import { authGuard } from './core/auth.guard';
import { roleGuard } from './core/role.guard';
import { CandidatesComponent } from './pages/candidates/candidates.component';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { JobsComponent } from './pages/jobs/jobs.component';
import { LayoutComponent } from './pages/layout/layout.component';
import { LoginComponent } from './pages/login/login.component';
import { MatchesComponent } from './pages/matches/matches.component';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  {
    path: '',
    component: LayoutComponent,
    canActivate: [authGuard],
    children: [
      { path: 'dashboard', component: DashboardComponent, canActivate: [roleGuard], data: { roles: ['Admin', 'HR'] } },
      { path: 'candidates', component: CandidatesComponent, canActivate: [roleGuard], data: { roles: ['Admin', 'HR'] } },
      { path: 'jobs', component: JobsComponent, canActivate: [roleGuard], data: { roles: ['Admin', 'HR'] } },
      { path: 'matches', component: MatchesComponent, canActivate: [roleGuard], data: { roles: ['Admin', 'HR'] } },
      { path: '', pathMatch: 'full', redirectTo: 'dashboard' },
    ],
  },
  { path: '**', redirectTo: '/dashboard' },
];
