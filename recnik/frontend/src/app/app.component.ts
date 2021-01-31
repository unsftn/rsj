import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MessageService, PrimeNGConfig, MenuItem } from 'primeng/api';
import { TokenStorageService } from './services/auth/token-storage.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  providers: [MessageService],
})
export class AppComponent implements OnInit {
  title = 'recnik';

  items: MenuItem[];

  constructor(
    private primengConfig: PrimeNGConfig,
    private tokenStorageService: TokenStorageService,
    private router: Router,
  ) {}

  signedIn(): boolean {
    return this.tokenStorageService.getUser() != null;
  }

  signOut(): void {
    this.tokenStorageService.signOut();
    this.router.navigate(['/']);
  }

  ngOnInit() {
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
  }
}
