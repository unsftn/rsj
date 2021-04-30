import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map, shareReplay } from 'rxjs/operators';
import { Qualificator } from '../../models';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  obradjivaci: any[] = [];
  redaktori: any[] = [];
  urednici: any[] = [];
  administratori: any[] = [];

  constructor(private http: HttpClient) {}

  fetchKorisnici(): Observable<any[]> {
    this.obradjivaci = [];
    this.redaktori = [];
    this.urednici = [];
    this.administratori = [];
    return this.http.get<any[]>('/api/odrednice/korisnici/').pipe(
      map((users: any[]) => {
        return users.map((item) => {
          item.full_name = item.first_name + ' ' + item.last_name;
          this.obradjivaci.push(item);
          if (item.group === 2) {
            this.redaktori.push(item);
          }
          if (item.group === 3) {
            this.redaktori.push(item);
            this.urednici.push(item);
          }
          if (item.group === 4) {
            this.redaktori.push(item);
            this.urednici.push(item);
            this.administratori.push(item);
          }
        });
      }), shareReplay(1));
  }

  getObradjivaci(): any[] {
    return this.obradjivaci;
  }

  getRedaktori(): any[] {
    return this.redaktori;
  }

  getUrednici(): any[] {
    return this.urednici;
  }

  getAdministratori(): any[] {
    return this.administratori;
  }

  getUser(id: number): any {
    for (const usr of this.obradjivaci)
      if (usr.id === id)
        return usr;
    return null;
  }
}

