import { Component, OnInit } from '@angular/core';
import { MessageService } from 'primeng/api';
import { ImenicaService } from '../../services/imenica/imenica.service';
import { GlagolService } from '../../services/glagol/glagol.service';
import { PridevService } from '../../services/pridev/pridev.service';
import { PredlogService } from '../../services/predlog/predlog.service';
import { PrilogService } from '../../services/prilog/prilog.service';
import { ReccaService } from '../../services/recca/recca.service';
import { UzvikService } from '../../services/uzvik/uzvik.service';
import { VeznikService } from '../../services/veznik/veznik.service';
import { Imenica } from '../../models/imenica';
import { Glagol } from '../../models/glagol';
import { Pridev } from '../../models/pridev';
import { Predlog } from '../../models/predlog';
import { Prilog } from '../../models/prilog';
import { Recca } from '../../models/recca';
import { Uzvik } from '../../models/uzvik';
import { Veznik } from '../../models/veznik';

interface WordType {
  name: string;
}

@Component({
  selector: 'app-form-selector',
  templateUrl: './form-selector.component.html',
  styleUrls: ['./form-selector.component.scss']
})
export class FormSelectorComponent implements OnInit {

  wordTypes: WordType[];
  selectedWordType: WordType;
  wordTypesMap: any;
  editMode: boolean;
  saveBtnDisabled: boolean;
  imenica: Imenica;
  glagol: Glagol;
  pridev: Pridev;
  predlog: Predlog;
  prilog: Prilog;
  recca: Recca;
  uzvik: Uzvik;
  veznik: Veznik;

  constructor(private messageService: MessageService, private imenicaService: ImenicaService, private glagolService: GlagolService,
    private pridevService: PridevService, private predlogService: PredlogService, private prilogService: PrilogService,
    private reccaService: ReccaService, private uzvikService: UzvikService, private veznikService: VeznikService) {
    this.wordTypes = [
      { name: 'именица' },
      { name: 'глагол' },
      { name: 'придев' },
      { name: 'заменица' },
      { name: 'број' },
      { name: 'прилог' },
      { name: 'предлог' },
      { name: 'узвик' },
      { name: 'речца' },
      { name: 'везник' }
    ];
    this.wordTypesMap = {
      'imenica': 'именица',
      'glagol': 'глагол',
      'pridev': 'придев',
      'zamenica': 'заменица',
      'broj': 'број',
      'prilog': 'прилог',
      'predlog': 'предлог',
      'uzvik': 'узвик',
      'recca': 'речца',
      'veznik': 'везник'
    };
   }

  ngOnInit(): void {
    this.saveBtnDisabled = true;
    if (window.location.href.endsWith('/add')) {
      this.editMode = false;
      this.selectedWordType = {name:''};
    }
    else {
      this.editMode = true;
      let routes =  window.location.href.split('/');
      let type = routes[routes.length-2]; // https://www.rsj.rs/edit/imenica/1234 => imenica
      this.selectedWordType = {name: this.wordTypesMap[type]};
      for (let i=this.wordTypes.length-1; i>=0; i--) // prevent word type change
        if (this.wordTypes[i].name !== this.selectedWordType.name)
          this.wordTypes.splice(this.wordTypes.indexOf(this.wordTypes[i]), 1);
    }
  }

  save(wordType: string): void {
    switch (wordType) {
      case 'именица':
        this.saveImenica();
        break;
      case 'глагол':
        this.saveGlagol();
        break;
      case 'придев':
        this.savePridev();
        break;
      case 'заменица':
        break;
      case 'број':
        break;
      case 'прилог':
        this.savePrilog();
        break;
      case 'предлог':
        this.savePredlog();
        break;
      case 'узвик':
        this.saveUzvik();
        break;
      case 'речца':
        this.saveRecca();
        break;
      case 'везник':
        this.saveVeznik();
        break;
      default:
        break;
    }
  }

  async saveImenica() {
    if (this.imenica.varijante.length == 0)
      delete this.imenica.varijante;
    if (this.editMode) {
      const response: any = await this.imenicaService.editImenica(this.imenica)
        .toPromise()
        .catch(() => {
          this.messageService.add({severity:'error', summary: 'Грешка', detail: 'Попуните сва потребна поља'});
      });
      if (response) { // TODO 409 Conflict => refresh
        this.messageService.add({severity:'success', summary: 'Сачувано', detail: 'Именица је измењена'});
        setTimeout(() => {
          window.history.back();
        }, 2000);
      }
    }
    else {
      const response: any = await this.imenicaService.saveImenica(this.imenica)
        .toPromise()
        .catch(() => {
          this.messageService.add({severity:'error', summary: 'Грешка', detail: 'Попуните сва потребна поља'});
      });
      if (response) {
        this.messageService.add({severity:'success', summary: 'Сачувано', detail: 'Именица је сачувана'});
        setTimeout(() => {
          window.history.back();
        }, 2000);
      }
    }
  }

