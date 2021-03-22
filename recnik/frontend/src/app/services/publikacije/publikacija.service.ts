import { Injectable, SecurityContext } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { Observable } from 'rxjs';
import { map } from 'rxjs/internal/operators';
import { shareReplay } from 'rxjs/operators';
import { PubType } from '../../models';

@Injectable({
  providedIn: 'root'
})
export class PublikacijaService {

  pubTypeCache: { [key: number]: PubType; } = {};
  pubTypeList: PubType[] = [];

  constructor(
    private httpClient: HttpClient,
    private domSanitizer: DomSanitizer,
  ) {}

  get(id: number): Observable<any> {
    return this.httpClient.get<any>(`/api/publikacije/publikacija/${id}/`);
  }

  getTitle(id: number): Observable<string> {
    return this.httpClient.get<any>(`/api/publikacije/publikacija/${id}`).pipe(map((v: any) => v.naslov), shareReplay(1));
  }

  getAll(): Observable<any[]> {
    return this.httpClient.get<any[]>(`/api/publikacije/publikacija/`);
  }

  add(publikacija: any): Observable<any> {
    return this.httpClient.post<any>(`/api/publikacije/save/`, publikacija);
  }

  save(publikacija: any): Observable<any> {
    return this.httpClient.put<any>(`/api/publikacije/save/`, publikacija);
  }

  search(text: string): Observable<any> {
    return this.httpClient.get(`/api/pretraga/publikacija/?q=${text}`);
  }

  getPubType(id: number): PubType {
    return this.pubTypeCache[id];
  }

  getPubTypes(): PubType[] {
    return this.pubTypeList;
  }

  getFirstPubType(): PubType {
    return this.pubTypeList[0];
  }

  fetchAllPubTypes(): Observable<PubType[]> {
    return this.httpClient.get<any[]>(`/api/publikacije/vrsta-publikacije/`).pipe(
      map((pubTypes: any[]) => {
        return pubTypes.map((item) => {
          const p = { id: item.id, naziv: item.naziv };
          this.pubTypeCache[p.id] = p;
          this.pubTypeList.push(p);
          return p;
        });
    }), shareReplay(1));
  }

  getOpis(pub: any): SafeHtml {
    let retVal = '';
    for (const autor of pub.autor_set) {
      retVal += autor.prezime + ', ' + autor.ime;
    }
    if (retVal.length > 0) {
      retVal += ': ';
    }
    retVal += '<i>' + pub.naslov + '</i>';
    if (pub.izdavac && pub.izdavac.length > 0) {
      retVal += ', ' + pub.izdavac;
    }
    if (pub.godina && pub.godina.length > 0) {
      retVal += ', ' + pub.godina;
    }
    if (retVal[-1] !== '.') {
      retVal += '.';
    }
    return this.domSanitizer.bypassSecurityTrustHtml(retVal);
  }
}
