import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Recca } from '../../models/reci';

@Injectable({
  providedIn: 'root'
})
export class ReccaService {

  constructor(private http: HttpClient) { }

  new(): Recca {
    return { id: null, tekst: '' };
  }

  get(id: number): Observable<any> {
    return this.http.get<any>(`/api/reci/recce/${id}/`);
  }

  add(recca: Recca): Observable<any> {
    return this.http.post<any>(`/api/reci/save/recca/`, recca);
  }

  update(recca: Recca): Observable<any> {
    return this.http.put<any>(`/api/reci/save/recca/`, recca);
  }

}
