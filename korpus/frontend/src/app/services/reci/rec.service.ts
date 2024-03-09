import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RecService {

  constructor(private http: HttpClient) { }

  get(id: number, wordType: number): Observable<any> {
    switch (wordType) {
      case 0: return this.http.get<any>(`/api/reci/imenice/${id}/`);
      case 1: return this.http.get<any>(`/api/reci/glagoli/${id}/`);
      case 2: return this.http.get<any>(`/api/reci/pridevi/${id}/`);
      case 3: return this.http.get<any>(`/api/reci/prilozi/${id}/`);
      case 4: return this.http.get<any>(`/api/reci/predlozi/${id}/`);
      case 5: return this.http.get<any>(`/api/reci/zamenice/${id}/`);
      case 6: return this.http.get<any>(`/api/reci/uzvici/${id}/`);
      case 7: return this.http.get<any>(`/api/reci/recce/${id}/`);
      case 8: return this.http.get<any>(`/api/reci/veznici/${id}/`);
      case 9: return this.http.get<any>(`/api/reci/brojevi/${id}/`);
    }
  }

  getEditLink(wordType: number): string {
    switch (wordType) {
      case 0: return '/imenica';
      case 1: return '/glagol';
      case 2: return '/pridev';
      case 3: return '/prilog';
      case 4: return '/predlog';
      case 5: return '/zamenica';
      case 6: return '/uzvik';
      case 7: return '/recca';
      case 8: return '/veznik';
      case 9: return '/broj';
      default: return '';
    }
  }

  getEditRouterLink(id: number, wordType: number): any[] {
    return [this.getEditLink(wordType), id];
  }

  remove(id: number, wordType: number): Observable<any> {
    return this.http.delete<any>(`/api/reci/delete/${wordType}/${id}/`);
  }
}
