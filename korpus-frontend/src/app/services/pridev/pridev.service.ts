import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Pridev } from '../../models/pridev';

@Injectable({
  providedIn: 'root'
})
export class PridevService {

  constructor(private httpClient: HttpClient) {}

  getPridev(id: number): Observable<any> {
    return this.httpClient.get(`/api/korpus/pridev/${id}/`);
  }

  getPridevByTekst(tekst: string): Observable<any> {
    return this.httpClient.get('api/korpus/pridev/', {
        params: new HttpParams().set('tekst', tekst)
      });
  }

  savePridev(pridev: Pridev): Observable<any> { // 201
    return this.httpClient.post('api/korpus/save-pridev/', pridev);
  }

  editPridev(pridev: Pridev): Observable<any> { // 204 || 409
    return this.httpClient.put('api/korpus/save-pridev/', pridev);
  }
}
