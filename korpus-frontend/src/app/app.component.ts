import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { PrimeNGConfig, MenuItem, MessageService } from 'primeng/api';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  providers: [MessageService],
})
export class AppComponent implements OnInit {
  title = 'korpus-frontend';
  items: MenuItem[];

  constructor(
    private primengConfig: PrimeNGConfig,
    private router: Router
  ) {}

  signedIn(): boolean {
    // TODO
    return true;
  }

  signOut(): void {
    // TODO
    this.router.navigate(['/']);
  }

  ngOnInit() {
    this.primengConfig.ripple = true;
    this.items = [
      {
        label: 'Пријава',
        icon: 'pi pi-sign-in',
        //routerLink: ['/login'],
      },
      {
        label: 'Профил',
        icon: 'pi pi-user',
        //routerLink: ['/profile'],
      },
      {
        separator: true,
      },
      {
        label: 'Администрација',
        icon: 'pi pi-cog',
        //routerLink: ['/admin'],
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
