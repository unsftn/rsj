import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

interface State {
  name: string;
  id: number;
}

interface WordType {
  name: string;
  id: number;
}

interface Qualificator {
  name: string;
  id: number;
}

@Component({
  selector: 'tabForm',
  templateUrl: './tabForm.component.html',
  styleUrls: ['./tabForm.component.scss'],
})
export class TabFormComponent implements OnInit {
  wordType: WordType[];
  state: State[];
  qualificators: Qualificator[];
  isNoun: boolean;
  isVerb: boolean;
  wordE: string;
  wordI: string;
  display = false;
  message: string;
  selectedKind;
  extension;

  selectedVerbKind;
  selectedVerbForm;
  present: string;
  details;
  collocations;

  selectedWordType: WordType;
  selectedState: State;
  selectedQualificator: Qualificator;

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

  constructor(
    private primengConfig: PrimeNGConfig,
    private httpClient: HttpClient,
  ) {
    this.wordType = [
      { name: 'Именица', id: 0 },
      { name: 'Глагол', id: 1 },
      { name: 'Придев', id: 2 },
      { name: 'Заменица', id: 5 },
      { name: 'Број', id: 9 },
      { name: 'Прилог', id: 3 },
      { name: 'Предлог', id: 4 },
      { name: 'Узвик', id: 6 },
      { name: 'Речца', id: 7 },
      { name: 'Везник', id: 8 },
    ];
    this.state = [
      { name: 'Први унос', id: 1 },
      { name: 'Редактура 1', id: 2 },
      { name: 'Редактура 2', id: 3 },
    ];

    this.isNoun = true;
    this.isVerb = false;

    this.fetchQualificatiors();
  }

  async addNewDeterminant() {
    console.log('SELECTED WORDTYPE', this.selectedWordType?.id);
    console.log('SELECTED STATE', this.selectedState?.id);
    console.log('WORD E', this.wordE);
    console.log('WORD I', this.wordI);
    console.log('SELECTED VERB KIND', this.selectedKind?.id);
    console.log('NASTAVAK', this.extension);
    console.log('GLAGOLSKI VID', this.selectedVerbForm);
    console.log('GLAGOLSKI ROD', this.selectedVerbKind);
    console.log('INFO', this.details);
    console.log('PREZENT', this.present);
    console.log('KOLOKACIJE', this.collocations);
    console.log(`${this.wordE}` + ` ` + `${this.wordI}`);
    const response: any = await this.httpClient
      .post('api/odrednice/save-odrednica/', {
        rec: this.wordE,
        ijekavski: this.wordI,
        vrsta: this.selectedWordType?.id,
        rod: this.selectedKind?.id ? this.selectedKind?.id : null,
        nastavak: this.extension ? this.extension : null,
        info: this.details ? this.details : null,
        glagolski_vid: this.selectedVerbForm?.id
          ? this.selectedVerbForm?.id
          : 0,
        glagolski_rod: this.selectedVerbKind?.id
          ? this.selectedVerbKind?.id
          : 0,
        prezent: this.present ? this.present : 0,
        broj_pregleda: 1,
        stanje: this.selectedState?.id ? this.selectedState?.id : null,
        version: 1,
        kolokacija_set: this.collocations ? this.collocations : null,
        kvalifikatorodrednice_set: this.qualificators
          ? this.qualificators
          : null,
      })
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

  async fetchQualificatiors() {
    const response: any = await this.httpClient
      .get('api/odrednice/kvalifikator/')
      .toPromise();
    if (response) {
      this.qualificators = response.map((item) => {
        return { name: item.skracenica, id: item.id };
      });
    }
  }

  onChange() {
    this.selectedWordType.name === 'Именица' ||
    this.selectedWordType.name === 'Заменица' ||
    this.selectedWordType.name === 'Придев' ||
    this.selectedWordType.name === 'Број'
      ? (this.isNoun = true)
      : (this.isNoun = false);

    this.selectedWordType.name === 'Глагол'
      ? (this.isVerb = true)
      : (this.isVerb = false);
  }

  ngOnInit() {
    this.primengConfig.ripple = true;
  }
}
