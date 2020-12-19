import { Component, OnInit } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

@Component({
  selector: 'antonym',
  templateUrl: './antonym.component.html',
})
export class AntonymComponent implements OnInit {
  constructor(private primengConfig: PrimeNGConfig) {}

  determinants: string[];
  selectedDeterminant: string;
  antonyms = [{ determinant: '' }];

  add() {
    this.antonyms.push({ determinant: this.determinants[0] });
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
