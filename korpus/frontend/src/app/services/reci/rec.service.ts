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
      case 3: return of({});  // TODO
      case 4: return of({});  // TODO
      case 5: return of({});  // TODO
      case 6: return of({});  // TODO
      case 7: return of({});  // TODO
      case 8: return of({});  // TODO
      case 9: return of({});  // TODO
    }
  }

  getEditLink(wordType: number): string {
    switch (wordType) {
      case 0: return '/imenica';
      case 1: return '/glagol';
      case 2: return '/pridev';
      default: return '';
    }
  }

  getEditRouterLink(id: number, wordType: number): any[] {
    return [this.getEditLink(wordType), id];
  }
}
