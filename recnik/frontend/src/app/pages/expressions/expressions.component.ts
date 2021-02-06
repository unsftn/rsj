import { Component, Input, OnInit } from '@angular/core';
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

  filteredKeywords: any[];
  keyWords = [];
  selectedKeyWord: string;

  @Input()
  expressions = [];

  add() {
    this.expressions.push({ value: '', keywords: [] });
  }

  remove(expression) {
    this.expressions.splice(this.expressions.indexOf(expression), 1);
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

  filterKeyword(event) {
    const query = event.query;
    this.filteredKeywords = this.keyWords.filter((kw) =>
      kw.toLowerCase().startsWith(query.toLowerCase()),
    );
  }

  ngOnInit() {
    this.primengConfig.ripple = true;
    this.fetch();
  }
}
