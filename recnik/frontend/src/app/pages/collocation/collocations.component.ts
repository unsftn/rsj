import { Component, OnInit } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';
import { HttpClient } from '@angular/common/http';

class Collocation {
  keywordsArray = [];
  keywords: string[];
  note: string;
  selectedKeyword: string;

  constructor(keyword, note, keywordArray) {
    this.note = note;
    this.keywords = [];
    this.keywordsArray = keywordArray;
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
  constructor(
    private primengConfig: PrimeNGConfig,
    private httpClient: HttpClient,
  ) {}

  collocations: Collocation[];

  async add() {
    const determinants: any = await this.fetchDeterminants();
    const col = new Collocation(
      determinants.results[0].rec,
      '',
      determinants.results.map((item) => item.rec),
    );
    this.collocations.push(col);
  }

  async fetchDeterminants() {
    return await this.httpClient.get('api/odrednice/odrednica').toPromise();
  }

  ngOnInit() {
    this.primengConfig.ripple = true;
    this.collocations = [];
    this.add();
  }
}
