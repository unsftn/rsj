import { Component, Injectable, HostListener, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { PrimeNGConfig } from 'primeng/api';

@Component({
  selector: 'home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
@Injectable({providedIn: 'root'})
export class HomeComponent implements OnInit {
  constructor(private primengConfig: PrimeNGConfig, private router: Router) {
  }

  ngOnInit() {
    this.primengConfig.ripple = true;
  }

  @HostListener('document:click', ['$event'])
  public handleClick(event: Event): void {
    if (event.target instanceof HTMLDivElement) {
      const element = event.target as HTMLDivElement;
      if (element.className === 'odrednica') {
        const odrednicaId = element?.getAttribute('data-id');
        if (odrednicaId) {
          this.router.navigate(['/edit', odrednicaId]);
        }
      }
    }
  }
}
