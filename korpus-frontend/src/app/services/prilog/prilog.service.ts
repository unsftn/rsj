import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Prilog } from '../../models/prilog';

@Injectable({
  providedIn: 'root'
})
export class PrilogService {

  constructor(private httpClient: HttpClient) {}

  getPrilog(id: number): Observable<any> {
    return this.httpClient.get(`/api/korpus/prilog/${id}/`);
  }

  getPrilogByTekst(tekst: string): Observable<any> {
    return this.httpClient.get('api/korpus/prilog/', {
        params: new HttpParams().set('tekst', tekst)
      });
  }

  savePrilog(prilog: Prilog): Observable<any> { // 201
    return this.httpClient.post('api/korpus/save-prilog/', prilog);
  }

  editPrilog(prilog: Prilog): Observable<any> { // 204 || 409
    return this.httpClient.put('api/korpus/save-prilog/', prilog);
  }
}
