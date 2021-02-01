import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MessageService } from 'primeng/api';
import { ImenicaService } from '../../services/imenica/imenica.service';
import { Imenica } from '../../models/imenica';

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
  editMode: boolean;
  saveBtnDisabled: boolean;
  imenica: Imenica;

  constructor(private messageService: MessageService, private httpClient: HttpClient, private imenicaService: ImenicaService) {
    this.wordTypes = [
      {name:'именица'},
      {name:'глагол'},
      {name:'придев'},
      {name:'заменица'},
      {name:'број'},
      {name:'прилог'},
      {name:'предлог'},
      {name:'узвик'},
      {name:'речца'},
      {name:'везник'}
    ];
   }

  ngOnInit(): void {
    this.saveBtnDisabled = true;
    if (window.location.href.endsWith('/add')) {
      this.selectedWordType = {name:''};
      this.editMode = false;
    }
    else { // TODO getWord
      this.selectedWordType = {name:'именица'}; // test case
      this.editMode = true;
    }
  }

  save(wordType: string): void {
    switch (wordType) {
      case 'именица':
        this.saveImenica();
        break;
      case 'глагол':
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

  imenicaChangedHandler(imenica: any): void {
    this.saveBtnDisabled = false;
    this.imenica = imenica;
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

  back(): void {
    window.history.back();
  }

  onChange(): void {
    this.saveBtnDisabled = true;
  }
}
