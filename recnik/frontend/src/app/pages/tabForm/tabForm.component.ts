import { Component, OnInit } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

interface State {
  name: string;
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
  wordType: string[];
  state: State[];
  qualificator: Qualificator[];
  isNoun: boolean;
  isVerb: boolean;

  selectedWordType: string;
  selectedState: State;
  selectedQualificator: Qualificator;

  constructor(private primengConfig: PrimeNGConfig) {
    this.wordType = [
      'Именица',
      'Глагол',
      'Придев',
      'Заменица',
      'Број',
      'Прилог',
      'Предлог',
      'Узвик',
      'Речца',
      'Везник',
    ];
    this.state = [
      { name: 'Први унос' },
      { name: 'Редактура 1' },
      { name: 'Редактура 2' },
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
    this.selectedWordType === 'Именица' ||
    this.selectedWordType === 'Заменица' ||
    this.selectedWordType === 'Придев' ||
    this.selectedWordType === 'Број'
      ? (this.isNoun = true)
      : (this.isNoun = false);
    console.log(this.isNoun);

    this.selectedWordType === 'Глагол'
      ? (this.isVerb = true)
      : (this.isVerb = false);
  }

  ngOnInit() {
    this.primengConfig.ripple = true;
  }
}
