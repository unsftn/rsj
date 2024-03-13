import { Component, OnInit, ViewChild } from '@angular/core';
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
  itemsAdmin: MenuItem[];
  searchWord: string;
  searchForm: string;
  searchResults: any[];
  username = '';
  headerStyle: string;
  caseSensitive: boolean;
  caseSensitiveLabel: string;
  caseSensitiveTooltip: string;

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

  isEditor(): boolean {
    if (!this.signedIn())
      return false;
    const groups = this.tokenStorageService.getUser().groups;
    return groups !== undefined && (groups.includes(1) || groups.includes(2));
  }

  isVolunteer(): boolean {
    if (!this.signedIn())
      return false;
    const groups = this.tokenStorageService.getUser().groups;
    if (groups === undefined)
      return false;
    return groups !== undefined && groups.includes(4);
  }

  signOut(): void {
    this.tokenStorageService.signOut();
    this.router.navigate(['/login']);
  }

  searchWords(): void {
    if (!this.searchWord)
      return;
    if (this.searchWord.charAt(0) === '~' && this.searchWord.length === 1)
      return;
    this.searchWord = this.searchWord.trim();
    const handler = {
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
    };
    if (this.searchWord.charAt(0) === '~') {
      this.searchService.searchSuffix(this.searchWord.substring(1)).subscribe(handler);
    } else {
      this.searchService.searchWords(this.searchWord).subscribe(handler);
    }
  }

  searchForms(event): void {
    const form = this.caseSensitive ? this.searchForm : this.searchForm.toLowerCase();
    this.searchWord = '';
    this.searchService.selectedWordId = null;
    this.searchService.selectedWordType = null;
    this.searchService.selectedWordForm = form;
    this.searchService.selectedWordChanged.emit(true);
    this.router.navigate(['/search'], { queryParams: { form: form, cs: this.caseSensitive}});
  }

  select(event): void {
    this.searchWord = '';
    this.searchForm = '';
    this.searchService.selectedWordId = event.value.pk;
    this.searchService.selectedWordType = event.value.vrsta;
    this.searchService.selectedWordForm = null;
    this.searchService.selectedWordChanged.emit(true);
    this.router.navigate(['/search'], { queryParams: { id: event.value.pk, type: event.value.vrsta }});
  }

  onKeyUp(event: KeyboardEvent): void {
    if (event.key === 'Enter')
      this.searchWords();
  }

  advanced(): void {
    this.router.navigate(['/pretraga']);
  }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
    this.caseSensitive = false;
    this.caseSensitiveLabel = 'aa';
    this.caseSensitiveTooltip = 'Велика и мала слова се не разликују';
    this.username = this.tokenStorageService.getUser()?.firstName ?? '';
    this.itemsUser = this.getUserMenu();
    this.itemsAdmin = this.getAdminMenu();
    this.itemsNew = this.getCreateMenu(); 
    this.tokenStorageService.loggedIn$.subscribe((loggedIn) => {
      this.username = loggedIn ? this.tokenStorageService.getUser().firstName : '';
      this.itemsUser = this.getUserMenu();
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

  getUserMenu(): any[] {
    return [
      {
        label: 'Пријава',
        icon: 'pi pi-sign-in',
        routerLink: ['/login'],
        disabled: this.signedIn(),
      },
      {
        label: 'Профил',
        icon: 'pi pi-user',
        routerLink: ['/profil'],
        disabled: !this.signedIn(),
      },
      {
        separator: true,
      },
      {
        label: 'Број унетих речи',
        icon: 'pi pi-sort-alpha-up',
        routerLink: ['/izvestaji/broj-unetih-reci'],
      },
      {
        label: 'Моје речи',
        icon: 'pi pi-heart',
        routerLink: ['/izvestaji/moje-reci'],
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
        disabled: !this.signedIn(),
      },
    ];
  }

  getAdminMenu(): MenuItem[] {
    return [
      {
        label: 'Одлуке за речник',
        icon: 'pi pi-thumbs-up',
        routerLink: ['/odluke'],
        disabled: !this.isAdmin() && !this.isEditor() && !this.isVolunteer(),
      },
      {
        label: 'Статистика одлука',
        icon: 'pi pi-chart-pie',
        routerLink: ['/izvestaji/statistika-odluka'],
        disabled: !this.isAdmin() && !this.isEditor() && !this.isVolunteer(),
      },
      {
        label: 'Речи у корпусу и/или речнику',
        icon: 'pi pi-arrow-right-arrow-left',
        routerLink: ['/izvestaji/korpus-recnik'],
        disabled: !this.isAdmin(),
      },
      {
        label: 'Број унетих речи',
        icon: 'pi pi-chart-bar',
        routerLink: ['/izvestaji/broj-unetih-reci'],
      },
      {
        label: 'Извори',
        icon: 'pi pi-book',
        routerLink: ['/izvori'],
        disabled: !this.isEditor(),
      },
      {
        label: 'Администрација',
        icon: 'pi pi-cog',
        command: (event: any) => {
          window.open('/admin', '_blank');
        },
        disabled: !this.isAdmin(),
      },
    ];
  }

  getCreateMenu(): MenuItem[] {
    return [
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
      {
        label: 'Заменица',
        routerLink: ['/zamenica/add']
      },
      {
        label: 'Број',
        routerLink: ['/broj/add']
      },
      {
        label: 'Прилог',
        routerLink: ['/prilog/add']
      },
    ];
  }

  toggle(): void {
    this.caseSensitive = !this.caseSensitive;
    this.caseSensitiveLabel = this.caseSensitive ? 'aA' : 'aa';
    this.caseSensitiveTooltip = this.caseSensitive ? 'Велика и мала слова се разликују' : 'Велика и мала слова се не разликују';
  }
}
