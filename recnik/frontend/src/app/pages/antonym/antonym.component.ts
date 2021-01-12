import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

@Component({
  selector: 'antonym',
  templateUrl: './antonym.component.html',
})
export class AntonymComponent implements OnInit {
  constructor(
    private primengConfig: PrimeNGConfig,
    private httpClient: HttpClient,
  ) {}

  determinants: string[];
  selectedDeterminant: string;
  antonyms = [{ determinant: '' }];

  add() {
    this.antonyms.push({ determinant: this.determinants[0] });
  }

  async fetch() {
    const response: any = await this.httpClient
      .get('api/odrednice/odrednica')
      .toPromise();

    if (response) {
      this.determinants = response.results.map((item) => {
        return item.rec;
      });
    }
  }

  ngOnInit() {
    this.primengConfig.ripple = true;
    this.fetch();
  }
}
