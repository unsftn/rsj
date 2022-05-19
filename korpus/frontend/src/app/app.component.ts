import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MessageService, PrimeNGConfig, MenuItem } from 'primeng/api';
import { TokenStorageService } from './services/auth/token-storage.service';
import { AppConfigService } from './services/config/app-config.service';
import { SearchService } from './services/search/search.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  providers: [MessageService],
})
export class AppComponent implements OnInit {
  title = 'korpus';
  itemsUser: MenuItem[];
  itemsNew: MenuItem[];
  searchWord: string;
  searchForm: string;
  searchResults: any[];
  username = '';
  headerStyle: string;

  constructor(
    private primengConfig: PrimeNGConfig,
    private tokenStorageService: TokenStorageService,
    private messageService: MessageService,
    private appConfigService: AppConfigService,
    private router: Router,
    private searchService: SearchService,
  ) {}

  signedIn(): boolean {
    return this.tokenStorageService.getUser() !== null;
  }

  isAdmin(): boolean {
    if (!this.signedIn())
      return false;
    return this.tokenStorageService.getUser().isStaff;
  }

  signOut(): void {
    this.tokenStorageService.signOut();
    this.router.navigate(['/']);
  }

  searchWords(event): void {
    this.searchService.searchWords(event.query).subscribe({
      next: (data) => {
        this.searchResults = data;
      },
      error: (error) => {
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

  searchForms(event): void {
    this.searchWord = '';
    this.searchService.selectedWordId = null;
    this.searchService.selectedWordType = null;
    this.searchService.selectedWordForm = this.searchForm.toLowerCase();
    this.searchService.selectedWordChanged.emit(true);
    this.router.navigate(['/']);
  }

  select(value): void {
    this.searchWord = '';
    this.searchForm = '';
    this.searchService.selectedWordId = value.pk;
    this.searchService.selectedWordType = value.vrsta;
    this.searchService.selectedWordForm = null;
    this.searchService.selectedWordChanged.emit(true);
    this.router.navigate(['/']);
  }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
    this.username = this.tokenStorageService.getUser()?.firstName ?? '';
    this.itemsUser = [
      {
        label: 'Пријава',
        icon: 'pi pi-sign-in',
        routerLink: ['/login'],
        disabled: this.signedIn(),
      },
      {
        label: 'Профил',
        icon: 'pi pi-user',
        routerLink: ['/profile'],
        disabled: !this.signedIn(),
      },
      {
        separator: true,
      },
      {
        label: 'Публикације',
        icon: 'pi pi-book',
        routerLink: ['/publikacije'],
      },
      {
        separator: true,
      },
      {
        label: 'Администрација',
        icon: 'pi pi-cog',
        command: (event: any) => {
          window.open('/admin', '_blank');
        },
      },
      {
        separator: true,
      },
      {
        label: 'Одјава',
        icon: 'pi pi-sign-out',
        command: (event: any) => {
          this.signOut();
        },
      },
    ];
    this.itemsNew = [
      {
        label: 'Именица',
        routerLink: ['/imenica/add']
      },
      {
        label: 'Глагол',
        routerLink: ['/glagol/add']
      },
      {
        label: 'Придев',
        routerLink: ['/pridev/add']
      },
      {
        label: 'Предлог',
        routerLink: ['/predlog/add']
      },
      {
        label: 'Речца',
        routerLink: ['/recca/add']
      },
      {
        label: 'Узвик',
        routerLink: ['/uzvik/add']
      },
      {
        label: 'Везник',
        routerLink: ['/veznik/add']
      },
    ];
    this.tokenStorageService.loggedIn$.subscribe((loggedIn) => {
      this.username = loggedIn ? this.tokenStorageService.getUser().firstName : '';
    });
    this.appConfigService.getAppConfig().subscribe({
      next: (data) => {
        this.headerStyle = data.HEADER_COLOR_SCHEME;
      }, 
      error: (error) => {
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
