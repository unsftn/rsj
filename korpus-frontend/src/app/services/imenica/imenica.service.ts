import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Imenica } from '../../models/imenica';

@Injectable({
  providedIn: 'root'
})
export class ImenicaService {

  constructor(private httpClient: HttpClient) {}

  getImenica(id: number): Observable<any> {
    return this.httpClient.get(`/api/korpus/imenica/${id}/`);
  }

  getImenicaByNomJed(nomjed: string): Observable<any> {
    return this.httpClient.get('api/korpus/imenica/', {
        params: new HttpParams().set('nomjed', nomjed)
      });
  }

  getImenicaByVrstaId(id: string): Observable<any> {
    return this.httpClient.get('api/korpus/imenica/', {
        params: new HttpParams().set('vrsta_id', id)
      });
  }

  saveImenica(imenica: Imenica): Observable<any> { // 201
    return this.httpClient.post('api/korpus/save-imenica/', imenica);
  }

  editImenica(imenica: Imenica): Observable<any> { // 204 || 409
    return this.httpClient.put('api/korpus/save-imenica/', imenica);
  }
}
