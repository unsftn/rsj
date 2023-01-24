import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';

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
  wordStart: string;
  wordEnd: string;
  wordPart: string;
  distanceWords: string;
  distance: number;
  showSidebar: boolean;
  caseSensitive: boolean;

  constructor(private titleService: Title) { }

  ngOnInit(): void {
    this.titleService.setTitle('Напредна претрага');
    this.showSidebar = false;
    this.caseSensitive = false;
    this.distance = 5;
  }

  search(): void {
    alert('Nije još implementirano.');
  }
}
