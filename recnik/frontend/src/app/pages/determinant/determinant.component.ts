import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

@Component({
  selector: 'determinant',
  templateUrl: './determinant.component.html',
})
export class DeterminantComponent implements OnInit {
  constructor(
    private primengConfig: PrimeNGConfig,
    private httpClient: HttpClient,
  ) {}

  determinants: string[];
  selectedDeterminant: string;
  keywords = [{ determinant: '' }];
  filteredDeterminants: any[];

  add() {
    this.keywords.push({ determinant: '' });
  }

  remove(keyword) {
    this.keywords.splice(this.keywords.indexOf(keyword), 1);
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
