import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Prilog } from '../../models/reci';

@Injectable({
  providedIn: 'root'
})
export class PrilogService {

  constructor(private http: HttpClient) { }

  new(): Prilog {
    return {
      komparativ: '', superlativ: '', recnikID: null,
    };
  }

  get(id: number): Observable<any> {
    return this.http.get<any>(`/api/reci/prilozi/${id}/`);
  }

  add(prilog: Prilog): Observable<any> {
    return this.http.post<any>(`/api/reci/save/prilog/`, prilog);
  }

  update(prilog: Prilog): Observable<any> {
    return this.http.put<any>(`/api/reci/save/prilog/`, prilog);
  }

}
