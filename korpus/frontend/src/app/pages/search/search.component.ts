import { Component, OnInit, ViewChild, ViewChildren, ElementRef, QueryList } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { DomSanitizer, SafeHtml, Title } from '@angular/platform-browser';
import { PrimeNGConfig, MessageService } from 'primeng/api';
import { OverlayPanel } from 'primeng/overlaypanel';
import { TokenStorageService } from '../../services/auth/token-storage.service';
import { SearchService } from '../../services/search';
import { RecService } from '../../services/reci';
import { transliterateSerbianCyrillicToLatin, transliterateSerbianLatinToCyrillic } from '../../utils/cyrlat';

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
  editorComponent: any;
  editorText: string;
  searchText: string;
  searchResults: any[];
  odrednica: any;
  azbuka = 'абвгдђежзијклљмнњопрстћуфхцчџш';
  selectedText: string;
  selectedHit: any;
  areYouSureVisible: boolean;
  areYouSureMessage: string;
  areYouSureCallback: any;
  areYouSureParams: any;
  primerRef: string;
  primerSubcorpus: string;
  primerCollection: any[];
  primerIndex: number;

  @ViewChild('colorpicker') colorPicker: OverlayPanel;
  @ViewChild('reference') refPanel: OverlayPanel;
  @ViewChild('referenceRecnik') refPanelRecnik: OverlayPanel;
  @ViewChild('addRef') addRefPanel: OverlayPanel;
  @ViewChildren('primer') primeri: QueryList<ElementRef>;

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
      { name: 'фраг. 1000', code: 1000 },
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
        this.messageService.add({
          severity: 'error',
          summary: 'Грешка',
          life: 5000,
          detail: error,
        });
      }
    });
  }

  fetchData(): void {
    this.searching = true;
    this.hits = [];
    if (Number.isFinite(this.wordId) && Number.isFinite(this.wordType)) {
      this.recService.get(this.wordId, this.wordType).subscribe({
        next: (word: any) => {
          this.word = word;
          this.loadFromRecnik(word.osnovni_oblik);
        },
        error: (error) => {
          this.searching = false;
          this.messageService.add({
            severity: 'error',
            summary: 'Грешка',
            life: 5000,
            detail: error,
        })}
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

  openPrimerRef(event: any, primeri: any[], index: number): void {
    this.primerRef = primeri[index].opis;
    this.primerSubcorpus = primeri[index].potkorpus;
    this.primerIndex = index;
    this.primerCollection = primeri;
    this.refPanelRecnik.toggle(event);
  }

  pickColor(color: any): void {
    this.coloredHit.color = color;
    this.colorPicker.hide();
  }

  selectText(event: any, hit: any): void {
    const selection = document.getSelection();
    if (!selection.isCollapsed && this.odrednica) {
      this.selectedText = selection.toString().trim();
      this.selectedHit = hit;
      this.addRefPanel.toggle(event);
    }
  }

  editorSave(): void {
    this.editorVisible = false;
    this.editorComponent.tekst = this.editorText;
  }

  editorCancel(): void {
    this.editorVisible = false;
  }

  editorOpen(component: any) {
    this.editorComponent = component;
    this.editorText = component.tekst;
    this.editorVisible = true;
  }

  search(event): void {
    this.searchService.searchRecnik(event.query).subscribe({
      next: (data) => {
        this.searchResults = data;
      },
      error: (error) => {
        this.messageService.add({
          severity: 'error',
          summary: 'Грешка',
          life: 5000,
          detail: error,
        });
      }
    });
  }

  select(event): void {
    this.searchText = '';
    this.searchService.readRecnik(event.value.pk).subscribe({
      next: (data) => { this.odrednica = data; },
      error: (error) => { 
        this.odrednica = null; 
        this.messageService.add({
          severity: 'error',
          summary: 'Грешка',
          life: 5000,
          detail: error,
        });
    }
    });
  }

  loadFromRecnik(rec: string): void {
    this.searchService.searchRecnik(rec).subscribe({
      next: (data) => {
        this.searchResults = data;
        if (data.length === 1) {
          const pk = data[0].pk;
          this.searchService.readRecnik(pk).subscribe({
            next: (data) => { this.odrednica = data; },
            error: (error) => { 
              this.odrednica = null; 
              this.messageService.add({
                severity: 'error',
                summary: 'Грешка',
                life: 5000,
                detail: error,
              });
            }
          });
        }
      },
      error: (error) => {
        this.messageService.add({
          severity: 'error',
          summary: 'Грешка',
          life: 5000,
          detail: error,
        });
      }
    });
  }

  trackByFn(index: number, item: any): any {
    return index;
  }

  moveMeaningUp(index: number): void {
    if (index === 0)
      return;
    const meaning = this.odrednica.znacenja.splice(index, 1)[0];
    this.odrednica.znacenja.splice(index - 1, 0, meaning);
    this.renumber(this.odrednica.znacenja);
  }

  moveMeaningDown(index: number): void {
    if (index === this.odrednica.znacenja.length - 1)
      return;
    const meaning = this.odrednica.znacenja.splice(index, 1)[0];
    this.odrednica.znacenja.splice(index + 1, 0, meaning);
    this.renumber(this.odrednica.znacenja);
  }

  moveSubmeaningUp(meaningIndex: number, subMeaningIndex: number): void {
    if (subMeaningIndex === 0)
      return;
    const submeaning = this.odrednica.znacenja[meaningIndex].podznacenja.splice(subMeaningIndex, 1)[0];
    this.odrednica.znacenja[meaningIndex].podznacenja.splice(subMeaningIndex - 1, 0, submeaning);
    this.renumber(this.odrednica.znacenja[meaningIndex].podznacenja);
  }

  moveSubmeaningDown(meaningIndex: number, subMeaningIndex: number): void {
    if (subMeaningIndex === this.odrednica.znacenja[meaningIndex].podznacenja.length - 1)
      return;
    const submeaning = this.odrednica.znacenja[meaningIndex].podznacenja.splice(subMeaningIndex, 1)[0];
    this.odrednica.znacenja[meaningIndex].podznacenja.splice(subMeaningIndex + 1, 0, submeaning);
    this.renumber(this.odrednica.znacenja[meaningIndex].podznacenja);
  }

  movePrimerUp(primerIndex: number, primeri: any[]): void {
    this.refPanelRecnik.hide();
    if (primerIndex === 0)
      return;
    const primer = primeri.splice(primerIndex, 1)[0];
    primeri.splice(primerIndex - 1, 0, primer);
    this.renumber(primeri);
  }

  movePrimerDown(primerIndex: number, primeri: any[]): void {
    this.refPanelRecnik.hide();
    if (primerIndex === primeri.length - 1)
      return;
    const primer = primeri.splice(primerIndex, 1)[0];
    primeri.splice(primerIndex + 1, 0, primer);
    this.renumber(primeri);
  }

  addMeaning(): void {
    this.odrednica.znacenja.push({ rbr: this.odrednica.znacenja.length + 1, tekst: '', id: null, podznacenja: [], primeri: [] });
  }

  addSubmeaning(meaning: any): void {
    meaning.podznacenja.push({ rbr: meaning.podznacenja.length + 1, tekst: '', id: null, primeri: [] });
  }

  renumber(collection: any[]): void {
    for (let i = 0; i < collection.length; i++)
      collection[i].rbr = i + 1;
  }

  addReference(meaningIndex: number, submeaningIndex: number): void {
    if (!this.odrednica)
      return;
    if (submeaningIndex === undefined || submeaningIndex === null) {
      this.odrednica.znacenja[meaningIndex].primeri.push({ 
        id: null,
        tekst: this.selectedText, 
        izvor_id: this.selectedHit.id,
        opis: this.selectedHit.opis,
        potkorpus: this.selectedHit.potkorpus,
        skracenica: this.selectedHit.skracenica,
        rbr: this.odrednica.znacenja[meaningIndex].primeri.length + 1
      });
    } else {
      this.odrednica.znacenja[meaningIndex].podznacenja[submeaningIndex].primeri.push({ 
        id: null,
        tekst: this.selectedText, 
        izvor_id: this.selectedHit.id,
        opis: this.selectedHit.opis,
        potkorpus: this.selectedHit.potkorpus,
        skracenica: this.selectedHit.skracenica,
        rbr: this.odrednica.znacenja[meaningIndex].podznacenja[submeaningIndex].primeri + 1
      });
    }
    this.addRefPanel.hide();
  }

  areYouSure(message: string, callback: any, params: any): void {
    this.areYouSureMessage = message;
    this.areYouSureVisible = true;
    this.areYouSureCallback = callback;
    this.areYouSureParams = params;
  }

  areYouSureYes(): void {
    this.areYouSureCallback(this.areYouSureParams);
    this.areYouSureVisible = false;
  }

  areYouSureNo(): void {
    this.areYouSureVisible = false;
  }

  deleteFrom(params: any): void {
    params.collection.splice(params.index, 1);
    this.renumber(params.collection);
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

  toCyrillic(): void {
    this.editorText = transliterateSerbianLatinToCyrillic(this.editorText);
  }

  toLatin(): void {
    this.editorText = transliterateSerbianCyrillicToLatin(this.editorText);
  }

}
