import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Veznik } from '../../models/reci';

@Injectable({
  providedIn: 'root'
})
export class VeznikService {

  constructor(private http: HttpClient) { }

  new(): Veznik {
    return { id: null, tekst: '' };
  }

  get(id: number): Observable<any> {
    return this.http.get<any>(`/api/reci/veznici/${id}/`);
  }

  add(veznik: Veznik): Observable<any> {
    return this.http.post<any>(`/api/reci/save/veznik/`, veznik);
  }

  update(veznik: Veznik): Observable<any> {
    return this.http.put<any>(`/api/reci/save/veznik/`, veznik);
  }

}
