import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Predlog } from '../../models/predlog';

@Injectable({
  providedIn: 'root'
})
export class PredlogService {

  constructor(private httpClient: HttpClient) {}

  getPredlog(id: number): Observable<any> {
    return this.httpClient.get(`/api/korpus/predlog/${id}/`);
  }

  getPredlogByTekst(tekst: string): Observable<any> {
    return this.httpClient.get('api/korpus/predlog/', {
        params: new HttpParams().set('tekst', tekst)
      });
  }

  savePredlog(predlog: Predlog): Observable<any> { // 201
    return this.httpClient.post('api/korpus/save-predlog/', predlog);
  }

  editPredlog(predlog: Predlog): Observable<any> { // 204 || 409
    return this.httpClient.put('api/korpus/save-predlog/', predlog);
  }
}
