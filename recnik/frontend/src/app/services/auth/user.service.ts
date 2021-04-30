import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(private http: HttpClient) {}

  getObradjivaci(): Observable<any> {
    return this.http.get('/api/odrednice/korisnici/obradjivaci/');
  }

  getRedaktori(): Observable<any> {
    return this.http.get('/api/odrednice/korisnici/redaktori/');
  }

  getUrednici(): Observable<any> {
    return this.http.get('/api/odrednice/korisnici/urednici/');
  }

  getAdministratori(): Observable<any> {
    return this.http.get('/api/odrednice/korisnici/administratori/');
  }

  getKorisnik(id: number): Observable<any> {
    return this.http.get(`/api/odrednice/korisnici/${id}`);
  }
}

