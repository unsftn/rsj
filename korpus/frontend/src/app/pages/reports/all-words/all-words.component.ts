import { Component, OnInit } from '@angular/core';
import { LazyLoadEvent } from 'primeng/api';
import { RecZaOdluku, GenerisaniSpisak } from '../../../models/reci';
import { DeciderService } from '../../../services/decider/decider.service';

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

  filterRecnikOptions: any[] = [
    { code: true, name: 'да' },
    { code: false, name: 'не' },
  ];

  constructor(
    private deciderService: DeciderService,
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
        this.reci[slovo] = response.results.map(item => { item.odluka_str = this.odluke[item.odluka-1].name; return item; });
        this.ukupno[slovo] = response.count;
        this.loading = false;
      }, 
      error: (error: any) => console.log(error),
    });
  }

}
