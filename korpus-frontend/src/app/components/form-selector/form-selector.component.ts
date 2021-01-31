import { Component, OnInit } from '@angular/core';

interface WordType {
  name: string;
}

@Component({
  selector: 'app-form-selector',
  templateUrl: './form-selector.component.html',
  styleUrls: ['./form-selector.component.scss']
})
export class FormSelectorComponent implements OnInit {

  wordTypes: WordType[];
  selectedWordType: WordType;

  constructor() {
    this.wordTypes = [
      {name:'именица'},
      {name:'глагол'},
      {name:'придев'},
      {name:'заменица'},
      {name:'број'},
      {name:'прилог'},
      {name:'предлог'},
      {name:'узвик'},
      {name:'речца'},
      {name:'везник'}
    ];
   }

  ngOnInit(): void {
    if (window.location.href.endsWith('/rec') && !window.location.href.endsWith('/rec/rec'))
      this.selectedWordType = {name:''};
    else // TODO getWord
      this.selectedWordType = {name:'именица'};
  }

  back(): void {
    window.history.back();
  }
}
