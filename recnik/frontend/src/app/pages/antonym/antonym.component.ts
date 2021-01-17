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
  filteredDeterminants: any[];

  add() {
    this.antonyms.push({ determinant: '' });
  }

  remove(antonym) {
    this.antonyms.splice(this.antonyms.indexOf(antonym), 1);
  }

  filterDeterminants(event) {
    const query = event.query;
    this.filteredDeterminants = this.determinants.filter((kw) =>
      kw.toLowerCase().startsWith(query.toLowerCase()),
    );
  }

  async fetch() {
    const response: any = await this.httpClient
      .get('api/odrednice/odrednica')
      .toPromise();

    if (response) {
      this.determinants = response.map((item) => {
        return item.rec;
      });
    }
  }

  ngOnInit() {
    this.primengConfig.ripple = true;
    this.fetch();
  }
}
