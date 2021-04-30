import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/x-www-form-urlencoded',
  }),
};

@Injectable({ providedIn: 'root' })
export class AuthService {
  constructor(private http: HttpClient) {}

  login(email: string, password: string): Observable<any> {
    const formData = `username=${email}&password=${password}`;
    return this.http.post('/api/token/', formData, httpOptions);
  }

  changePassword(newPassword: string): Observable<any> {
    return this.http.put('/api/odrednice/password/change/', {newPassword});
  }
}
