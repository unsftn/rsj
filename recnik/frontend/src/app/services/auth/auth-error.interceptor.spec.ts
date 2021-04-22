import { TestBed } from '@angular/core/testing';

import { AuthErrorInterceptor } from './auth-error.interceptor.service';

describe('ErrorInterceptor', () => {
  beforeEach(() => TestBed.configureTestingModule({
    providers: [
      AuthErrorInterceptor
      ]
  }));

  it('should be created', () => {
    const interceptor: AuthErrorInterceptor = TestBed.inject(AuthErrorInterceptor);
    expect(interceptor).toBeTruthy();
  });
});
