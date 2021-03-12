import { Injectable, SecurityContext } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PublikacijaService {

  constructor(
    private httpClient: HttpClient,
    private domSanitizer: DomSanitizer,
  ) {}

  get(id: number): Observable<any> {
    return this.httpClient.get<any>(`/api/publikacije/publikacija/${id}/`);
  }

  getAll(): Observable<any[]> {
    return this.httpClient.get<any[]>(`/api/publikacije/publikacija/`);
  }

  getAllTypes(): Observable<any[]> {
    return this.httpClient.get<any[]>(`/api/publikacije/vrsta-publikacije/`);
  }

  getType(id: number): Observable<any> {
    return this.httpClient.get<any>(`/api/publikacije/vrsta-publikacije/${id}/`);
  }

  save(publikacija: any): Observable<any> {
    return this.httpClient.post<any>(`/api/publikacije/create-publikacija/`, publikacija);
  }

  getOpis(pub: any): SafeHtml {
    let retVal = '';
    for (const autor of pub.autor_set) {
      retVal += autor.prezime + ', ' + autor.ime;
    }
    if (retVal.length > 0)
      retVal += ': ';
    retVal += '<i>' + pub.naslov + '</i>';
    if (pub.izdavac.length > 0)
      retVal += ', ' + pub.izdavac;
    if (pub.godina.length > 0)
      retVal += ', ' + pub.godina;
    if (retVal[-1] !== '.')
      retVal += '.';
    return this.domSanitizer.bypassSecurityTrustHtml(retVal);
  }
}
