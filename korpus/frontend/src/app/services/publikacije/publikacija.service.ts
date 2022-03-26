/* tslint:disable:variable-name */
import { EventEmitter, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { Observable } from 'rxjs';
import { map, shareReplay } from 'rxjs/operators';
import { PubType } from '../../models/reci';

@Injectable({
  providedIn: 'root'
})
export class PublikacijaService {

  pubTypeCache: { [key: number]: PubType; } = {};
  pubTypeList: PubType[] = [];
  private _changed: boolean;
  private _publicationChanged: EventEmitter<boolean> = new EventEmitter<boolean>();
  private _importStep: EventEmitter<number> = new EventEmitter<number>();

  constructor(
    private http: HttpClient,
    private domSanitizer: DomSanitizer,
  ) {}

  public get changed(): boolean {
    return this._changed;
  }

  public set changed(changed: boolean) {
    this._changed = changed;
  }

  public get publicationChanged(): EventEmitter<boolean> {
    return this._publicationChanged;
  }

  public get importStep(): EventEmitter<number> {
    return this._importStep;
  }

  get(id: number): Observable<any> {
    return this.http.get<any>(`/api/publikacije/publikacija/${id}/`);
  }

  getFragment(pid: number, fid: number): Observable<any> {
    return this.http.get<any>(`/api/publikacije/publikacija/${pid}/tekst/${fid}/`);
  }

  updateFragment(pid: number, fid: number, text: string): Observable<any> {
    return this.http.put<any>(`/api/publikacije/publikacija/${pid}/tekst/${fid}/`, text);
  }

  getTitle(id: number): Observable<string> {
    return this.http.get<any>(`/api/publikacije/publikacija/${id}/`).pipe(map((v: any) => v.naslov), shareReplay(1));
  }

  getAll(): Observable<any[]> {
    return this.http.get<any[]>(`/api/publikacije/publikacija/`);
  }

  add(publikacija: any): Observable<any> {
    return this.http.post<any>(`/api/publikacije/save/publikacija/`, publikacija);
  }

  save(publikacija: any): Observable<any> {
    return this.http.put<any>(`/api/publikacije/save/publikacija/`, publikacija);
  }

  search(text: string): Observable<any> {
    return this.http.get<any>(`/api/pretraga/publikacija/?q=${text}`);
  }

  getPubType(id: number): PubType {
    if (!id)
      return null;
    return this.pubTypeCache[id];
  }

  getPubTypes(): PubType[] {
    return this.pubTypeList;
  }

  getFirstPubType(): PubType {
    return this.pubTypeList[0];
  }

  fetchAllPubTypes(): Observable<PubType[]> {
    return this.http.get<any[]>(`/api/publikacije/vrsta-publikacije/`).pipe(
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
    if (!pub)
      return this.domSanitizer.bypassSecurityTrustHtml('');
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

  uploadFile(pubId: number, file): Observable<any> {
    const formData = new FormData();
    formData.append(file.name, file);
    return this.http.post<any>(`/api/publikacije/save/pubfile/${pubId}/`, formData);
  }

  uploadFiles(pubId: number, files: any[]): Observable<any> {
    const formData = new FormData();
    for (const file of files) {
      formData.append(file.name, file);
    }
    return this.http.post<any>(`/api/publikacije/save/pubfile/${pubId}/`, formData);
  }

  deleteFiles(pubId: number, fileIds: number[]): Observable<any> {
    return this.http.post<any>(`/api/publikacije/delete/pubfile/${pubId}/`, fileIds);
  }

  reorderFiles(pubId: number, fileIds: number[]): Observable<any> {
    return this.http.post<any>(`/api/publikacije/reorder/pubfile/${pubId}/`, fileIds);
  }

  deleteTextsForPub(pubId: number): Observable<any> {
    return this.http.delete<any>(`/api/publikacije/delete/text/${pubId}/`);
  }

  extractTextFromFile(pubId: number, fileId: number): Observable<any> {
    return this.http.put<any>(`/api/publikacije/extract/${pubId}/file/${fileId}/`, {});
  }

  getFilterList(): Observable<any[]> {
    return this.http.get<any[]>('/api/publikacije/svi-filteri/');
  }

  saveFilters(pubId: number, filters: any[]): Observable<any> {
    return this.http.put<any>(`/api/publikacije/save/filters/${pubId}/`, filters);
  }

  applyFilters(pubId: number): Observable<any> {
    return this.http.put<any[]>(`/api/publikacije/primeni-filtere/${pubId}/`, {});
  }
}
