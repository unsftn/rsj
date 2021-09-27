import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MessageService, PrimeNGConfig, MenuItem } from 'primeng/api';
import { TokenStorageService } from './services/auth/token-storage.service';
import { UserService } from './services/auth/user.service';
import { AppConfigService } from './services/config/app-config.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  providers: [MessageService],
})
export class AppComponent implements OnInit {
  title = 'korpus';
  items: MenuItem[];
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
    // TODO: search reci
  }

  select(value): void {
    this.searchText = '';
    this.router.navigate(['/edit', value.pk]);
  }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
    this.username = this.tokenStorageService.getUser()?.firstName ?? '';
    this.items = [
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
    this.userService.fetchKorisnici().subscribe(() => {});
    this.tokenStorageService.loggedIn$.subscribe((loggedIn) => {
      this.username = loggedIn ? this.tokenStorageService.getUser().firstName : '';
      this.items.forEach((item, index) => {
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