  async saveGlagol() {
    let glagol = this.glagol;
    if (glagol.rod == 3)
      glagol = this.handlePovratniGlagol(JSON.parse(JSON.stringify(glagol)));
    if (glagol.varijante.length == 0)
      delete glagol.varijante;
    if (this.editMode) {
      const response: any = await this.glagolService.editGlagol(glagol)
        .toPromise()
        .catch(() => {
          this.messageService.add({severity:'error', summary: 'Грешка', detail: 'Попуните сва потребна поља'});
      });
      if (response) { // TODO 409 Conflict => refresh
        this.messageService.add({severity:'success', summary: 'Сачувано', detail: 'Глагол је измењен'});
        setTimeout(() => {
          window.history.back();
        }, 2000);
      }
    }
    else {
      const response: any = await this.glagolService.saveGlagol(glagol)
        .toPromise()
        .catch(() => {
          this.messageService.add({severity:'error', summary: 'Грешка', detail: 'Попуните сва потребна поља'});
      });
      if (response) {
        this.messageService.add({severity:'success', summary: 'Сачувано', detail: 'Глагол је сачуван'});
        setTimeout(() => {
          window.history.back();
        }, 2000);
      }
    }
  }

  async savePridev() {
    if (this.pridev.tekst === '')
      this.pridev.tekst = this.pridev.oblici[0].tekst;
    if (this.editMode) {
      const response: any = await this.pridevService.editPridev(this.pridev)
        .toPromise()
        .catch(() => {
          this.messageService.add({severity:'error', summary: 'Грешка', detail: 'Попуните сва потребна поља'});
      });
      if (response) { // TODO 409 Conflict => refresh
        this.messageService.add({severity:'success', summary: 'Сачувано', detail: 'Придев је измењен'});
        setTimeout(() => {
          window.history.back();
        }, 2000);
      }
    }
    else {
      const response: any = await this.pridevService.savePridev(this.pridev)
        .toPromise()
        .catch(() => {
          this.messageService.add({severity:'error', summary: 'Грешка', detail: 'Попуните сва потребна поља'});
      });
      if (response) {
        this.messageService.add({severity:'success', summary: 'Сачувано', detail: 'Придев је сачуван'});
        setTimeout(() => {
          window.history.back();
        }, 2000);
      }
    }
  }

  async savePredlog() {
    if (this.editMode) {
      const response: any = await this.predlogService.editPredlog(this.predlog)
        .toPromise()
        .catch(() => {
          this.messageService.add({severity:'error', summary: 'Грешка', detail: 'Попуните сва потребна поља'});
      });
      if (response) { // TODO 409 Conflict => refresh
        this.messageService.add({severity:'success', summary: 'Сачувано', detail: 'Предлог је измењен'});
        setTimeout(() => {
          window.history.back();
        }, 2000);
      }
    }
    else {
      const response: any = await this.predlogService.savePredlog(this.predlog)
        .toPromise()
        .catch(() => {
          this.messageService.add({severity:'error', summary: 'Грешка', detail: 'Попуните сва потребна поља'});
      });
      if (response) {
        this.messageService.add({severity:'success', summary: 'Сачувано', detail: 'Предлог је сачуван'});
        setTimeout(() => {
          window.history.back();
        }, 2000);
      }
    }
  }

  async savePrilog() {
    if (this.editMode) {
      const response: any = await this.prilogService.editPrilog(this.prilog)
        .toPromise()
        .catch(() => {
          this.messageService.add({severity:'error', summary: 'Грешка', detail: 'Попуните сва потребна поља'});
      });
      if (response) { // TODO 409 Conflict => refresh
        this.messageService.add({severity:'success', summary: 'Сачувано', detail: 'Прилог је измењен'});
        setTimeout(() => {
          window.history.back();
        }, 2000);
      }
    }
    else {
      const response: any = await this.prilogService.savePrilog(this.prilog)
        .toPromise()
        .catch(() => {
          this.messageService.add({severity:'error', summary: 'Грешка', detail: 'Попуните сва потребна поља'});
      });
      if (response) {
        this.messageService.add({severity:'success', summary: 'Сачувано', detail: 'Прилог је сачуван'});
        setTimeout(() => {
          window.history.back();
        }, 2000);
      }
    }
  }

