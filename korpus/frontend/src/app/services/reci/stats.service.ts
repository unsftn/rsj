import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class StatsService {

  constructor(private http: HttpClient) { }

  // getBrojUnetihReci(): Observable<any> {
  //   return this.http.get<any>(`/api/reci/stats/bur/`);
  // }

  getBrojUnetihReciZaSve(): Observable<any> {
    return this.http.get<any>(`/api/reci/stats/unos-reci/`);
  }

  getMojeReci(): Observable<any> {
    return this.http.get<any>(`/api/reci/stats/moje-reci/`);
  }

  getBrojMojihReci(): Observable<any> {
    return this.http.get<any>(`/api/reci/stats/broj-mojih-reci/`);
  }
}