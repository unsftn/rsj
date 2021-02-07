import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Qualificator } from '../../models/qualificator';
import { map, shareReplay } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class QualificatorService {
  qualificatorCache: { [key: number]: Qualificator; } = {};
  qualificatorList: Qualificator[] = [];

  constructor(private httpClient: HttpClient) { }

  fetchAllQualificators(): Observable<Qualificator[]> {
    return this.httpClient.get<any[]>('/api/odrednice/kvalifikator/').pipe(
      map((qualificators: any[]) => {
        return qualificators.map((item) => {
          const q = { name: item.naziv, abbreviation: item.skracenica, id: item.id };
          this.qualificatorCache[q.id] = q;
          this.qualificatorList.push(q);
          return q;
        });
      }), shareReplay(1));
  }

  getQualificator(id: number): Qualificator {
    return this.qualificatorCache[id];
  }

  getAllQualificators(): Qualificator[] {
    return this.qualificatorList;
  }
}
