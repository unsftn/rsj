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
    {name: 'не додати у речник', code: 2},
    {name: 'уклонити из речника', code: 3},
  ];
  filterRecnikOptions: any[] = [
    {code: true, name: 'да'},
    {code: false, name: 'не'},
  ];

  constructor() { }

  ngOnInit(): void {
    this.words = this.demoWords();
  }

  onChangeStatus(event: any, rec: any): void {
    rec.status_str = this.statuses[event.value].name;
  }

  demoWords(): any[] {
    return [
      {
        word: 'глава',
        pub_count: 532,
        freq: 3424,
        in_rsj: true,
        in_rsj_str: 'да',
        status: 0,
        status_str: 'недефинисано',
        pubs: [{
          word: 'глава',
          pubskr: 'Скр.1',
          freq: 21
        }, {
          word: 'главе',
          pubskr: 'Скр.1',
          freq: 22
        }, {
          word: 'главом',
          pubskr: 'Скр.1',
          freq: 13
        }, {
          word: 'главама',
          pubskr: 'Скр.2',
          freq: 11
        }, {
          word: 'глави',
          pubskr: 'Скр.2',
          freq: 9
        }]
      },
      {
        word: 'поглед',
        pub_count: 312,
        freq: 2461,
        in_rsj: true,
        in_rsj_str: 'да',
        status: 0,
        status_str: 'недефинисано',
        pubs: [{
          word: 'поглед',
          pubskr: 'Скр.1',
          freq: 21
        }, {
          word: 'погледа',
          pubskr: 'Скр.2',
          freq: 22
        }, {
          word: 'погледом',
          pubskr: 'Скр.2',
          freq: 13
        }, {
          word: 'погледи',
          pubskr: 'Скр.3',
          freq: 11
        }, {
          word: 'погледима',
          pubskr: 'Скр.3',
          freq: 9
        }]
      },
    ];
  }
}
