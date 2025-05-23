import { Component, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { LazyLoadEvent, MessageService } from 'primeng/api';
import { Title } from '@angular/platform-browser';
import { GenerisaniSpisak } from '../../../models/reci';
import { DeciderService } from '../../../services/decider/decider.service';
import { RecService } from '../../../services/reci/rec.service';
import { TokenStorageService } from '../../../services/auth/token-storage.service';

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
  noteVisible: boolean = false;

  odluke: any[] = [
    { name: 'без одлуке', code: 1 },
    { name: 'иде', code: 2 },
    { name: 'не иде', code: 3 },
    { name: 'у проширени', code: 4 },
    { name: 'уклони', code: 5 },
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

  filterBeleskaOptions: any[] = [
    { code: true, name: 'да' },
    { code: false, name: 'не' },
  ];

  filterPotkorpusOptions: any[] = [
    { code: 1, name: 'Књижевни' },
    { code: 2, name: 'Новински' },
    { code: 3, name: 'Разговорни' },
    { code: 4, name: 'Научни' },
    { code: 5, name: 'Административни' },
  ];

  filterRecnik: boolean = null;
  filterBeleska: boolean = null;
  filterOdluka: number[] = [];
  filterPotkorpus: number[] = [];
  leksema: string = '';
  filterFrekOd: number = null;
  filterFrekDo: number = null;
  first: number = null;
  rows: number = null;
  slovo: string = null;
  tabIndex: number;
  izabranaRec: any = {};

  constructor(
    private router: Router,
    private deciderService: DeciderService,
    private recService: RecService,
    private messageService: MessageService,
    private titleService: Title,
    private tokenStorageService: TokenStorageService,
  ) { }

  ngOnInit(): void {
    this.titleService.setTitle('Одлуке за речник');
    this.tabIndex = 0;
    this.deciderService.getLastSpisak().subscribe({
      next: (spisak: GenerisaniSpisak) => this.poslednjiSpisak = spisak,
      error: (error: any) => console.log(error),
    });
  }

  onChangeStatus(event: any, rec: any): void {
    rec.odluka_str = this.odluke[event.value-1].name;
  }

  onLazyLoad(event: LazyLoadEvent, slovo: string): void {
    this.first = event.first;
    this.rows = event.rows;
    this.loadReci(slovo);
  }

  onSearch(): void {
    this.loadReci(this.azbuka[this.tabIndex]);
  }

  onTabChange(event: any): void {
    this.loadReci(this.azbuka[this.tabIndex]);
  }

  loadReci(slovo: string): void {
    this.loading = true;
    this.deciderService.getByLetterPagedFiltered(
        slovo, this.first, this.rows, this.filterRecnik, this.filterOdluka, 
        this.filterPotkorpus, this.filterBeleska, this.leksema, this.filterFrekOd, 
        this.filterFrekDo).subscribe({
      next: (response: any) => {
        this.reci[slovo] = response.results.map((item: any) => { 
          item.odluka_str = this.odluke[item.odluka-1].name;
          item.vrsta_str = item.vrsta_reci != null ? this.vrste[item.vrsta_reci].name : '';
          item.in_rsj_str = item.recnik_id ? 'да': 'не';
          item.potkorpusi = this.potkorpusi(item);
          return item; 
        });
        this.ukupno[slovo] = response.count;
        this.loading = false;
      }, 
      error: (error: any) => console.log(error),
    });
  }

  setFilterRecnik(value: boolean): void {
    this.loadReci(this.azbuka[this.tabIndex]);
  }

  setFilterOdluka(value: number): void {
    this.loadReci(this.azbuka[this.tabIndex]);
  }

  setFilterBeleska(value: boolean): void {
    this.loadReci(this.azbuka[this.tabIndex]);
  }

  setFilterPotkorpus(value: number): void {
    this.loadReci(this.azbuka[this.tabIndex]);
  }

  setStatus(rec: any, odluka: number): void {
    rec.odluka = odluka;
    this.deciderService.update(rec).subscribe({
      next: (data) => {},
      error: (error: any) => {
        this.messageService.add({
          severity: 'error',
          summary: 'Грешка',
          life: 5000,
          detail: `Грешка приликом измене статуса речи: ${error}`,
        });
      }
    });
  }

  openRec(rec: any): void {
    let url = '';
    let queryParams = {};
    if (Number.isFinite(rec.vrsta_reci) && Number.isFinite(rec.korpus_id))
      queryParams = { id: rec.korpus_id, type: rec.vrsta_reci};
    else
      queryParams = { form: rec.tekst };

    url = this.router.serializeUrl(
      this.router.createUrlTree(['/search'], { queryParams }));
    window.open(url, '_blank');
  }

  openKorpus(rec: any): void {
    if (rec.korpus_id) {
      const url = this.router.serializeUrl(
        this.router.createUrlTree(
          this.recService.getEditRouterLink(rec.korpus_id, rec.vrsta_reci)));
      window.open(url, '_blank');  
    }
  }

  openRecnik(rec: any): void {
    if (rec.recnik_id)
      window.open(`https://recnik.rsj.rs/edit/${rec.recnik_id}`, '_blank');    
  }

  showNote(rec: any): void {
    this.izabranaRec = rec;
    this.noteVisible = true;
  }

  closeNote(): void {
    console.log('close');
    this.izabranaRec.beleska = this.izabranaRec.beleska.trim();
    this.noteVisible = false;
    this.deciderService.update(this.izabranaRec).subscribe({
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

  isVolunteer(): boolean {
    return this.tokenStorageService.isVolunteer();
  }

  isAdmin(): boolean {
    return this.tokenStorageService.isAdmin();
  }

  potkorpusi(rec: any): string {
    let potkorpusi = '';
    if (rec.potkorpus_1) potkorpusi += 'К ';
    if (rec.potkorpus_2) potkorpusi += 'Нв ';
    if (rec.potkorpus_3) potkorpusi += 'Р ';
    if (rec.potkorpus_4) potkorpusi += 'Нч ';
    if (rec.potkorpus_5) potkorpusi += 'Ад ';
    return potkorpusi.length > 0 ? potkorpusi.slice(0, -1) : '' ;
  }

}
