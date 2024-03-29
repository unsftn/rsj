import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Pridev, VarijantaPrideva } from '../../models/reci';

@Injectable({
  providedIn: 'root'
})
export class PridevService {

  constructor(private http: HttpClient) { }

  new(): Pridev {
    return {
      dvaVida: true,
      varijante: [],
      monomjed: '',
      mogenjed: '',
      modatjed: '',
      moakujed: '',
      movokjed: '',
      moinsjed: '',
      molokjed: '',
      monommno: '',
      mogenmno: '',
      modatmno: '',
      moakumno: '',
      movokmno: '',
      moinsmno: '',
      molokmno: '',
      mnnomjed: '',
      mngenjed: '',
      mndatjed: '',
      mnakujed: '',
      mnvokjed: '',
      mninsjed: '',
      mnlokjed: '',
      mnnommno: '',
      mngenmno: '',
      mndatmno: '',
      mnakumno: '',
      mnvokmno: '',
      mninsmno: '',
      mnlokmno: '',
      mknomjed: '',
      mkgenjed: '',
      mkdatjed: '',
      mkakujed: '',
      mkvokjed: '',
      mkinsjed: '',
      mklokjed: '',
      mknommno: '',
      mkgenmno: '',
      mkdatmno: '',
      mkakumno: '',
      mkvokmno: '',
      mkinsmno: '',
      mklokmno: '',
      msnomjed: '',
      msgenjed: '',
      msdatjed: '',
      msakujed: '',
      msvokjed: '',
      msinsjed: '',
      mslokjed: '',
      msnommno: '',
      msgenmno: '',
      msdatmno: '',
      msakumno: '',
      msvokmno: '',
      msinsmno: '',
      mslokmno: '',
      zpnomjed: '',
      zpgenjed: '',
      zpdatjed: '',
      zpakujed: '',
      zpvokjed: '',
      zpinsjed: '',
      zplokjed: '',
      zpnommno: '',
      zpgenmno: '',
      zpdatmno: '',
      zpakumno: '',
      zpvokmno: '',
      zpinsmno: '',
      zplokmno: '',
      zknomjed: '',
      zkgenjed: '',
      zkdatjed: '',
      zkakujed: '',
      zkvokjed: '',
      zkinsjed: '',
      zklokjed: '',
      zknommno: '',
      zkgenmno: '',
      zkdatmno: '',
      zkakumno: '',
      zkvokmno: '',
      zkinsmno: '',
      zklokmno: '',
      zsnomjed: '',
      zsgenjed: '',
      zsdatjed: '',
      zsakujed: '',
      zsvokjed: '',
      zsinsjed: '',
      zslokjed: '',
      zsnommno: '',
      zsgenmno: '',
      zsdatmno: '',
      zsakumno: '',
      zsvokmno: '',
      zsinsmno: '',
      zslokmno: '',
      spnomjed: '',
      spgenjed: '',
      spdatjed: '',
      spakujed: '',
      spvokjed: '',
      spinsjed: '',
      splokjed: '',
      spnommno: '',
      spgenmno: '',
      spdatmno: '',
      spakumno: '',
      spvokmno: '',
      spinsmno: '',
      splokmno: '',
      sknomjed: '',
      skgenjed: '',
      skdatjed: '',
      skakujed: '',
      skvokjed: '',
      skinsjed: '',
      sklokjed: '',
      sknommno: '',
      skgenmno: '',
      skdatmno: '',
      skakumno: '',
      skvokmno: '',
      skinsmno: '',
      sklokmno: '',
      ssnomjed: '',
      ssgenjed: '',
      ssdatjed: '',
      ssakujed: '',
      ssvokjed: '',
      ssinsjed: '',
      sslokjed: '',
      ssnommno: '',
      ssgenmno: '',
      ssdatmno: '',
      ssakumno: '',
      ssvokmno: '',
      ssinsmno: '',
      sslokmno: '',
    };
  }

  newVarijanta(rod: number, redni_broj: number): VarijantaPrideva {
    return {
      rod: rod,
      redni_broj: redni_broj,
      onomjed: '',
      ogenjed: '',
      odatjed: '',
      oakujed: '',
      ovokjed: '',
      oinsjed: '',
      olokjed: '',
      nnomjed: '',
      ngenjed: '',
      ndatjed: '',
      nakujed: '',
      nvokjed: '',
      ninsjed: '',
      nlokjed: '',
      pnomjed: '',
      pgenjed: '',
      pdatjed: '',
      pakujed: '',
      pvokjed: '',
      pinsjed: '',
      plokjed: '',
      knomjed: '',
      kgenjed: '',
      kdatjed: '',
      kakujed: '',
      kvokjed: '',
      kinsjed: '',
      klokjed: '',
      snomjed: '',
      sgenjed: '',
      sdatjed: '',
      sakujed: '',
      svokjed: '',
      sinsjed: '',
      slokjed: '',
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
}
