import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Injectable } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
};

@Component({
  selector: 'home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
@Injectable({ providedIn: 'root' })
export class HomeComponent implements OnInit {
  listOfDeterminants = [];
  latest = [];
  changed = [];
  popular = [];
  constructor(
    private primengConfig: PrimeNGConfig,
    private httpClient: HttpClient,
  ) {}

  async fetch() {
    const latest = await this.httpClient
      .get('api/odrednice/odrednica-latest/')
      .toPromise();
    const changed = await this.httpClient
      .get('api/odrednice/odrednica-changed/')
      .toPromise();
    const popular = await this.httpClient
      .get('api/odrednice/odrednica-popular/')
      .toPromise();
    console.log(latest);
    console.log(changed);
    console.log(popular);
  }

  ngOnInit() {
    this.primengConfig.ripple = true;
    this.fetch();
  }
}
