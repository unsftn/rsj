import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';
import { PrimeNGConfig } from 'primeng/api';
import { Determinant } from '../../models/determinant';
import { OdrednicaService } from '../../services/odrednice/odrednica.service';

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
  selector: 'tabForm',
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
  message: string;
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
  selectedQualificators: [];
  id: number;

  meanings: any[];

  addVariant() {
    this.variants.push({ nameE: '', nameI: '' });
  }

  removeVariant(variant) {
    this.variants.splice(this.variants.indexOf(variant), 1);
  }

  selectedKindChangedHandler(selectedKind) {
    this.selectedKind = selectedKind;
  }

  selectedVerbKindChangedHandler(selectedVerbKind) {
    this.selectedVerbKind = selectedVerbKind;
  }

  selectedVerbFormChangedHandler(selectedVerbForm) {
    this.selectedVerbForm = selectedVerbForm;
  }

  extensionChangedHandler(extension) {
    this.extension = extension;
  }

  presentChangedHandler(present) {
    this.present = present;
  }

  detailsChangedHandler(details) {
    this.details = details;
  }

  collocationsChangedHandler(collocations) {
    this.collocations = collocations;
  }

  selectedQualificatorsHandler(qualificators) {
    this.selectedQualificators = qualificators;
  }

  constructor(
    private primengConfig: PrimeNGConfig,
    private httpClient: HttpClient,
    private route: ActivatedRoute,
    private odrednicaService: OdrednicaService,
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

  async addNewDeterminant(): Promise<void> {
    const response: any = await this.odrednicaService
      .saveOdrednica(this.makeNewDeterminant())
      .toPromise()
      .catch(() => {
        this.message =
          'Није могуће додати нову одредницу. Унесите све потребне податке.';
        this.display = true;
      });

    if (response) {
      this.message = 'Успешно додата нова одредница';
      this.display = true;
    }
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
        this.isVerb = true;
        this.isNoun = false;
        break;
      case 'Глагол':
        this.isVerb = false;
        this.isNoun = true;
        break;
    }
  }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
    this.route.data.subscribe((data) => {
      switch (data.mode) {
        case 'add':
          this.id = null;
          console.log('unos nove odrednice');
          break;
        case 'edit':
          this.route.params.subscribe((params) => {
            this.id = +params.id;
            console.log('obrada postojece odrednice', this.id);
            this.odrednicaService.getOdrednica(this.id).subscribe((value) => {
              this.fillForm(value);
            });
          });
          break;
      }
    });
  }

  makeNewDeterminant(): Determinant {
    const determinant: Determinant = {
      rec: this.wordE,
      ijekavski: this.wordI,
      vrsta: this.selectedWordType?.id,
      rod: this.selectedKind?.id ? this.selectedKind?.id : null,
      nastavak: this.extension ? this.extension : '',
      info: this.details ? this.details : '',
      glagolski_vid: this.selectedVerbForm?.id ? this.selectedVerbForm?.id : 0,
      glagolski_rod: this.selectedVerbKind?.id ? this.selectedVerbKind?.id : 0,
      prezent: this.present ? this.present : '',
      broj_pregleda: 0,
      stanje: this.selectedState?.id ? this.selectedState?.id : 1,
      version: 1,
      kolokacija_set: this.collocations ? this.collocations : [],
      kvalifikatorodrednice_set: this.selectedQualificators
        ? this.selectedQualificators
        : [],
    };
    if (this.id !== null) {
      determinant.id = this.id;
    }
    console.log(determinant);
    return determinant;
  }

  fillForm(value: any): void {
    console.log(value);
    this.wordE = value.rec;
    this.wordI = value.ijekavski;
    for (let v of value.varijantaodrednice_set) {
      this.variants.push({ nameE: v.tekst, nameI: v.ijekavski });
    }
    this.selectedWordType = this.wordType[value.vrsta];
    switch (value.vrsta) {
      case 0:
      case 2:
      case 5:
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
    for (let z of value.znacenje_set) {
      let obj = { value: z.tekst, submeanings: [] };
      for (let pz of z.podznacenje_set) {
        obj.submeanings.push({ value: pz.tekst });
      }
      this.meanings.push(obj);
    }
  }
}
