import { Component, Injectable, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { DomSanitizer, SafeHtml, Title } from '@angular/platform-browser';
import { PrimeNGConfig, MessageService } from 'primeng/api';
import { OverlayPanel } from 'primeng/overlaypanel';
import { TokenStorageService } from '../../services/auth/token-storage.service';
import { SearchService } from '../../services/search';
import { RecService } from '../../services/reci';

@Component({
  selector: 'home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
@Injectable({providedIn: 'root'})
export class HomeComponent implements OnInit {

  wordId: number;
  wordType: number;
  wordForm: string;
  word: any;
  hits: any[];
  hitPage: any[];
  hitsPerPage: number;
  searching: boolean;
  first: number;
  fragmentSize: any;
  scanner: any;
  fragmentSizes: any[];
  scanners: any[];
  coloredHit: any;

  @ViewChild('colorpicker') colorPicker: OverlayPanel;

  constructor(
    private primengConfig: PrimeNGConfig,
    private tokenStorageService: TokenStorageService,
    private titleService: Title,
    private router: Router,
    private sanitizer: DomSanitizer,
    private messageService: MessageService,
    private searchService: SearchService,
    private recService: RecService,
  ) {
    this.fragmentSizes = [
      { name: 'фраг. 150', code: 150 },
      { name: 'фраг. 200', code: 200 },
      { name: 'фраг. 300', code: 300 },
    ];
    this.scanners = [
      { name: 'реч', code: 'word' },
      { name: 'реченица', code: 'sentence' },
    ]
  }

  ngOnInit(): void {
    // this.titleService.setTitle('Српко');
    // this.fragmentSize = this.fragmentSizes[0];
    // this.scanner = this.scanners[0];
    // this.primengConfig.ripple = true;
    // if (this.searchService.selectedWordId || this.searchService.selectedWordForm)
    //   this.fetchData();
    // this.searchService.selectedWordChanged.subscribe({
    //   next: (data: boolean) => {
    //     this.fetchData();
    //   },
    //   error: (error) => {
    //     console.log(error);
    //   }
    // });
  }

  fetchData(): void {
    this.wordId = this.searchService.selectedWordId;
    this.wordType = this.searchService.selectedWordType;
    this.wordForm = this.searchService.selectedWordForm;
    this.searching = true;
    this.hits = [];
    if (this.wordId) {
      this.recService.get(this.wordId, this.wordType).subscribe({
        next: (word: any) => {
          this.word = word;
        },
        error: (error) => {
          console.log(error);
        }
      });
      this.searchService.searchPubs(this.wordId, this.wordType, this.fragmentSize.code, this.scanner.code).subscribe({
        next: (hits: any[]) => {
          this.searching = false;
          this.hits = hits;
          this.first = 0;
          this.hitsPerPage = 100;
          this.hitPage = this.hits.slice(this.first, this.first + this.hitsPerPage);
        },
        error: (error) => {
          this.searching = false;
          console.log(error);
          this.messageService.add({
            severity: 'error',
            summary: 'Грешка',
            life: 5000,
            detail: error,
          });
        }
      });  
    } else {
      this.word = null;
      console.log(`Home searching for ${this.wordForm}`);
      this.searchService.searchForms(this.wordForm, this.fragmentSize.code, this.scanner.code, false).subscribe({
        next: (hits: any[]) => {
          this.searching = false;
          this.hits = hits;
          this.first = 0;
          this.first = 0;
          this.hitsPerPage = 100;
          this.hitPage = this.hits.slice(this.first, this.first + this.hitsPerPage);
        },
        error: (error) => {
          this.searching = false;
          console.log(error);
          this.messageService.add({
            severity: 'error',
            summary: 'Грешка',
            life: 5000,
            detail: error,
          });
        }
      });
    }
  }

  safe(html: string): SafeHtml {
    return this.sanitizer.bypassSecurityTrustHtml(html);
  }

  goto(odrId: number): void {
    this.router.navigate(['/edit', odrId]);
  }

  isLoggedIn(): boolean {
    return this.tokenStorageService.isLoggedIn();
  }

  isEditor(): boolean {
    return this.tokenStorageService.isEditor();
  }

  get editRouterLink(): any[] {
    return this.recService.getEditRouterLink(this.wordId, this.wordType);
  }

  onPageChange(event: any): void {
    this.first = event.first;
    this.hitsPerPage = event.rows;
    this.hitPage = this.hits.slice(this.first, this.first + this.hitsPerPage);
  }

  changeFragmentSize(event: any): void {
    this.fetchData();
  }

  changeScanner(event: any): void {
    this.fetchData();
  }

  openColorPicker(event: any, hit: any): void {
    this.coloredHit = hit;
    this.colorPicker.toggle(event);
  }

  pickColor(color: any): void {
    this.coloredHit.color = color;
    this.colorPicker.hide();
  }

  pogodaka(): string {
    // izuzetak: 11, 12, 13, 14 pogodaka
    const teens = this.hits.length % 100;
    if (teens > 10 && teens < 20)
      return 'погодака';
    const ostatak = this.hits.length % 10;
    switch (ostatak) {
      case 1: 
        return 'погодак';
      case 2:
      case 3:
      case 4:
        return 'поготка';
      default: 
        return 'погодака';
    }
  }
}
