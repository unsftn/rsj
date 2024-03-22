import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { DomSanitizer, SafeHtml, Title } from '@angular/platform-browser';
import { PrimeNGConfig, MessageService } from 'primeng/api';
import { OverlayPanel } from 'primeng/overlaypanel';
import { TokenStorageService } from '../../services/auth/token-storage.service';
import { SearchService } from '../../services/search';
import { RecService } from '../../services/reci';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit {

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
  caseSensitive: boolean;
  fragmentSizes: any[];
  scanners: any[];
  coloredHit: any;
  referencePreview: string;
  referenceSubcorpus: string;
  editorVisible: boolean;
  editorText: string;
  searchText: string;
  searchResults: any[];

  @ViewChild('colorpicker') colorPicker: OverlayPanel;
  @ViewChild('reference') refPanel: OverlayPanel;
  @ViewChild('reference2') refPanel2: OverlayPanel;

  constructor(
    private primengConfig: PrimeNGConfig,
    private tokenStorageService: TokenStorageService,
    private titleService: Title,
    private router: Router,
    private route: ActivatedRoute,
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
    this.titleService.setTitle('Корпус');
    this.fragmentSize = this.fragmentSizes[0];
    this.scanner = this.scanners[0];
    this.primengConfig.ripple = true;
    this.route.queryParams.subscribe(params => {
      if (params.id !== undefined)
        if (!isNaN(+params.id))
          this.wordId = +params.id;
      if (params.type !== undefined)
        if (!isNaN(+params.type))
          this.wordType = +params.type;        
      if (params.form !== undefined)
        this.wordForm = params.form;
      if (params.cs !== undefined)
        this.caseSensitive = params.cs === 'true';
      if ((Number.isFinite(this.wordId) && Number.isFinite(this.wordType)) || this.wordForm)
        this.fetchData();
    });
    this.searchService.selectedWordChanged.subscribe({
      next: (data: boolean) => {
        this.wordId = this.searchService.selectedWordId;
        this.wordType = this.searchService.selectedWordType;
        this.wordForm = this.searchService.selectedWordForm;
        this.fetchData();
      },
      error: (error: any) => {
        console.log(error);
      }
    });
  }

  fetchData(): void {
    this.searching = true;
    this.hits = [];
    if (Number.isFinite(this.wordId) && Number.isFinite(this.wordType)) {
      this.recService.get(this.wordId, this.wordType).subscribe({
        next: (word: any) => this.word = word,
        error: (error) => console.log(error)
      });
      this.searchService.searchPubs(this.wordId, this.wordType, this.fragmentSize.code, this.scanner.code).subscribe({
        next: (hits: any[]) => {
          this.searching = false;
          this.process(hits);
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
      this.searchService.searchForms(this.wordForm, this.fragmentSize.code, this.scanner.code, this.caseSensitive).subscribe({
        next: (hits: any[]) => {
          this.searching = false;
          this.process(hits);
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

  process(hits: any[]): void {
    for (let i = 0; i < hits.length; i++) {
      const hit = hits[i];
      hit.highlights = hit.highlights.split('***');
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

  openReference(event: any, hit: any): void {
    this.referencePreview = hit.opis;
    this.referenceSubcorpus = hit.potkorpus;
    this.refPanel.toggle(event);
  }

  openReference2(event: any, hit: any): void {
    this.referencePreview = hit.opis;
    this.referenceSubcorpus = hit.potkorpus;
    this.refPanel2.toggle(event);
  }

  pickColor(color: any): void {
    this.coloredHit.color = color;
    this.colorPicker.hide();
  }

  selectText(event: any, hit: any): void {
    const selection = document.getSelection();
    if (!selection.isCollapsed) {
      const text = selection.toString().trim();
      console.log(text);
    }
  }

  editorSave(): void {
    this.editorVisible = false;
  }

  editorCancel(): void {
    this.editorVisible = false;
  }

  editorOpen(text: string) {
    this.editorText = text;
    this.editorVisible = true;
  }

  search(event): void {
    this.searchService.searchRecnik(event.query).subscribe({
      next: (data) => {
        this.searchResults = data;
      },
      error: (error) => {
        console.log(error);
      }
    });
  }

  select(event): void {
    console.log(event);
    this.searchText = '';
    //this.router.navigate(['/edit', event.value.pk]);
  }


  pogodaka(): string {
    // izuzetak: 11, 12, 13, 14 pogodaka
    if (this.hits === undefined)
      return 'погодака';
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
