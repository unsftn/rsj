import { Component, Injectable, HostListener, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { PrimeNGConfig } from 'primeng/api';
import { Table } from 'primeng/table';
import { TokenStorageService } from '../../services/auth/token-storage.service';
import { Title } from '@angular/platform-browser';

class UserCollection extends Array {
  sum(key): number {
    return this.reduce((a, b) => a + (b[key] || 0), 0);
  }
}

@Component({
  selector: 'home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
@Injectable({providedIn: 'root'})
export class HomeComponent implements OnInit {

  users: UserCollection;
  colors = ['#ffbe0b', '#fb5607', '#8338ec', '#06d6a0', '#ff006e', '#3a86ff', '#ef476f', '#118ab2', '#073b4c'];

  constructor(
    private primengConfig: PrimeNGConfig,
    private tokenStorageService: TokenStorageService,
    private titleService: Title,
    private router: Router) {}

  ngOnInit(): void {
    this.titleService.setTitle('Почетна');
    this.primengConfig.ripple = true;
  }

  // @HostListener('document:click', ['$event'])
  // public handleClick(event: Event): void {
  //   let targetDiv = event.target;
  //   if (!(targetDiv instanceof HTMLDivElement))
  //     targetDiv = (targetDiv as HTMLElement).parentElement;
  //   if (targetDiv instanceof HTMLDivElement) {
  //     const element = targetDiv as HTMLDivElement;
  //     if (element.className === 'odrednica') {
  //       const odrednicaId = element?.getAttribute('data-id');
  //       if (odrednicaId) {
  //         this.router.navigate(['/edit', odrednicaId]);
  //       }
  //     }
  //   }
  // }

  clear(table: Table, filter: HTMLInputElement): void {
    filter.value = '';
    table.clear();
  }

  goto(odrId: number): void {
    this.router.navigate(['/edit', odrId]);
  }

  isLoggedIn(): boolean {
    return this.tokenStorageService.isLoggedIn();
  }
}
