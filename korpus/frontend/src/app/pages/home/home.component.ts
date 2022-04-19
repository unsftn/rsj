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
    this.searchService.selectedWordChanged.subscribe({
      next: (data: boolean) => {
        this.wordId = this.searchService.selectedWordId;
        this.wordType = this.searchService.selectedWordType;
        this.recService.get(this.wordId, this.wordType).subscribe({
          next: (word: any) => {
            this.word = word;
            console.log(word);
          },
          error: (error) => {
            console.log(error);
          }
        });
        this.searchService.searchPubs(this.wordId, this.wordType).subscribe({
          next: (hits: any[]) => {
            this.hits = hits;
          },
          error: (error) => {
            console.log(error);
          }
        });
      },
      error: (error) => {
        console.log(error);
      }
    });
    this.searchService.selectedWordId = 28247;
    this.searchService.selectedWordType = 0;
    this.searchService.selectedWordChanged.emit(true);
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
