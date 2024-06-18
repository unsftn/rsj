import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { TokenStorageService } from './token-storage.service';

@Injectable()
export class AuthErrorInterceptor implements HttpInterceptor {
  constructor(
    private tokenStorageService: TokenStorageService,
    private router: Router) {}

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    return next.handle(request).pipe(
      catchError((err) => {
        if (err.status === 401) {
          this.tokenStorageService.signOut();
          this.router.navigate(['/login']);
        }
        const error = err.error.message || err.statusText;
        return throwError(() => error);
      })
    );
  }
}
