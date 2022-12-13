import { Component, OnInit } from '@angular/core';
import { LazyLoadEvent, MessageService } from 'primeng/api';
import { GenerisaniSpisak } from '../../../models/reci';
import { DeciderService } from '../../../services/decider/decider.service';
import { RecService } from '../../../services/reci/rec.service';

@Component({
  selector: 'app-all-words',
  templateUrl: './all-words.component.html',
  styleUrls: ['./all-words.component.scss']
})
export class AllWordsComponent implements OnInit {

  azbuka: string[] = ['а', 'б', 'в', 'г', 'д', 'ђ', 'е', 'ж', 'з', 'и', 'ј', 'к', 'л', 'љ', 'м', 'н', 'њ', 'о', 'п', 'р', 'с', 'т', 'ћ', 'у', 'ф', 'х', 'ц', 'ч', 'џ', 'ш', '_'];
  AZBUKA: string[] = ['А', 'Б', 'В', 'Г', 'Д', 'Ђ', 'Е', 'Ж', 'З', 'И', 'Ј', 'К', 'Л', 'Љ', 'М', 'Н', 'Њ', 'О', 'П', 'Р', 'С', 'Т', 'Ћ', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Џ', 'Ш', '_'];
  poslednjiSpisak: GenerisaniSpisak;
  reci = {'а': [], 'б': [], 'в': [], 'г': [], 'д': [], 'ђ': [], 'е': [], 'ж': [], 'з': [], 'и': [], 'ј': [], 'к': [], 'л': [], 
    'љ': [], 'м': [], 'н': [], 'њ': [], 'о': [], 'п': [], 'р': [], 'с': [], 'т': [], 'ћ': [], 'у': [], 'ф': [], 'х': [], 
    'ц': [], 'ч': [], 'џ': [], 'ш': [], '_': []};
  ukupno = {'а': 0, 'б': 0, 'в': 0, 'г': 0, 'д': 0, 'ђ': 0, 'е': 0, 'ж': 0, 'з': 0, 'и': 0, 'ј': 0, 'к': 0, 'л': 0, 
    'љ': 0, 'м': 0, 'н': 0, 'њ': 0, 'о': 0, 'п': 0, 'р': 0, 'с': 0, 'т': 0, 'ћ': 0, 'у': 0, 'ф': 0, 'х': 0, 
    'ц': 0, 'ч': 0, 'џ': 0, 'ш': 0, '_': 0};
  loading: boolean = true;

  odluke: any[] = [
    { name: 'без одлуке', code: 1 },
    { name: 'иде', code: 2 },
    { name: 'не иде', code: 3 },
    { name: 'уклони', code: 4 },
  ];

  vrste: any[] = [
    { name: 'именица', code: 0},
    { name: 'глагол', code: 1},
    { name: 'придев', code: 2},
    { name: 'прилог', code: 3},
    { name: 'предлог', code: 4},
    { name: 'заменица', code: 5},
    { name: 'узвик', code: 6},
    { name: 'речца', code: 7},
    { name: 'везник', code: 8},
    { name: 'број', code: 9},
    { name: 'остало', code: 10},
  ];

  filterRecnikOptions: any[] = [
    { code: true, name: 'да' },
    { code: false, name: 'не' },
  ];

  constructor(
    private deciderService: DeciderService,
    private recService: RecService,
    private messageService: MessageService,
  ) { }

  ngOnInit(): void {
    this.deciderService.getLastSpisak().subscribe({
      next: (spisak: GenerisaniSpisak) => this.poslednjiSpisak = spisak,
      error: (error: any) => console.log(error),
    });
  }

  onChangeStatus(event: any, rec: any): void {
    rec.odluka_str = this.odluke[event.value-1].name;
  }

  loadReci(event: LazyLoadEvent, slovo: string): void {
    this.loading = true;
    this.deciderService.getByLetterPaged(slovo, event.first, event.rows).subscribe({
      next: (response: any) => {
        this.reci[slovo] = response.results.map((item: any) => { 
          item.odluka_str = this.odluke[item.odluka-1].name;
          item.vrsta_str = item.vrsta_reci != null ? this.vrste[item.vrsta_reci].name : '';
          item.in_rsj_str = item.recnik_id ? 'да': 'не';
          return item; 
        });
        this.ukupno[slovo] = response.count;
        this.loading = false;
      }, 
      error: (error: any) => console.log(error),
    });
  }

  korpusLink(vrstaReci: number): string {
    return this.recService.getEditLink(vrstaReci);
  }

  status(rec: any, odluka: number): void {
    rec.odluka = odluka;
    this.deciderService.update(rec).subscribe({
      next: (data) => {},
      error: (error: any) => {
        console.log(error);        
        this.messageService.add({
          severity: 'error',
          summary: 'Грешка',
          life: 5000,
          detail: `Грешка приликом измене статуса речи: ${error}`,
        });
      }
    });
  }

}
