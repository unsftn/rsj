import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { ActivatedRoute } from '@angular/router';
import { PrimeNGConfig } from 'primeng/api';
import { Determinant } from '../../models/determinant';
import { Qualificator } from '../../models/qualificator';
import { OdrednicaService, PreviewService, QualificatorService } from '../../services/odrednice';

interface State {
  name: string;
  id: number;
}

interface WordType {
  name: string;
  id: number;
}

interface Variant {
  nameE: string;
  nameI: string;
}

@Component({
  selector: 'tab-form',
  templateUrl: './tabForm.component.html',
  styleUrls: ['./tabForm.component.scss'],
})
export class TabFormComponent implements OnInit {
  wordType: WordType[];
  state: State[];
  isNoun: boolean;
  isVerb: boolean;
  wordE: string;
  wordI: string;
  display = false;
  message: SafeHtml;
  selectedKind;
  extension;
  variants: Variant[];

  selectedVerbKind;
  selectedVerbForm;
  present: string;
  details;
  collocations;

  selectedWordType: WordType;
  selectedState: State;
  qualificators: Qualificator[];
  id: number;

  meanings: any[] = [];
  expressions: any[] = [];

  addVariant(): void {
    this.variants.push({ nameE: '', nameI: '' });
  }

  removeVariant(variant): void {
    this.variants.splice(this.variants.indexOf(variant), 1);
  }

  selectedKindChangedHandler(selectedKind): void {
    this.selectedKind = selectedKind;
  }

  selectedVerbKindChangedHandler(selectedVerbKind): void {
    this.selectedVerbKind = selectedVerbKind;
  }

  selectedVerbFormChangedHandler(selectedVerbForm): void {
    this.selectedVerbForm = selectedVerbForm;
  }

  extensionChangedHandler(extension): void {
    this.extension = extension;
  }

  presentChangedHandler(present): void {
    this.present = present;
  }

  detailsChangedHandler(details): void {
    this.details = details;
  }

  collocationsChangedHandler(collocations): void {
    this.collocations = collocations;
  }

  selectedQualificatorsHandler(qualificators): void {
    this.qualificators = qualificators;
  }

  constructor(
    private primengConfig: PrimeNGConfig,
    private httpClient: HttpClient,
    private route: ActivatedRoute,
    private odrednicaService: OdrednicaService,
    private previewService: PreviewService,
    private qualificatorService: QualificatorService,
    private domSanitizer: DomSanitizer,
  ) {
    this.wordType = [
      { name: 'Именица', id: 0 },
      { name: 'Глагол', id: 1 },
      { name: 'Придев', id: 2 },
      { name: 'Прилог', id: 3 },
      { name: 'Предлог', id: 4 },
      { name: 'Заменица', id: 5 },
      { name: 'Узвик', id: 6 },
      { name: 'Речца', id: 7 },
      { name: 'Везник', id: 8 },
      { name: 'Број', id: 9 },
    ];
    this.state = [
      { name: 'Први унос', id: 1 },
      { name: 'Редактура 1', id: 2 },
      { name: 'Редактура 2', id: 3 },
    ];

    this.variants = [];

    this.isNoun = true;
    this.isVerb = false;
  }

  async save(): Promise<void> {
    const response: any = await this.odrednicaService
      .saveOdrednica(this.makeNewDeterminant())
      .toPromise()
      .catch((error) => {
        console.log(error);
        this.message = this.domSanitizer.bypassSecurityTrustHtml(
          '<p>Није могуће додати нову одредницу. Унесите све потребне податке.</p>');
        this.display = true;
      });

    if (response) {
      this.message = this.domSanitizer.bypassSecurityTrustHtml(
        '<p>Успешно додата нова одредница.</p>');
      this.display = true;
    }
  }

  preview(): void {
    const tekst = this.previewService.preview(this.makeNewDeterminant());
    this.message = this.domSanitizer.bypassSecurityTrustHtml(tekst);
    this.display = true;
  }

