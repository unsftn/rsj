import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Glagol, GlagolskaVarijanta, GlagolskiRod, GlagolskiVid } from '../../models/reci';

@Injectable({
  providedIn: 'root'
})
export class GlagolService {

  rodovi: GlagolskiRod[] = [
    {id: null, name: '---'},
    {id: 1, name: 'прелазни'},
    {id: 2, name: 'непрелазни'},
    {id: 3, name: 'повратни'},
    {id: 4, name: 'прелазни и непрелазни'},
    {id: 5, name: 'непрелазни и прелазни'},
    {id: 6, name: 'прелазни (непрелазни)'},
    {id: 7, name: 'непрелазни (прелазни)'},
  ];

  vidovi: GlagolskiVid[] = [
    {id: null, name: '---'},
    {id: 1, name: 'свршени'},
    {id: 2, name: 'несвршени'},
    {id: 3, name: 'свршени и несвршени'},
    {id: 4, name: 'несвршени и свршени'},
    {id: 5, name: 'свршени (несвршени)'},
    {id: 6, name: 'несвршени (свршени)'},
  ];

  varijante: GlagolskaVarijanta[] = [
    {id: null, name: '---'},
    {id: 1, name: 'пр.л.јед.'},
    {id: 2, name: 'др.л.јед.'},
    {id: 3, name: 'тр.л.јед.'},
    {id: 4, name: 'пр.л.мн.'},
    {id: 5, name: 'др.л.мн.'},
    {id: 6, name: 'тр.л.мн.'},
  ];

  constructor(private http: HttpClient) { }

  new(): Glagol {
    return {
      infinitiv: '',
      gl_rod: null,
      gl_vid: null,
      rgp_mj: '',
      rgp_zj: '',
      rgp_sj: '',
      rgp_mm: '',
      rgp_zm: '',
      rgp_sm: '',
      gpp: '',
      gps: '',
      gpp2: '',
      oblici: [
        { vreme: 1, jd1: '', jd2: '', jd3: '', mn1: '', mn2: '', mn3: '', varijante: [] },
        { vreme: 2, jd1: '', jd2: '', jd3: '', mn1: '', mn2: '', mn3: '', varijante: [] },
        { vreme: 3, jd1: '', jd2: '', jd3: '', mn1: '', mn2: '', mn3: '', varijante: [] },
        { vreme: 4, jd1: '', jd2: '', jd3: '', mn1: '', mn2: '', mn3: '', varijante: [] },
        { vreme: 5, jd1: '', jd2: '', jd3: '', mn1: '', mn2: '', mn3: '', varijante: [] },
      ]
    };
  }

  get(id: number): Observable<any> {
    return this.http.get<any>(`/api/reci/glagoli/${id}/`);
  }

  add(glagol: Glagol): Observable<any> {
    return this.http.post<any>(`/api/reci/save/glagol/`, glagol);
  }

  update(glagol: Glagol): Observable<any> {
    return this.http.put<any>(`/api/reci/save/glagol/`, glagol);
  }

  getRodovi(): GlagolskiRod[] {
    return this.rodovi;
  }

  getVidovi(): GlagolskiVid[] {
    return this.vidovi;
  }

  getVarijante(): GlagolskaVarijanta[] {
    return this.varijante;
  }
}
