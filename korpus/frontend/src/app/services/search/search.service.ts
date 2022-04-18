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

  public set selectedWordId(value: number) {
    this._selectedWordId = value;
  }

  public set selectedWordType(value: number) {
    this._selectedWordType = value;
  }

  searchWords(query: string): Observable<any> {
    return this.http.get<any>(`/api/pretraga/reci/?q=${query}`);
  }

  searchPubs(wordId: number, wordType: number): Observable<any[]> {
    return this.http.get<any[]>(`/api/pretraga/publikacije/?w=${wordId}&t=${wordType}`);
  }
}
