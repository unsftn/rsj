import { Component, Input, OnInit } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'expressions',
  templateUrl: './expressions.component.html',
  styleUrls: ['./expressions.component.scss'],
})
export class ExpressionsComponent implements OnInit {
  filteredKeywords: any[];
  keyWords = [];
  selectedKeyWord: string;

  @Input() isTopLevel: boolean;
  @Input() expressions = [];

  constructor(
    private primengConfig: PrimeNGConfig,
    private httpClient: HttpClient,
  ) {}

  add(): void {
    this.expressions.push({ value: '', tekst: '', keywords: [] });
  }

  remove(expression): void {
    this.expressions.splice(this.expressions.indexOf(expression), 1);
  }

  async fetch(): Promise<void> {
    const response: any = await this.httpClient
      .get('api/odrednice/odrednica')
      .toPromise();

    if (response) {
      this.keyWords = response.map((item) => {
        return item.rec;
      });
    }
  }

  filterKeyword(event): void {
    const query = event.query;
    this.filteredKeywords = this.keyWords.filter((kw) =>
      kw.toLowerCase().startsWith(query.toLowerCase()),
    );
  }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
    this.fetch();
  }
}
