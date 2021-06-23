import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { EMPTY, Observable } from 'rxjs';
import { Determinant, DeterminantStatus } from '../../models';
import { catchError, shareReplay } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class OdrednicaService {

  statusCache: Observable<DeterminantStatus[]>;

  constructor(private httpClient: HttpClient) {}

  get(id: number): Observable<any> {
    return this.httpClient.get(`/api/odrednice/odrednica/${id}/`);
  }

  getAllSorted(): Observable<any> {
    return this.httpClient.get(`/api/odrednice/short-odrednica-alpha/`);
  }

  save(odrednica: Determinant): Observable<any> {
    return this.httpClient.post('/api/odrednice/save/', odrednica);
  }

  update(odrednica: Determinant): Observable<any> {
    return this.httpClient.put('/api/odrednice/save/', odrednica);
  }

  preview(odrednica: Determinant): Observable<any> {
    return this.httpClient.post('/api/render/preview/', odrednica);
  }

  delete(id: number): Observable<any> {
    return this.httpClient.delete(`/api/odrednice/delete/${id}/`);
  }

  search(text: string): Observable<any> {
    return this.httpClient.get(`/api/pretraga/odrednica/?q=${text}`);
  }

  my(pageSize: number): Observable<any> {
    return this.httpClient.get(`/api/odrednice/workflow/moje-odrednice/${pageSize}/`);
  }

  toObradjivac(id: number): Observable<any> {
    return this.httpClient.post(`/api/odrednice/workflow/za-obradjivaca/${id}/`, {});
  }

  toRedaktor(id: number): Observable<any> {
    return this.httpClient.post(`/api/odrednice/workflow/za-redaktora/${id}/`, {});
  }

  toUrednik(id: number): Observable<any> {
    return this.httpClient.post(`/api/odrednice/workflow/za-urednika/${id}/`, {});
  }

  toKraj(id: number): Observable<any> {
    return this.httpClient.post(`/api/odrednice/workflow/kraj/${id}/`, {});
  }

  statObradjivaca(): Observable<any> {
    return this.httpClient.get('/api/odrednice/stats/obradjivaci/');
  }

  zaduzenja(id: number, obradjivac: number, redaktor: number, urednik: number): Observable<any> {
    return this.httpClient.put(`/api/odrednice/workflow/zaduzenja/${id}/`, {obradjivac, redaktor, urednik});
  }

  odredniceObradjivaca(userId: number): Observable<any> {
    return this.httpClient.get(`/api/odrednice/short-odrednica/?obradjivac_id=${userId}`);
  }

  getStatuses(): Observable<DeterminantStatus[]> {
    if (this.statusCache) {
      return this.statusCache;
    }
    this.statusCache = this.httpClient.get<DeterminantStatus[]>('/api/odrednice/status-odrednice/').pipe(
      shareReplay(1),
      catchError((err) => {
        this.statusCache = null;
        return EMPTY;
      })
    );
    return this.statusCache;
  }

}
