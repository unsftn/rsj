import { Component, OnInit } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

interface WordType {
  name: string;
}

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
  wordType: WordType[];
  state: State[];
  qualificator: Qualificator[];

  selectedWordType: WordType;
  selectedState: State;
  selectedQualificator: Qualificator;

  constructor(private primengConfig: PrimeNGConfig) {
    this.wordType = [
      { name: 'Именица' },
      { name: 'Глагол' },
      { name: 'Придев' },
      { name: 'Заменица' },
      { name: 'Број' },
      { name: 'Прилог' },
      { name: 'Предлог' },
      { name: 'Узвик' },
      { name: 'Речца' },
      { name: 'Везник' },
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
  }

  ngOnInit() {
    this.primengConfig.ripple = true;
  }
}
