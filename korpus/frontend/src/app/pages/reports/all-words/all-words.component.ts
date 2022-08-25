import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-all-words',
  templateUrl: './all-words.component.html',
  styleUrls: ['./all-words.component.scss']
})
export class AllWordsComponent implements OnInit {

  words: any[];
  statuses: any[] = [
    {name: 'недефинисано', code: 0},
    {name: 'додати у речник', code: 1},
    {name: 'игнорисати', code: 2},
  ];

  constructor() { }

  ngOnInit(): void {
    this.words = this.demoWords();
  }

  onChangeStatus(event: any, rec: any): void {
    // console.log(event, rec);
    rec.status_str = this.statuses[event.value].name;
  }

  demoWords(): any[] {
    return [
      {
        leksema: 'глава',
        br_izvora: 532,
        frekvencija: 3424,
        u_recniku: true,
        u_recniku_str: 'да',
        status: 0,
        status_str: 'недефинисано',
        oblici: 'главе глави главом главама'
      },
      {
        leksema: 'поглед',
        br_izvora: 312,
        frekvencija: 2461,
        u_recniku: true,
        u_recniku_str: 'да',
        status: 0,
        status_str: 'недефинисано',
        oblici: 'погледа погледе погледом погледи погледима'
      },
    ];
  }
}
