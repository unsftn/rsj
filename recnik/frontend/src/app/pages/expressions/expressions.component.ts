import { Component, OnInit } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'expressions',
  templateUrl: './expressions.component.html',
  styleUrls: ['./expressions.component.scss'],
})
export class ExpressionsComponent implements OnInit {
  constructor(
    private primengConfig: PrimeNGConfig,
    private httpClient: HttpClient,
  ) {}

  keyWords = [];
  selectedKeyWord: string;
  expressions = [{ value: '', keyWord: this.keyWords[0] }];

  add() {
    this.expressions.push({ value: '', keyWord: this.keyWords[0] });
  }

  async fetch() {
    const response: any = await this.httpClient
      .get('api/odrednice/odrednica')
      .toPromise();

    if (response) {
      this.keyWords = response.map((item) => {
        return item.rec;
      });
    }
  }

  ngOnInit() {
    this.primengConfig.ripple = true;
    this.fetch();
  }
}
