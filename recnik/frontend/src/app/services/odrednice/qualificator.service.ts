import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Qualificator } from '../../models/qualificator';
import { map, shareReplay } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class QualificatorService {

  constructor(private httpClient: HttpClient) { }

  getAllQualificators(): Observable<Qualificator[]> {
    return this.httpClient.get<any[]>('/api/odrednice/kvalifikator/').pipe(
      map((qualificators: any[]) => {
        return qualificators.map((item) => {
          return { name: item.naziv, abbreviation: item.skracenica, id: item.id };
        });
      }), shareReplay(1));
  }
}
