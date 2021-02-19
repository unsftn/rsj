import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Recca } from '../../models/recca';

@Injectable({
  providedIn: 'root'
})
export class ReccaService {

  constructor(private httpClient: HttpClient) {}

  getRecca(id: number): Observable<any> {
    return this.httpClient.get(`/api/korpus/recca/${id}/`);
  }

  getReccaByTekst(tekst: string): Observable<any> {
    return this.httpClient.get('api/korpus/recca/', {
        params: new HttpParams().set('tekst', tekst)
      });
  }

  saveRecca(recca: Recca): Observable<any> { // 201
    return this.httpClient.post('api/korpus/save-recca/', recca);
  }

  editRecca(recca: Recca): Observable<any> { // 204 || 409
    return this.httpClient.put('api/korpus/save-recca/', recca);
  }
}
