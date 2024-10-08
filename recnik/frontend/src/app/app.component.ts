import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MessageService, PrimeNGConfig, MenuItem } from 'primeng/api';
import { TokenStorageService } from './services/auth/token-storage.service';
import { UserService } from './services/auth/user.service';
import { OdrednicaService, QualificatorService } from './services/odrednice';
import { PublikacijaService } from './services/publikacije';
import { AppConfigService } from './services/config/app-config.service';
import { PodvrstaReciService } from './services/odrednice/podvrsta-reci.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  providers: [MessageService],
})
export class AppComponent implements OnInit {
  title = 'recnik';
  items: MenuItem[];
  searchText: string;
  searchResults: any[];
  username = '';
  headerStyle: string;

  constructor(
    private primengConfig: PrimeNGConfig,
    private tokenStorageService: TokenStorageService,
    private qualificatorService: QualificatorService,
    private odrednicaService: OdrednicaService,
    private publikacijaService: PublikacijaService,
    private podvrstaReciService: PodvrstaReciService,
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
    this.router.navigate(['/login']);
  }

  search(event): void {
    this.odrednicaService.search(event.query).subscribe({
      next: (data) => {
        this.searchResults = data;
      },
      error: (error) => {
        console.log(error);
      }
    });
  }

  select(event): void {
    this.searchText = '';
    this.router.navigate(['/edit', event.value.pk]);
  }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
    const user = this.tokenStorageService.getUser();
    this.username = (user === null) ? '' : (( 'firstName' in user ? user.firstName : ''));
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
        label: 'Рендери',
        icon: 'pi pi-book',
        routerLink: ['/renders'],
        disabled: !this.signedIn(),
      },
      {
        separator: true,
      },
      {
        label: 'Администрација',
        icon: 'pi pi-cog',
        url: '/admin',
        disabled: !this.isAdmin(),
      },
      {
        label: 'Прегледи',
        icon: 'pi pi-fw pi-calendar',
        disabled: !this.isAdmin(),
        items: [
          {
            label: 'Са напоменом',
            icon: 'pi pi-flag',
            routerLink: ['/review/with-notes'],
          },
          {
            label: 'По обрађивачу',
            icon: 'pi pi-users',
            routerLink: ['/review/by-person'],
          },
          {
            label: 'Азбучни преглед',
            icon: 'pi pi-sort-alpha-up',
            routerLink: ['/review/alphabetical'],
          },
        ]
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
    this.qualificatorService.fetchAllQualificators().subscribe((values) => {});
    this.podvrstaReciService.fetchAllPodvrsta().subscribe(() => {});
    // this.publikacijaService.fetchAllPubTypes().subscribe((values) => {});
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
    this.appConfigService.getAppConfig().subscribe({
      next: (data) => {
        const user = this.tokenStorageService.getUser();
        if (user?.firstName === 'Дејан' && user?.lastName === 'Милорадов')
          this.headerStyle = 'gray';
        else
          this.headerStyle = data.HEADER_COLOR_SCHEME;
      }, 
      error: (error) => {
        this.headerStyle = 'purple';
        //console.log(error);
      }
    });
    this.odrednicaService.getStatuses().subscribe(() => {});
  }
}
