import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Zamenica } from '../../models/reci';

@Injectable({
  providedIn: 'root'
})
export class ZamenicaService {

  constructor(private http: HttpClient) { }

  new(): Zamenica {
    return {
      nomjed: '', genjed: '', datjed: '', akujed: '', vokjed: '', insjed: '', lokjed: '',
      varijante: [], recnikID: null };
  }

  get(id: number): Observable<any> {
    return this.http.get<any>(`/api/reci/zamenice/${id}/`);
  }

  add(zamenica: Zamenica): Observable<any> {
    return this.http.post<any>(`/api/reci/save/zamenica/`, zamenica);
  }

  update(zamenica: Zamenica): Observable<any> {
    return this.http.put<any>(`/api/reci/save/zamenica/`, zamenica);
  }

}
