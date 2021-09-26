import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map, shareReplay } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class PodvrstaReciService {

  podvrstaCache: { [key: number]: any; } = {};
  podvrstaList: any[] = [];

  constructor(private httpClient: HttpClient) { }

  fetchAllPodvrsta(): Observable<any[]> {
    return this.httpClient.get<any[]>('/api/odrednice/podvrsta-reci/').pipe(
      map((podvrste: any[]) => {
        return podvrste.map((item) => {
          const q = { name: item.naziv, abbreviation: item.skracenica, id: item.id, wordType: item.vrsta };
          this.podvrstaCache[q.id] = q;
          this.podvrstaList.push(q);
          return q;
        });
      }), shareReplay(1));
  }

  getPodvrsta(id: number): any {
    return this.podvrstaCache[id];
  }

  getAllPodvrsta(): any[] {
    return this.podvrstaList;
  }

  getPodvrste(vrsta: number): any[] {
    return this.podvrstaList.filter((item) => item.wordType === vrsta);
  }
}
