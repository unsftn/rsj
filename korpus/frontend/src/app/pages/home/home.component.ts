import { Component, Injectable, HostListener, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { PrimeNGConfig, MessageService } from 'primeng/api';
import { TokenStorageService } from '../../services/auth/token-storage.service';
import { DomSanitizer, SafeHtml, Title } from '@angular/platform-browser';
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

  constructor(
    private primengConfig: PrimeNGConfig,
    private tokenStorageService: TokenStorageService,
    private titleService: Title,
    private router: Router,
    private sanitizer: DomSanitizer,
    private messageService: MessageService,
    private searchService: SearchService,
    private recService: RecService,
  ) {}

  ngOnInit(): void {
    this.titleService.setTitle('Почетна');
    this.primengConfig.ripple = true;
    if (this.searchService.selectedWordId)
      this.fetchData();
    this.searchService.selectedWordChanged.subscribe({
      next: (data: boolean) => {
        this.fetchData();
      },
      error: (error) => {
        console.log(error);
      }
    });
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
      this.searchService.searchPubs(this.wordId, this.wordType).subscribe({
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
      this.searchService.searchForms(this.wordForm).subscribe({
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

  get editRouterLink(): any[] {
    return this.recService.getEditRouterLink(this.wordId, this.wordType);
  }

  onPageChange(event: any) {
    this.first = event.first;
    this.hitsPerPage = event.rows;
    this.hitPage = this.hits.slice(this.first, this.first + this.hitsPerPage);
  }
}
