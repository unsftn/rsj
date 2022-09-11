import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class StatsService {

  constructor(private http: HttpClient) { }

  getBrojUnetihReci(): Observable<any> {
    return this.http.get<any>(`/api/reci/stats/bur/`);
  }

  getBrojUnetihReciZaSve(): Observable<any> {
    return this.http.get<any>(`/api/reci/stats/bur/svi/`);
  }
}
