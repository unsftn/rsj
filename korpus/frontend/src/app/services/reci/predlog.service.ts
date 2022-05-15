import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Predlog } from '../../models/reci';

@Injectable({
  providedIn: 'root'
})
export class PredlogService {

  constructor(private http: HttpClient) { }

  new(): Predlog {
    return { id: null, tekst: '' };
  }

  get(id: number): Observable<any> {
    return this.http.get<any>(`/api/reci/predlozi/${id}/`);
  }

  add(predlog: Predlog): Observable<any> {
    return this.http.post<any>(`/api/reci/save/predlog/`, predlog);
  }

  update(predlog: Predlog): Observable<any> {
    return this.http.put<any>(`/api/reci/save/predlog/`, predlog);
  }

}
