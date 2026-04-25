import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';

import { AuthService } from './auth.service';

export const roleGuard: CanActivateFn = (route) => {
  const auth = inject(AuthService);
  const router = inject(Router);
  const allowedRoles = route.data['roles'] as string[] | undefined;
  if (!allowedRoles || allowedRoles.length === 0) {
    return true;
  }
  const role = auth.role();
  if (role && allowedRoles.includes(role)) {
    return true;
  }
  return router.createUrlTree(['/dashboard']);
};

