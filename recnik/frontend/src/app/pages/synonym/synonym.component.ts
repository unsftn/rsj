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
  filteredDeterminants: any[];

  add() {
    this.synonyms.push({ determinant: '' });
  }

  remove(synonym) {
    this.synonyms.splice(this.synonyms.indexOf(synonym), 1);
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
