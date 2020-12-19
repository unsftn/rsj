import { Component, OnInit } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

@Component({
  selector: 'expressions',
  templateUrl: './expressions.component.html',
  styleUrls: ['./expressions.component.scss'],
})
export class ExpressionsComponent implements OnInit {
  constructor(private primengConfig: PrimeNGConfig) {}

  keyWords = [];
  selectedKeyWord: string;
  expressions = [{ value: '', keyWord: this.keyWords[0] }];

  add() {
    this.expressions.push({ value: '', keyWord: this.keyWords[0] });
  }

  ngOnInit() {
    this.primengConfig.ripple = true;
    this.keyWords = [
      'Кључна реч 1',
      'Кључна реч 2',
      'Кључна реч 3',
      'Кључна реч 4',
    ];
  }
}
