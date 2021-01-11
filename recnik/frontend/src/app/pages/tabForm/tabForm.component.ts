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
}

@Component({
  selector: 'tabForm',
  templateUrl: './tabForm.component.html',
  styleUrls: ['./tabForm.component.scss'],
})
export class TabFormComponent implements OnInit {
  wordType: WordType[];
  state: State[];
  qualificator: Qualificator[];
  isNoun: boolean;
  isVerb: boolean;
  wordE: string;
  wordI: string;
  selectedKind;

  selectedVerbKind;
  selectedVerbForm;
  present: string;
  details;

  selectedWordType: WordType;
  selectedState: State;
  selectedQualificator: Qualificator;

  selectedKindChangedHandler(selectedKind) {
    this.selectedKind = selectedKind;
  }

  constructor(private primengConfig: PrimeNGConfig) {
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
    this.qualificator = [
      { name: 'Прва ставка' },
      { name: 'Друга ставка' },
      { name: 'Трећа ставка' },
    ];

    this.isNoun = true;
    this.isVerb = false;
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
