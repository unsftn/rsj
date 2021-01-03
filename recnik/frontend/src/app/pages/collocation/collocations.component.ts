import { Component, OnInit } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

class Collocation {
  keywordsArray = [];
  keywords: string[];
  note: string;
  selectedKeyword: string;

  constructor(keyword, note) {
    this.keywordsArray = [
      'Кључна реч 1',
      'Кључна реч 2',
      'Кључна реч 3',
      'Кључна реч 4',
    ];
    this.note = note;
    this.keywords = [];
    this.add(keyword);
  }

  add(keyword) {
    this.keywords.push(keyword);
  }
}

@Component({
  selector: 'collocations',
  templateUrl: './collocations.component.html',
  styleUrls: ['./collocations.component.scss'],
})
export class CollocationsComponent implements OnInit {
  constructor(private primengConfig: PrimeNGConfig) {}

  collocations: Collocation[];

  add() {
    this.collocations.push(new Collocation('', ''));
  }

  ngOnInit() {
    this.primengConfig.ripple = true;
    this.collocations = [];
    this.add();
  }
}