  onChange(): void {
    switch (this.selectedWordType.name) {
      case 'Прилог':
      case 'Узвик':
      case 'Речца':
      case 'Везник':
      case 'Предлог':
        this.isVerb = false;
        this.isNoun = false;
        break;
      case 'Именица':
      case 'Заменица':
      case 'Придев':
      case 'Број':
        this.isVerb = false;
        this.isNoun = true;
        break;
      case 'Глагол':
        this.isVerb = true;
        this.isNoun = false;
        break;
    }
  }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
    this.route.data.subscribe((data) => {
      switch (data.mode) {
        case 'add':
          this.id = null;
          break;
        case 'edit':
          this.route.params.subscribe((params) => {
            this.id = +params.id;
            this.odrednicaService.getOdrednica(this.id).subscribe((value) => {
              this.fillForm(value);
            });
          });
          break;
      }
    });
  }

  makeNewDeterminant(): Determinant {
    console.log(this.meanings);
    const determinant: Determinant = {
      rec: this.wordE,
      ijekavski: this.wordI,
      varijante: [],
      vrsta: this.selectedWordType?.id,
      rod: this.selectedKind?.id ? this.selectedKind?.id : null,
      nastavak: this.extension ? this.extension : '',
      info: this.details ? this.details : '',
      glagolski_vid: this.selectedVerbForm?.id ? this.selectedVerbForm?.id : 0,
      glagolski_rod: this.selectedVerbKind?.id ? this.selectedVerbKind?.id : 0,
      prezent: this.present ? this.present : '',
      stanje: this.selectedState?.id ? this.selectedState?.id : 1,
      version: 1, // TODO: sacuvaj prilikom edita postojece odrednice
      kolokacija_set: this.collocations ? this.collocations : [],
      kvalifikatori: this.qualificators.map((q, index) => {
        console.log(q);
        return {
          redni_broj: index + 1,
          kvalifikator_id: q.id,
          skracenica: q.abbreviation
        };
      }),
      znacenja: this.meanings ? this.meanings.map((z, index) => {
        return {
          redni_broj: index + 1,
          tekst: z.value,
          podznacenja: z.submeanings.map((pz, idx) => {
            return {
              redni_broj: idx + 1,
              tekst: pz.value,
              izrazi_fraze: pz.expressions.map((value, idx2) => {
                return {
                  redni_broj: idx2 + 1,
                  opis: value.value
                };
              }),
              kvalifikatori: pz.qualificators.map((q, idx2) => { return {
                  redni_broj: idx2 + 1,
                  kvalifikator_id: q.id,
                  skracenica: q.abbreviation
                };
              }),
            };
          }),
          izrazi_fraze: z.expressions.map((value, idx) => {
            return {
              redni_broj: idx + 1,
              opis: value.value
            };
          }),
          kvalifikatori: z.qualificators.map((q, idx) => { return {
              redni_broj: idx + 1,
              kvalifikator_id: q.id,
              skracenica: q.abbreviation
            };
          }),
          konkordanse: [],
        };
      }) : [],
    };
    if (this.id !== null) {
      determinant.id = this.id;
    }
    console.log('Sastavljeno za server:');
    console.log(determinant);
    return determinant;
  }

  fillForm(value: any): void {
    console.log('Procitano sa servera:');
    console.log(value);
    this.wordE = value.rec;
    this.wordI = value.ijekavski;
    for (const v of value.varijantaodrednice_set) {
      this.variants.push({ nameE: v.tekst, nameI: v.ijekavski });
    }
    this.selectedWordType = this.wordType[value.vrsta];
    switch (value.vrsta) {
      case 0:
        this.selectedKind = value.rod;
      case 5:
      case 2:
      case 9:
        this.isNoun = true;
        this.isVerb = false;
        break;
      case 1:
        this.isNoun = false;
        this.isVerb = true;
        break;
      default:
        this.isNoun = false;
        this.isVerb = false;
        break;
    }
    this.details = value.info === null ? '' : value.info;
    this.meanings = [];
    for (const z of value.znacenje_set) {
      const obj = {
        value: z.tekst,
        submeanings: [],
        expressions: z.izrazfraza_set.map((e) => { return { value: e.opis, keywords: [] }; }),
        qualificators: z.kvalifikatorznacenja_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id)),
      };
      for (const pz of z.podznacenje_set) {
        const submeaning = { value: pz.tekst, expressions: [], qualificators: [] };
        obj.submeanings.push(submeaning);
        for (const expr of pz.izrazfraza_set) {
          submeaning.expressions.push({ value: expr.opis, keywords: []});
        }
        pz.qualificators = pz.kvalifikatorpodznacenja_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id));
      }
      // for (const expr of z.izrazfraza_set) {
      //   obj.expressions.push({ value: expr.opis, keywords: [] });
      // }
      // obj.qualificators = z.kvalifikatorznacenja_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id));
      this.meanings.push(obj);
    }
    this.expressions = [];
    for (const expr of value.izrazfraza_set) {
      this.expressions.push({ value: expr.opis, keywords: [] });
    }
    this.qualificators = value.kvalifikatorodrednice_set.map((q) => this.qualificatorService.getQualificator(q.kvalifikator_id));
  }
}
