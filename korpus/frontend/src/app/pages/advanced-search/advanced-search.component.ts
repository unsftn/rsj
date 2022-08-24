import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-advanced-search',
  templateUrl: './advanced-search.component.html',
  styleUrls: ['./advanced-search.component.scss']
})
export class AdvancedSearchComponent implements OnInit {

  allWords: string;
  phrase: string;
  anyWord: string;
  withoutWords: string;

  constructor() { }

  ngOnInit(): void {
  }

  search(): void {
    alert('Nije još implementirano.');
  }
}
