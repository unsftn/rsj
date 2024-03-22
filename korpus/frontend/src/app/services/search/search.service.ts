/* tslint:disable:variable-name */
import { HttpClient } from '@angular/common/http';
import { EventEmitter, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SearchService {

  private _selectedWordId: number;
  private _selectedWordType: number;
  private _selectedWordForm: string;
  private _selectedWordChanged: EventEmitter<boolean> = new EventEmitter<boolean>();

  constructor(private http: HttpClient) { }

  public get selectedWordChanged(): EventEmitter<boolean> {
    return this._selectedWordChanged;
  }

  public get selectedWordId(): number {
    return this._selectedWordId;
  }

  public get selectedWordType(): number {
    return this._selectedWordType;
  }

  public get selectedWordForm(): string {
    return this._selectedWordForm;
  }

  public set selectedWordId(value: number) {
    this._selectedWordId = value;
  }

  public set selectedWordType(value: number) {
    this._selectedWordType = value;
  }

  public set selectedWordForm(value: string) {
    this._selectedWordForm = value;
  }

  public clear(): void {
    this._selectedWordId = null;
    this._selectedWordType = null;
    this._selectedWordForm = null;
  }

  searchWords(query: string): Observable<any> {
    return this.http.get<any>(`/api/pretraga/reci/?q=${query}`);
  }

  searchSuffix(query: string): Observable<any> {
    return this.http.get<any>(`/api/pretraga/sufiks/?q=${query}`);
  }

  searchPubs(wordId: number, wordType: number, fragmentSize: number, scanner: string): Observable<any[]> {
    return this.http.get<any[]>(`/api/pretraga/publikacije/?w=${wordId}&t=${wordType}&f=${fragmentSize}&s=${scanner}`);
  }

  searchForms(query: string, fragmentSize: number, scanner: string, caseSensitive: boolean): Observable<any> {
    return this.http.get<any>(`/api/pretraga/oblici/?q=${query}&f=${fragmentSize}&s=${scanner}&cs=${caseSensitive}`);
  }

  checkDupes(word: string, id: number): Observable<any> {
    let url = `/api/pretraga/duplikati/?w=${word}`;
    if (id)
      url += `&id=${id}`;
    return this.http.get<any>(url);
  }

  searchRecnik(word: string): Observable<any> {
    return this.http.get<any>(`/api/recnikproxy/search/?q=${word}`);
  }
}
