import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Determinant } from '../../models/determinant';

@Injectable({
  providedIn: 'root',
})
export class OdrednicaService {

  constructor(private httpClient: HttpClient) { }

  getOdrednica(id: number): Observable<any> {
    return this.httpClient.get(`/api/odrednice/odrednica/${id}/`);
  }

  saveOdrednica(odrednica: Determinant): Observable<any> {
    return this.httpClient.post('api/odrednice/save-odrednica/', odrednica);
  }
}