  async saveRecca() {
    if (this.editMode) {
      const response: any = await this.reccaService.editRecca(this.recca)
        .toPromise()
        .catch(() => {
          this.messageService.add({severity:'error', summary: 'Грешка', detail: 'Попуните сва потребна поља'});
      });
      if (response) { // TODO 409 Conflict => refresh
        this.messageService.add({severity:'success', summary: 'Сачувано', detail: 'Речца је измењена'});
        setTimeout(() => {
          window.history.back();
        }, 2000);
      }
    }
    else {
      const response: any = await this.reccaService.saveRecca(this.recca)
        .toPromise()
        .catch(() => {
          this.messageService.add({severity:'error', summary: 'Грешка', detail: 'Попуните сва потребна поља'});
      });
      if (response) {
        this.messageService.add({severity:'success', summary: 'Сачувано', detail: 'Речца је сачувана'});
        setTimeout(() => {
          window.history.back();
        }, 2000);
      }
    }
  }

  async saveUzvik() {
    if (this.editMode) {
      const response: any = await this.uzvikService.editUzvik(this.uzvik)
        .toPromise()
        .catch(() => {
          this.messageService.add({severity:'error', summary: 'Грешка', detail: 'Попуните сва потребна поља'});
      });
      if (response) { // TODO 409 Conflict => refresh
        this.messageService.add({severity:'success', summary: 'Сачувано', detail: 'Узвик је измењен'});
        setTimeout(() => {
          window.history.back();
        }, 2000);
      }
    }
    else {
      const response: any = await this.uzvikService.saveUzvik(this.uzvik)
        .toPromise()
        .catch(() => {
          this.messageService.add({severity:'error', summary: 'Грешка', detail: 'Попуните сва потребна поља'});
      });
      if (response) {
        this.messageService.add({severity:'success', summary: 'Сачувано', detail: 'Узвик је сачуван'});
        setTimeout(() => {
          window.history.back();
        }, 2000);
      }
    }
  }

  async saveVeznik() {
    if (this.editMode) {
      const response: any = await this.veznikService.editVeznik(this.veznik)
        .toPromise()
        .catch(() => {
          this.messageService.add({severity:'error', summary: 'Грешка', detail: 'Попуните сва потребна поља'});
      });
      if (response) { // TODO 409 Conflict => refresh
        this.messageService.add({severity:'success', summary: 'Сачувано', detail: 'Везник је измењен'});
        setTimeout(() => {
          window.history.back();
        }, 2000);
      }
    }
    else {
      const response: any = await this.veznikService.saveVeznik(this.veznik)
        .toPromise()
        .catch(() => {
          this.messageService.add({severity:'error', summary: 'Грешка', detail: 'Попуните сва потребна поља'});
      });
      if (response) {
        this.messageService.add({severity:'success', summary: 'Сачувано', detail: 'Везник је сачуван'});
        setTimeout(() => {
          window.history.back();
        }, 2000);
      }
    }
  }

  handlePovratniGlagol(glagol: Glagol): Glagol {
    let keys = ['infinitiv', 'rgp_mj', 'rgp_zj', 'rgp_sj', 'rgp_mm', 'rgp_zm', 'rgp_sm', 'gpp', 'gps'];
    for (const key in glagol)
      if (keys.includes(key) && glagol[key] !== '')
        glagol[key] = glagol[key] += ' се';
    for (let i=0; i<glagol.oblici.length; i++)
      for (const key in glagol.oblici[i])
        if (key !== 'vreme' && glagol.oblici[i][key] !== '')
          glagol.oblici[i][key] += ' се';
    keys = ['jd1', 'jd2', 'jd3', 'mn1', 'mn2', 'mn3'];
    for (let i=0; i<glagol.varijante.length; i++)
      for (const key in glagol.varijante[i])
        if (key !== 'vreme' && glagol.varijante[i][key] !== '')
          glagol.varijante[i][key] += ' се';
    return glagol;
  }

  imenicaChangedHandler(imenica: any): void {
    this.saveBtnDisabled = false;
    this.imenica = imenica;
  }

  glagolChangedHandler(glagol: any): void {
    this.saveBtnDisabled = false;
    this.glagol = glagol;
  }

  pridevChangedHandler(pridev: any): void {
    this.saveBtnDisabled = false;
    this.pridev = pridev;
  }

  predlogChangedHandler(predlog: any): void {
    this.saveBtnDisabled = false;
    this.predlog = predlog;
  }

  prilogChangedHandler(prilog: any): void {
    this.saveBtnDisabled = false;
    this.prilog = prilog;
  }

  reccaChangedHandler(recca: any): void {
    this.saveBtnDisabled = false;
    this.recca = recca;
  }

  uzvikChangedHandler(uzvik: any): void {
    this.saveBtnDisabled = false;
    this.uzvik = uzvik;
  }

  veznikChangedHandler(veznik: any): void {
    this.saveBtnDisabled = false;
    this.veznik = veznik;
  }

  back(): void {
    window.history.back();
  }

  onChange(): void {
    this.saveBtnDisabled = true;
  }
}
