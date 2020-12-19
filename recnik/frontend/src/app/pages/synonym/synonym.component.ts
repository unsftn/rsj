import { Component, OnInit } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

@Component({
  selector: 'synonym',
  templateUrl: './synonym.component.html',
})
export class SynonymComponent implements OnInit {
  constructor(private primengConfig: PrimeNGConfig) {}

  determinants: string[];
  selectedDeterminant: string;
  synonyms = [{ determinant: '' }];

  add() {
    this.synonyms.push({ determinant: this.determinants[0] });
  }

  ngOnInit() {
    this.primengConfig.ripple = true;
    this.determinants = [
      'Одредница 1',
      'Одредница 2',
      'Одредница 3',
      'Одредница 4',
    ];
  }
}
