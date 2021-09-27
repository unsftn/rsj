import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Imenica, VrstaImenice } from '../../models/reci';

@Injectable({
  providedIn: 'root'
})
export class ImenicaService {

  vrste: VrstaImenice[] = [
    {id: null, name: '---'},
    {id: 1, name: 'апстрактна'},
    {id: 2, name: 'заједничка'},
    {id: 3, name: 'властита'},
    {id: 4, name: 'збирна'},
    {id: 5, name: 'градивна'},
    {id: 6, name: 'глаголска'},
  ];

  constructor(private http: HttpClient) { }

  get(id: number): Observable<any> {
    return this.http.get<any>(`/api/reci/imenice/${id}/`);
  }

  add(imenica: Imenica): Observable<any> {
    return this.http.post<any>(`/api/reci/save/imenica/`, imenica);
  }

  update(imenica: Imenica): Observable<any> {
    return this.http.put<any>(`/api/reci/save/imenica/`, imenica);
  }

  getVrste(): VrstaImenice[] {
    return this.vrste;
  }
}
