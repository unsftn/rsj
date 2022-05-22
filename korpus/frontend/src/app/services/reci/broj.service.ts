import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Broj } from '../../models/reci';

@Injectable({
  providedIn: 'root'
})
export class BrojService {

  constructor(private http: HttpClient) { }

  new(): Broj {
    return {
      nomjed: '', genjed: '', datjed: '', akujed: '', vokjed: '', insjed: '', lokjed: '',
      nommno: '', genmno: '', datmno: '', akumno: '', vokmno: '', insmno: '', lokmno: '',
      recnikID: null,
    };
  }

  get(id: number): Observable<any> {
    return this.http.get<any>(`/api/reci/brojevi/${id}/`);
  }

  add(broj: Broj): Observable<any> {
    return this.http.post<any>(`/api/reci/save/broj/`, broj);
  }

  update(broj: Broj): Observable<any> {
    return this.http.put<any>(`/api/reci/save/broj/`, broj);
  }

}
