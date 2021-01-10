import { Component, OnInit } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'synonym',
  templateUrl: './synonym.component.html',
})
export class SynonymComponent implements OnInit {
  constructor(
    private primengConfig: PrimeNGConfig,
    private httpClient: HttpClient,
  ) {}

  determinants: string[];
  selectedDeterminant: string;
  synonyms = [{ determinant: '' }];

  add() {
    this.synonyms.push({ determinant: this.determinants[0] });
  }

  async fetch() {
    const response: any = await this.httpClient
      .get('api/odrednice/odrednica')
      .toPromise();
    this.determinants = response.map((item) => {
      return item.rec;
    });
  }

  ngOnInit() {
    this.primengConfig.ripple = true;
    this.fetch();
  }
}
