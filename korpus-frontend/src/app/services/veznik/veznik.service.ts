import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Veznik } from '../../models/veznik';

@Injectable({
  providedIn: 'root'
})
export class VeznikService {

  constructor(private httpClient: HttpClient) {}

  getVeznik(id: number): Observable<any> {
    return this.httpClient.get(`/api/korpus/veznik/${id}/`);
  }

  getVeznikByTekst(tekst: string): Observable<any> {
    return this.httpClient.get('api/korpus/veznik/', {
        params: new HttpParams().set('tekst', tekst)
      });
  }

  saveVeznik(veznik: Veznik): Observable<any> { // 201
    return this.httpClient.post('api/korpus/save-veznik/', veznik);
  }

  editVeznik(veznik: Veznik): Observable<any> { // 204 || 409
    return this.httpClient.put('api/korpus/save-veznik/', veznik);
  }
}
