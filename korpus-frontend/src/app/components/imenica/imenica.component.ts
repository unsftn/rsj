import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { MessageService } from 'primeng/api';

interface NounType {
  name: string;
  id: number;
}

interface Variant {
  nomjed: string;
  genjed: string;
  datjed: string;
  akujed: string;
  vokjed: string;
  insjed: string;
  lokjed: string;
  nommno: string;
  genmno: string;
  datmno: string;
  akumno: string;
  vokmno: string;
  insmno: string;
  lokmno: string;
}

@Component({
  selector: 'imenica',
  templateUrl: './imenica.component.html',
  styleUrls: ['./imenica.component.scss'],
  providers: [MessageService]
})
export class ImenicaComponent implements OnInit {

  nounTypes: NounType[];
  selectedNounType: NounType = {name:'', id:0};
  variants: Variant[];
  word: any;
  wordURL: string;

  constructor(private messageService: MessageService, private httpClient: HttpClient) {
    this.nounTypes = [
      {name:'апстрактна', id:1},
      {name:'заједничка', id:2},
      {name:'властита', id:3},
      {name:'збирна', id:4},
      {name:'градивна', id:5},
      {name:'глаголска', id:6}
    ];
  }

  ngOnInit(): void {
    this.variants = new Array<Variant>();
    if (window.location.href.endsWith('/rec'))
      this.word = {
        vrsta_id: 0,
        nomjed: '',
        genjed: '',
        datjed: '',
        akujed: '',
        vokjed: '',
        insjed: '',
        lokjed: '',
        nommno: '',
        genmno: '',
        datmno: '',
        akumno: '',
        vokmno: '',
        insmno: '',
        lokmno: ''
      }
    else {
      this.wordURL = window.location.href.split('/').slice(-1)[0];
      this.getImenicaByNomJed();
      this.word = { // test case
        vrsta_id: 2,
        nomjed: 'тест',
        genjed: 'теста',
        datjed: 'тесту',
        akujed: 'тест',
        vokjed: 'тесте',
        insjed: 'тестом',
        lokjed: 'тесту',
        nommno: 'тестови',
        genmno: 'тестова',
        datmno: 'тестовима',
        akumno: 'тестове',
        vokmno: 'тестови',
        insmno: 'тестовима',
        lokmno: 'тестовима',
        version: 1
      }
      this.selectedNounType = this.nounTypes.find(type => type.id === this.word.vrsta_id);
    }
  }

  addVariant(): void {
    this.variants.push({
      nomjed: '',
      genjed: '',
      datjed: '',
      akujed: '',
      vokjed: '',
      insjed: '',
      lokjed: '',
      nommno: '',
      genmno: '',
      datmno: '',
      akumno: '',
      vokmno: '',
      insmno: '',
      lokmno: ''
    });
  }

  removeVariant(variant: Variant): void {
    this.variants.splice(this.variants.indexOf(variant), 1);
  }

  async getImenicaByNomJed() {
    let nomjed = decodeURIComponent(this.wordURL); // decode Cyrillic letters
    const response: any = await this.httpClient
      .get('api/korpus/imenica/', {
        params: new HttpParams().set('nomjed', nomjed)
      })
      .toPromise()
      .catch(() => {
        this.messageService.add({severity:'error', summary: 'Грешка', detail: 'Тражена реч није пронађена'});
      });

    if (response) {
      this.word = response.map((item) => { // TODO varijante
        return {
          vrsta_id: item.vrsta_id, nomjed: item.nomjed, genjed: item.genjed,
          datjed: item.datjed, akujed: item.akujed, vokjed: item.vokjed,
          insjed: item.insjed, lokjed: item.lokjed, nommno: item.nommno,
          genmno: item.genmno, datmno: item.datmno, akumno: item.akumno,
          vokmno: item.vokmno, insmno: item.insmno, lokmno: item.lokmno,
          version: item.version
        };
      });
    }
  }

  // TODO provera da li rec vec postoji
  async save() {
    this.word.vrsta_id = this.selectedNounType.id;
    this.word.varijante = this.variants;
    if (this.word.varijante == 0)
      delete this.word.varijante;

    const response: any = await this.httpClient
      .post('api/korpus/save-imenica/', this.word)
      .toPromise()
      .catch(() => {
        this.messageService.add({severity:'error', summary: 'Грешка', detail: 'Попуните сва поља'});
      });
    if (response) {
      this.messageService.add({severity:'success', summary: 'Сачувано', detail: 'Именица је сачувана'});
      setTimeout(() => {
        window.history.back();
      }, 2000);
    }
  }
}
