import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Uzvik } from '../../models/reci';

@Injectable({
  providedIn: 'root'
})
export class UzvikService {

  constructor(private http: HttpClient) { }

  new(): Uzvik {
    return { id: null, tekst: '' };
  }

  get(id: number): Observable<any> {
    return this.http.get<any>(`/api/reci/uzvici/${id}/`);
  }

  add(uzvik: Uzvik): Observable<any> {
    return this.http.post<any>(`/api/reci/save/uzvik/`, uzvik);
  }

  update(uzvik: Uzvik): Observable<any> {
    return this.http.put<any>(`/api/reci/save/uzvik/`, uzvik);
  }

}
