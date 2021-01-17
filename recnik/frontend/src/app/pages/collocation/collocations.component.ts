import { Component, OnInit, Output, EventEmitter, Input } from '@angular/core';
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

  remove(keyword) {
    this.keywords.splice(this.keywords.indexOf(keyword), 1);
  }
}

@Component({
  selector: 'collocations',
  templateUrl: './collocations.component.html',
  styleUrls: ['./collocations.component.scss'],
})
export class CollocationsComponent implements OnInit {
  @Input() collocations: Collocation[];

  @Output() collocationChanged: EventEmitter<
    Collocation[]
  > = new EventEmitter();

  constructor(
    private primengConfig: PrimeNGConfig,
    private httpClient: HttpClient,
  ) {}

  changeCollocation() {
    this.collocationChanged.emit(this.collocations);
  }

  async add() {
    const determinants: any = await this.fetchDeterminants();
    const col = new Collocation(
      determinants.rec,
      '',
      determinants.map((item) => item.rec),
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
