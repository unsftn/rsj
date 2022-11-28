import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class StatsService {

  constructor(private http: HttpClient) { }

  getBrojUnetihReciZaSve(): Observable<any> {
    return this.http.get<any>(`/api/reci/stats/unos-reci/`);
  }

  getMojeReci(): Observable<any> {
    return this.http.get<any>(`/api/reci/stats/moje-reci/`);
  }

  getReciKorisnika(userID: number): Observable<any> {
    return this.http.get<any>(`/api/reci/stats/reci-korisnika/${userID}/`);
  }

  getBrojMojihReci(): Observable<any> {
    return this.http.get<any>(`/api/reci/stats/broj-mojih-reci/`);
  }
}
