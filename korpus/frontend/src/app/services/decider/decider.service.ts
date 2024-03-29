import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { RecZaOdluku, GenerisaniSpisak } from '../../models/reci';

@Injectable({
  providedIn: 'root'
})
export class DeciderService {

  constructor(private http: HttpClient) { }

  get(id: number): Observable<RecZaOdluku> {
    return this.http.get<RecZaOdluku>(`/api/decider/rec-za-odluku/${id}/`);
  }

  getAll(): Observable<RecZaOdluku[]> {
    return this.http.get<RecZaOdluku[]>(`/api/decider/rec-za-odluku/`);
  }

  getByLetter(letter: string): Observable<RecZaOdluku[]> {
    return this.http.get<RecZaOdluku[]>(`/api/decider/rec-za-odluku/?prvo_slovo=${letter}`);
  }

  getByLetterPagedFiltered(letter: string, offset: number, limit: number, recnik: boolean, 
      odluka: number[], potkorpus: number[], beleska: boolean, leksema: string, 
      frekOd: number, frekDo: number): Observable<RecZaOdluku[]> {
    let url = `/api/decider/rec-za-odluku-po/${letter}/?offset=${offset}&limit=${limit}`;
    if (recnik != null)
      url += `&recnik=${recnik}`;
    if (odluka)
      url += `&odluka=${odluka.join(',')}`;
    if (potkorpus)
      url += `&potkorpus=${potkorpus.join(',')}`;
    if (leksema)
      url += `&leksema=${leksema}`;
    if (beleska !== null)
      url += `&beleska=${beleska}`;
    if (frekOd !== null)
        url += `&frekod=${frekOd}`;
    if (frekDo !== null)
      url += `&frekdo=${frekDo}`;
    return this.http.get<RecZaOdluku[]>(url);
  }

  update(rec: RecZaOdluku): Observable<any> {
    return this.http.put<any>(`/api/decider/rec-za-odluku/${rec.id}/`, rec);
  }

  getLastSpisak(): Observable<GenerisaniSpisak> {
    return this.http.get<GenerisaniSpisak>(`/api/decider/generisani-spisak/poslednji/`);
  }

  createReport(upit: any): Observable<number> {
    return this.http.post<number>(`/api/decider/report/`, upit);
  }

  getReport(id: number): Observable<any> {
    return this.http.get<any>(`/api/decider/report/${id}/`);
  }

  getBrojOdluka(): Observable<any[]> {
    return this.http.get<any[]>(`/api/decider/stats/broj-odluka/`);
  }
}
