import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MessageService } from 'primeng/api';
import { ImenicaService } from '../../services/imenica/imenica.service';
import { GlagolService } from '../../services/glagol/glagol.service';
import { Imenica } from '../../models/imenica';
import { Glagol } from '../../models/glagol';

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

  constructor(private messageService: MessageService, private httpClient: HttpClient,
    private imenicaService: ImenicaService, private glagolService: GlagolService) {
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
        break;
      case 'заменица':
        break;
      case 'број':
        break;
      case 'прилог':
        break;
      case 'предлог':
        break;
      case 'узвик':
        break;
      case 'речца':
        break;
      case 'везник':
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
        this.messageService.add({severity:'success', summary: 'Сачувано', detail: 'Именица је измењена'});
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

  back(): void {
    window.history.back();
  }

  onChange(): void {
    this.saveBtnDisabled = true;
  }
}
