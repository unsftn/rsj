import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Pridev, PridevskiVid } from '../../models/reci';

@Injectable({
  providedIn: 'root'
})
export class PridevService {

  vidovi: PridevskiVid[] = [
    {id: null, name: '---'},
    {id: 1, name: 'одређени'},
    {id: 2, name: 'неодређени'},
    {id: 3, name: 'компаратив'},
    {id: 4, name: 'суперлатив'},
  ];

  constructor(private http: HttpClient) { }

  new(): Pridev {
    return {
      vidovi: [
        { vid: 1,
          mnomjed: '', mgenjed: '', mdatjed: '', makujed: '', mvokjed: '', minsjed: '', mlokjed: '',
          mnommno: '', mgenmno: '', mdatmno: '', makumno: '', mvokmno: '', minsmno: '', mlokmno: '',
          znomjed: '', zgenjed: '', zdatjed: '', zakujed: '', zvokjed: '', zinsjed: '', zlokjed: '',
          znommno: '', zgenmno: '', zdatmno: '', zakumno: '', zvokmno: '', zinsmno: '', zlokmno: '',
          snomjed: '', sgenjed: '', sdatjed: '', sakujed: '', svokjed: '', sinsjed: '', slokjed: '',
          snommno: '', sgenmno: '', sdatmno: '', sakumno: '', svokmno: '', sinsmno: '', slokmno: ''
        },
        { vid: 2,
          mnomjed: '', mgenjed: '', mdatjed: '', makujed: '', mvokjed: '', minsjed: '', mlokjed: '',
          mnommno: '', mgenmno: '', mdatmno: '', makumno: '', mvokmno: '', minsmno: '', mlokmno: '',
          znomjed: '', zgenjed: '', zdatjed: '', zakujed: '', zvokjed: '', zinsjed: '', zlokjed: '',
          znommno: '', zgenmno: '', zdatmno: '', zakumno: '', zvokmno: '', zinsmno: '', zlokmno: '',
          snomjed: '', sgenjed: '', sdatjed: '', sakujed: '', svokjed: '', sinsjed: '', slokjed: '',
          snommno: '', sgenmno: '', sdatmno: '', sakumno: '', svokmno: '', sinsmno: '', slokmno: ''
        },
        { vid: 3,
          mnomjed: '', mgenjed: '', mdatjed: '', makujed: '', mvokjed: '', minsjed: '', mlokjed: '',
          mnommno: '', mgenmno: '', mdatmno: '', makumno: '', mvokmno: '', minsmno: '', mlokmno: '',
          znomjed: '', zgenjed: '', zdatjed: '', zakujed: '', zvokjed: '', zinsjed: '', zlokjed: '',
          znommno: '', zgenmno: '', zdatmno: '', zakumno: '', zvokmno: '', zinsmno: '', zlokmno: '',
          snomjed: '', sgenjed: '', sdatjed: '', sakujed: '', svokjed: '', sinsjed: '', slokjed: '',
          snommno: '', sgenmno: '', sdatmno: '', sakumno: '', svokmno: '', sinsmno: '', slokmno: ''
        },
        { vid: 4,
          mnomjed: '', mgenjed: '', mdatjed: '', makujed: '', mvokjed: '', minsjed: '', mlokjed: '',
          mnommno: '', mgenmno: '', mdatmno: '', makumno: '', mvokmno: '', minsmno: '', mlokmno: '',
          znomjed: '', zgenjed: '', zdatjed: '', zakujed: '', zvokjed: '', zinsjed: '', zlokjed: '',
          znommno: '', zgenmno: '', zdatmno: '', zakumno: '', zvokmno: '', zinsmno: '', zlokmno: '',
          snomjed: '', sgenjed: '', sdatjed: '', sakujed: '', svokjed: '', sinsjed: '', slokjed: '',
          snommno: '', sgenmno: '', sdatmno: '', sakumno: '', svokmno: '', sinsmno: '', slokmno: ''
        },
      ]
    };
  }

  get(id: number): Observable<any> {
    return this.http.get<any>(`/api/reci/pridevi/${id}/`);
  }

  add(pridev: Pridev): Observable<any> {
    return this.http.post<any>(`/api/reci/save/pridev/`, pridev);
  }

  update(pridev: Pridev): Observable<any> {
    return this.http.put<any>(`/api/reci/save/pridev/`, pridev);
  }

  getVidovi(): PridevskiVid[] {
    return this.vidovi;
  }
}
