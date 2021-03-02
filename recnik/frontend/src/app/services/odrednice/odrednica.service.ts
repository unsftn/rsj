import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Determinant } from '../../models/determinant';

@Injectable({
  providedIn: 'root',
})
export class OdrednicaService {
  constructor(private httpClient: HttpClient) {}

  get(id: number): Observable<any> {
    return this.httpClient.get(`/api/odrednice/odrednica/${id}/`);
  }

  save(odrednica: Determinant): Observable<any> {
    return this.httpClient.post('/api/odrednice/save/', odrednica);
  }

  update(odrednica: Determinant): Observable<any> {
    return this.httpClient.put('/api/odrednice/save/', odrednica);
  }

  preview(odrednica: Determinant): Observable<any> {
    return this.httpClient.post('/api/odrednice/preview/', odrednica);
  }

  delete(id: number): Observable<any> {
    return this.httpClient.delete(`/api/odrednice/delete/${id}/`);
  }

  search(text: string): Observable<any> {
    return this.httpClient.get(`/api/pretraga/odrednica/?q=${text}`);
  }
}
