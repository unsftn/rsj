import { Component, OnInit, AfterViewInit, Input, Output, EventEmitter } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MessageService } from 'primeng/api';
import { Imenica } from '../../models/imenica';
import { ImenicaVarijanta } from '../../models/imenicaVarijanta';
import { ImenicaService } from '../../services/imenica/imenica.service';

interface NounType {
  name: string;
  id: number;
}

@Component({
  selector: 'imenica',
  templateUrl: './imenica.component.html',
  styleUrls: ['./imenica.component.scss'],
  providers: [MessageService]
})
export class ImenicaComponent implements OnInit, AfterViewInit {

  @Input() imenica: Imenica;

  @Output() imenicaChanged: EventEmitter<Imenica> = new EventEmitter();

  nounTypes: NounType[];
  selectedNounType: NounType;
  variants: ImenicaVarijanta[];
  id: number;

  constructor(private messageService: MessageService, private imenicaService: ImenicaService, private route: ActivatedRoute) {
    this.nounTypes = [
      { id: 1, name: 'апстрактна' },
      { id: 2, name: 'заједничка' },
      { id: 3, name: 'властита' },
      { id: 4, name: 'збирна' },
      { id: 5, name: 'градивна' },
      { id: 6, name: 'глаголска' }
    ];
    this.selectedNounType = { id:0, name:'' };
  }

  ngOnInit(): void {
    if (window.location.href.endsWith('/add'))
      this.imenica = {
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
        lokmno: '',
        varijante: new Array<ImenicaVarijanta>()
      };
    else {
      this.route.params.subscribe((params) => {
        this.id = +params.id;
      });
      this.getImenicaById();
      this.imenica = { // test case, delete if getting data from the server
        id: this.id,
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
        vrsta: { id: 2, naziv: 'заједничка' },
        version: 1,
        varijante: [
          {
            id: 1,
            imenica_id: this.id,
            redni_broj: 1,
            nomjed: '',
            genjed: '',
            datjed: '',
            akujed: '',
            vokjed: 'тесту',
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
        ]
      };
      this.selectedNounType = this.nounTypes.find(type => type.id === this.imenica.vrsta.id);
      delete this.imenica.vrsta;
    }
    this.variants = this.imenica.varijante;
    if (this.variants.length > 0)
      this.alignVariantForms();
  }

  ngAfterViewInit(): void {
    this.alignVariantForms();
  }

  addVariant(): void {
    this.variants.push(
      {
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
    );
    this.alignVariantForms();
  }

  removeVariant(variant: ImenicaVarijanta): void {
    this.variants.splice(this.variants.indexOf(variant), 1);
    this.changeImenica();
  }

  changeImenica(): void {
    this.imenica.vrsta_id = this.selectedNounType.id;
    this.imenica.varijante = this.variants;
    this.imenicaChanged.emit(this.imenica);
  }

  async getImenicaById() {
    const response: any = await this.imenicaService.getImenica(this.id)
      .toPromise()
      .catch(() => {
        this.messageService.add({severity:'error', summary: 'Грешка', detail: 'Тражена именица није пронађена'});
      });
    if (response) {
      this.imenica = response.map((item: Imenica) => {
        return {
          vrsta_id: item.vrsta.id, nomjed: item.nomjed, genjed: item.genjed,
          datjed: item.datjed, akujed: item.akujed, vokjed: item.vokjed,
          insjed: item.insjed, lokjed: item.lokjed, nommno: item.nommno,
          genmno: item.genmno, datmno: item.datmno, akumno: item.akumno,
          vokmno: item.vokmno, insmno: item.insmno, lokmno: item.lokmno,
          version: item.version, id: item.id, varijante: item.varijantaimenice_set
        };
      });
    }
  }

  async getImenicaByNomJed() {
    let nomjed = decodeURIComponent(this.imenica.nomjed); // decode Cyrillic letters
    const response: any = await this.imenicaService.getImenicaByNomJed(nomjed)
      .toPromise()
      .catch(() => {
        this.messageService.add({severity:'error', summary: 'Грешка', detail: 'Тражена именица није пронађена'});
      });
    if (response) {
      this.imenica = response.map((item: Imenica) => {
        return {
          vrsta_id: item.vrsta.id, nomjed: item.nomjed, genjed: item.genjed,
          datjed: item.datjed, akujed: item.akujed, vokjed: item.vokjed,
          insjed: item.insjed, lokjed: item.lokjed, nommno: item.nommno,
          genmno: item.genmno, datmno: item.datmno, akumno: item.akumno,
          vokmno: item.vokmno, insmno: item.insmno, lokmno: item.lokmno,
          version: item.version, id: item.id, varijante: item.varijantaimenice_set
        };
      });
    }
  }

  alignVariantForms(): void {
    setTimeout(() => {
      const divs = document.getElementsByClassName('p-d-flex p-flex-wrap p-col-8 ng-star-inserted');
      let variantDiv: Element;
      for (let i=1; i<divs.length; i++) {
        variantDiv = divs[i];
        variantDiv.className = 'p-d-flex p-flex-wrap p-col-12 ng-star-inserted';
      }
    }, 0);
  }
}
