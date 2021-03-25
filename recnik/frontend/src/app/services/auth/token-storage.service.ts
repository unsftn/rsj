import { Injectable } from '@angular/core';
import { Observable, Observer, of } from 'rxjs';

const ACCESS_TOKEN = 'access-token';
const REFRESH_TOKEN = 'refresh-token';
const USER = 'user';

@Injectable({ providedIn: 'root' })
export class TokenStorageService {
  loggedIn$: Observable<boolean>;
  private observers: any[] = [];

  constructor() {
    this.loggedIn$ = new Observable((observer) => {
      this.observers.push(observer);
    });
  }

  signOut(): void {
    sessionStorage.clear();
    this.observers.forEach((observer) => observer.next(false));
  }

  public saveToken(accessToken: string, refreshToken: string): void {
    sessionStorage.removeItem(ACCESS_TOKEN);
    sessionStorage.setItem(ACCESS_TOKEN, accessToken);
    sessionStorage.removeItem(REFRESH_TOKEN);
    sessionStorage.setItem(REFRESH_TOKEN, refreshToken);
  }

  public getAccessToken(): string {
    return sessionStorage.getItem(ACCESS_TOKEN);
  }

  public getRefreshToken(): string {
    return sessionStorage.getItem(REFRESH_TOKEN);
  }

  public saveUser(user): void {
    sessionStorage.removeItem(USER);
    sessionStorage.setItem(USER, JSON.stringify(user));
    this.observers.forEach((observer) => observer.next(true));
  }

  public isLoggedIn(): boolean {
    return this.getUser() != null;
  }

  public getUser(): any {
    const user = sessionStorage.getItem(USER);
    if (user == null) {
      return null;
    }
    return JSON.parse(user);
  }
}
