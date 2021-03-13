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

  constructor(
    private primengConfig: PrimeNGConfig,
    private tokenStorageService: TokenStorageService,
    private qualificatorService: QualificatorService,
    private odrednicaService: OdrednicaService,
    private publikacijaService: PublikacijaService,
    private router: Router,
  ) {}

  signedIn(): boolean {
    return this.tokenStorageService.getUser() != null;
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
    this.items = [
      {
        label: 'Пријава',
        icon: 'pi pi-sign-in',
        routerLink: ['/login'],
      },
      {
        label: 'Профил',
        icon: 'pi pi-user',
      },
      {
        separator: true,
      },
      {
        label: 'Рендери',
        icon: 'pi pi-book',
        url: '/renders',
      },
      {
        label: 'Публикације',
        icon: 'pi pi-bookmark',
        url: '/pubs',
      },
      {
        separator: true,
      },
      {
        label: 'Администрација',
        icon: 'pi pi-cog',
        url: '/admin',
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
    this.qualificatorService.fetchAllQualificators();
    this.publikacijaService.fetchAllPubTypes();
  }
}
