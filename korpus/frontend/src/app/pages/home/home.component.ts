import { Component, Injectable, HostListener, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { PrimeNGConfig } from 'primeng/api';
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
  word: any;
  hits: any[];
  searching: boolean;

  constructor(
    private primengConfig: PrimeNGConfig,
    private tokenStorageService: TokenStorageService,
    private titleService: Title,
    private router: Router,
    private sanitizer: DomSanitizer,
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
    this.searching = true;
    this.hits = [];
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
      },
      error: (error) => {
        console.log(error);
      }
    });
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
}
