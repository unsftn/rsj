import { Component, Injectable, HostListener, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { PrimeNGConfig } from 'primeng/api';
import { Table } from 'primeng/table';
import { TokenStorageService } from '../../services/auth/token-storage.service';
import { DomSanitizer, SafeHtml, Title } from '@angular/platform-browser';
import { SearchService } from '../../services/search/search.service';

class UserCollection extends Array {
  sum(key): number {
    return this.reduce((a, b) => a + (b[key] || 0), 0);
  }
}

@Component({
  selector: 'home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
@Injectable({providedIn: 'root'})
export class HomeComponent implements OnInit {

  users: UserCollection;
  colors = ['#ffbe0b', '#fb5607', '#8338ec', '#06d6a0', '#ff006e', '#3a86ff', '#ef476f', '#118ab2', '#073b4c'];
  wordId: number;
  wordType: number;
  hits: any[];

  constructor(
    private primengConfig: PrimeNGConfig,
    private tokenStorageService: TokenStorageService,
    private titleService: Title,
    private router: Router,
    private sanitizer: DomSanitizer,
    private searchService: SearchService,
  ) {}

  ngOnInit(): void {
    this.titleService.setTitle('Почетна');
    this.primengConfig.ripple = true;
    this.searchService.selectedWordChanged.subscribe({
      next: (data: boolean) => {
        this.wordId = this.searchService.selectedWordId;
        this.wordType = this.searchService.selectedWordType;

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

  // @HostListener('document:click', ['$event'])
  // public handleClick(event: Event): void {
  //   let targetDiv = event.target;
  //   if (!(targetDiv instanceof HTMLDivElement))
  //     targetDiv = (targetDiv as HTMLElement).parentElement;
  //   if (targetDiv instanceof HTMLDivElement) {
  //     const element = targetDiv as HTMLDivElement;
  //     if (element.className === 'odrednica') {
  //       const odrednicaId = element?.getAttribute('data-id');
  //       if (odrednicaId) {
  //         this.router.navigate(['/edit', odrednicaId]);
  //       }
  //     }
  //   }
  // }

  // clear(table: Table, filter: HTMLInputElement): void {
  //   filter.value = '';
  //   table.clear();
  // }

  goto(odrId: number): void {
    this.router.navigate(['/edit', odrId]);
  }

  isLoggedIn(): boolean {
    return this.tokenStorageService.isLoggedIn();
  }
}
