import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MessageService, PrimeNGConfig, MenuItem } from 'primeng/api';
import { TokenStorageService } from './services/auth/token-storage.service';
import { OdrednicaService, QualificatorService } from './services/odrednice';
import { PublikacijaService } from './services/publikacije';

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

  constructor(
    private primengConfig: PrimeNGConfig,
    private tokenStorageService: TokenStorageService,
    private qualificatorService: QualificatorService,
    private odrednicaService: OdrednicaService,
    private publikacijaService: PublikacijaService,
    private router: Router,
  ) {}

  signedIn(): boolean {
    return this.tokenStorageService.getUser() !== null;
  }

  signOut(): void {
    this.tokenStorageService.signOut();
    this.router.navigate(['/']);
  }

  search(event): void {
    this.odrednicaService.search(event.query).subscribe(
      (data) => {
        this.searchResults = data;
      },
      (error) => {
        console.log(error);
      }
    );
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
        label: 'Публикације',
        icon: 'pi pi-bookmark',
        routerLink: ['/pubs'],
        disabled: !this.signedIn(),
      },
      {
        separator: true,
      },
      {
        label: 'Администрација',
        icon: 'pi pi-cog',
        url: '/admin',
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
    this.qualificatorService.fetchAllQualificators().subscribe((values) => {});
    this.publikacijaService.fetchAllPubTypes().subscribe((values) => {});
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
  }
}
