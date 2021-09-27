import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MessageService, PrimeNGConfig, MenuItem } from 'primeng/api';
import { TokenStorageService } from './services/auth/token-storage.service';
import { UserService } from './services/auth/user.service';
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
  searchText: string;
  searchResults: any[];
  username = '';
  headerStyle: string;

  constructor(
    private primengConfig: PrimeNGConfig,
    private tokenStorageService: TokenStorageService,
    private userService: UserService,
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

  search(event): void {
    this.searchService.search(event.query).subscribe(
      (data) => {
        this.searchResults = data;
      },
      (error) => {
        console.log(error);
      });
  }

  select(value): void {
    this.searchText = '';
    let url = '/imenica';
    switch (value.vrsta) {
      case 0: url = '/imenica'; break;
      case 1: url = '/glagol'; break;
      case 2: url = '/pridev'; break;
      case 3: url = '/prilog'; break;
      case 4: url = '/predlog'; break;
      case 5: url = '/zamenica'; break;
      case 6: url = '/uzvik'; break;
      case 7: url = '/recca'; break;
      case 8: url = '/veznik'; break;
      case 9: url = '/broj'; break;
      case 10: url = '/ostalo'; break;
    }
    this.router.navigate([url, value.pk]);
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
        label: 'Одјава',
        icon: 'pi pi-sign-out',
        command: (event: any) => {
          this.signOut();
        },
        disabled: !this.signedIn(),
      },
    ];
    this.itemsNew = [
      {
        label: 'Именица',
        routerLink: ['/imenica/add'],
        disabled: !this.signedIn(),
      },
    ];
    this.tokenStorageService.loggedIn$.subscribe((loggedIn) => {
      this.username = loggedIn ? this.tokenStorageService.getUser().firstName : '';
      this.itemsUser.forEach((item, index) => {
        if (item.separator)
          return;
        if (index === 0)
          item.disabled = loggedIn;
        else
          item.disabled = !loggedIn;
      });
      this.itemsNew.forEach((item, index) => {
        if (item.separator)
          return;
        if (index === 0)
          item.disabled = loggedIn;
        else
          item.disabled = !loggedIn;
      });
    });
    this.appConfigService.getAppConfig().subscribe(data => {
      this.headerStyle = data.HEADER_COLOR_SCHEME;
    }, error => {
      console.log(error);
    });
  }
}
