import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Glagol } from '../../models/glagol';

@Injectable({
  providedIn: 'root'
})
export class GlagolService {

  constructor(private httpClient: HttpClient) {}

  getGlagol(id: number): Observable<any> {
    return this.httpClient.get(`/api/korpus/glagol/${id}/`);
  }

  getGlagolByInfinitiv(infinitiv: string): Observable<any> {
    return this.httpClient.get('api/korpus/glagol/', {
        params: new HttpParams().set('infinitiv', infinitiv)
      });
  }

  getGlagolByRod(rodId: number): Observable<any> {
    return this.httpClient.get('api/korpus/glagol/', {
        params: new HttpParams().set('rod', rodId.toString())
      });
  }

  saveGlagol(glagol: Glagol): Observable<any> { // 201
    return this.httpClient.post('api/korpus/save-glagol/', glagol);
  }

  editGlagol(glagol: Glagol): Observable<any> { // 204 || 409
    return this.httpClient.put('api/korpus/save-glagol/', glagol);
  }
}
