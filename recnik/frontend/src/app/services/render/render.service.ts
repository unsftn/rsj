import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Render } from '../../models';

@Injectable({
  providedIn: 'root',
})
export class RenderService {
  constructor(private httpClient: HttpClient) {}

  getRenderi(): Observable<Render[]> {
    return this.httpClient.get<Render[]>('/api/render/dokument/');
  }

  getRender(id: number): Observable<Render> {
    return this.httpClient.get<Render>(`/api/render/dokument/${id}/`);
  }
}
