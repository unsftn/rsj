import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Uzvik } from '../../models/uzvik';

@Injectable({
  providedIn: 'root'
})
export class UzvikService {

  constructor(private httpClient: HttpClient) {}

  getUzvik(id: number): Observable<any> {
    return this.httpClient.get(`/api/korpus/uzvik/${id}/`);
  }

  getUzvikByTekst(tekst: string): Observable<any> {
    return this.httpClient.get('api/korpus/uzvik/', {
        params: new HttpParams().set('tekst', tekst)
      });
  }

  saveUzvik(uzvik: Uzvik): Observable<any> { // 201
    return this.httpClient.post('api/korpus/save-uzvik/', uzvik);
  }

  editUzvik(uzvik: Uzvik): Observable<any> { // 204 || 409
    return this.httpClient.put('api/korpus/save-uzvik/', uzvik);
  }
}
