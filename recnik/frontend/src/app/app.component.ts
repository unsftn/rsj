import { Component } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';
import {MenuItem} from 'primeng/api';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'recnik';

  items: MenuItem[];

  constructor(private primengConfig: PrimeNGConfig) {}

  ngOnInit() {
    this.primengConfig.ripple = true;
    this.items = [
      {
          label: 'Sign in',
          icon: 'pi pi-plus'
      },
      {
          label: 'Profil',
          icon: 'pi pi-users',
      },
      {
        separator:true
      },
      {
        label: 'Log out',
        icon: 'pi pi-sign-out'
      },
  ];
  }
}
