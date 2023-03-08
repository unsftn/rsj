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

  constructor(private http: HttpClient) {}

  get(id: number): Observable<any> {
    return this.http.get<any>(`/api/odrednice/odrednica/${id}/`);
  }

  getAllSorted(): Observable<any> {
    return this.http.get<any>(`/api/odrednice/short-odrednica-alpha/`);
  }

  getAllWithNotes(): Observable<any> {
    return this.http.get<any>(`/api/odrednice/short-odrednica-with-notes/`);
  }

  save(odrednica: Determinant): Observable<any> {
    return this.http.post<any>('/api/odrednice/save/', odrednica);
  }

  update(odrednica: Determinant): Observable<any> {
    return this.http.put<any>('/api/odrednice/save/', odrednica);
  }

  preview(odrednica: Determinant): Observable<any> {
    return this.http.post<any>('/api/render/preview/', odrednica);
  }

  delete(id: number): Observable<any> {
    return this.http.delete<any>(`/api/odrednice/delete/${id}/`);
  }

  search(text: string): Observable<any> {
    return this.http.get<any>(`/api/pretraga/odrednica/?q=${text}`);
  }

  searchWithMeanings(text: string): Observable<any> {
    return this.http.get<any>(`/api/pretraga/odrednica-znacenja/?q=${text}`);
  }

  my(pageSize: number): Observable<any> {
    return this.http.get<any>(`/api/odrednice/workflow/moje-odrednice/${pageSize}/`);
  }

  nobodys(pageSize: number): Observable<any> {
    return this.http.get<any>(`/api/odrednice/workflow/nicije-odrednice/${pageSize}/`);
  }

  toObradjivac(id: number): Observable<any> {
    return this.http.post<any>(`/api/odrednice/workflow/za-obradjivaca/${id}/`, {});
  }

  toRedaktor(id: number): Observable<any> {
    return this.http.post<any>(`/api/odrednice/workflow/za-redaktora/${id}/`, {});
  }

  toUrednik(id: number): Observable<any> {
    return this.http.post<any>(`/api/odrednice/workflow/za-urednika/${id}/`, {});
  }

  toKraj(id: number): Observable<any> {
    return this.http.post<any>(`/api/odrednice/workflow/kraj/${id}/`, {});
  }

  statObradjivaca(): Observable<any> {
    return this.http.get<any>('/api/odrednice/stats/obradjivaci/');
  }

  grafikon(tip: number): Observable<any> {
    return this.http.get<any>(`/api/odrednice/stats/grafikon/${tip}/`);
  }

  zaduzenja(id: number, obradjivac: number, redaktor: number, urednik: number): Observable<any> {
    return this.http.put<any>(`/api/odrednice/workflow/zaduzenja/${id}/`, {obradjivac, redaktor, urednik});
  }

  odredniceObradjivaca(userId: number): Observable<any> {
    return this.http.get<any>(`/api/odrednice/short-odrednica/?obradjivac_id=${userId}`);
  }

  getStatuses(): Observable<DeterminantStatus[]> {
    if (this.statusCache) {
      return this.statusCache;
    }
    this.statusCache = this.http.get<DeterminantStatus[]>('/api/odrednice/status-odrednice/').pipe(
      shareReplay(1),
      catchError((err) => {
        this.statusCache = null;
        return EMPTY;
      })
    );
    return this.statusCache;
  }

  checkDuplicate(word: string, id: number, homo: number, vrsta: number): Observable<any> {
    let req = `/api/pretraga/odrednica/duplicate/?q=${word}`;
    if (id)
      req += `&id=${id}`;
    if (homo)
      req += `&homo=${homo}`;
    if (vrsta)
      req += `&vrsta=${vrsta}`;
    return this.http.get(req);
  }
}
