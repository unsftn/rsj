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
    localStorage.clear();
    this.observers.forEach((observer) => observer.next(false));
  }

  public saveToken(accessToken: string, refreshToken: string): void {
    localStorage.removeItem(ACCESS_TOKEN);
    localStorage.setItem(ACCESS_TOKEN, accessToken);
    localStorage.removeItem(REFRESH_TOKEN);
    localStorage.setItem(REFRESH_TOKEN, refreshToken);
  }

  public getAccessToken(): string {
    return localStorage.getItem(ACCESS_TOKEN);
  }

  public getRefreshToken(): string {
    return localStorage.getItem(REFRESH_TOKEN);
  }

  public saveUser(user): void {
    localStorage.removeItem(USER);
    localStorage.setItem(USER, JSON.stringify(user));
    this.observers.forEach((observer) => observer.next(true));
  }

  public isLoggedIn(): boolean {
    return this.getUser() != null;
  }

  public getUser(): any {
    const user = localStorage.getItem(USER);
    if (user == null) {
      return null;
    }
    return JSON.parse(user);
  }

  public isEditor(): boolean {
    if (!this.isLoggedIn())
      return false;
    const groups = this.getUser().groups;
    return groups.includes(1) || groups.includes(2);
  }
}
