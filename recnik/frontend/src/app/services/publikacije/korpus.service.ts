import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class KorpusService {

  constructor(private http: HttpClient) { }

  searchIzvor(text: string): Observable<any[]> {
    return this.http.get<any[]>(`/api/pretraga/naslov/?q=${text}`);
  }

  loadIzvor(izvorId: number): Observable<any> {
    return this.http.get<any>(`/api/pretraga/naslov/${izvorId}/`);
  }
}
