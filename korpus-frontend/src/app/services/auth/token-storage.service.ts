import { Injectable } from '@angular/core';

const ACCESS_TOKEN = 'access-token';
const REFRESH_TOKEN = 'refresh-token';
const USER = 'user';

@Injectable({ providedIn: 'root' })
export class TokenStorageService {
  constructor() {}

  signOut(): void {
    sessionStorage.clear();
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
  }

  public isLoggedIn(): boolean {
    return this.getUser() != null;
  }

  public getUser(): any {
    const user = sessionStorage.getItem(USER);
    if (user == null)
      return null;
    return JSON.parse(user);
  }
}
