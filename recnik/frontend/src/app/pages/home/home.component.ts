import { Component, Injectable, HostListener, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { PrimeNGConfig } from 'primeng/api';
import { Table } from 'primeng/table';
import { OdrednicaService } from '../../services/odrednice';

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

  myDeterminants: any[];
  users: UserCollection;

  constructor(
    private primengConfig: PrimeNGConfig,
    private odrednicaService: OdrednicaService,
    private router: Router) {}

  ngOnInit(): void {
    this.primengConfig.ripple = true;
    this.odrednicaService.my(100).subscribe(
      (data) => this.myDeterminants = data,
      (error) => console.log(error)
    );
    this.odrednicaService.statObradjivaca().subscribe(
      (data) => {
        this.users = new UserCollection(...data);
        this.users.push({
          first_name: 'УКУПНО',
          last_name: '',
          broj_odrednica: this.users.sum('broj_odrednica'),
          broj_znakova: this.users.sum('broj_znakova'),
          zavrsenih_odrednica: this.users.sum('zavrsenih_odrednica'),
          zavrsenih_znakova: this.users.sum('zavrsenih_znakova'),
        });
      },
      (error) => console.log(error)
    );
  }

  @HostListener('document:click', ['$event'])
  public handleClick(event: Event): void {
    let targetDiv = event.target;
    if (!(targetDiv instanceof HTMLDivElement))
      targetDiv = (targetDiv as HTMLElement).parentElement;
    if (targetDiv instanceof HTMLDivElement) {
      const element = targetDiv as HTMLDivElement;
      if (element.className === 'odrednica') {
        const odrednicaId = element?.getAttribute('data-id');
        if (odrednicaId) {
          this.router.navigate(['/edit', odrednicaId]);
        }
      }
    }
  }

  clear(table: Table, filter: HTMLInputElement): void {
    filter.value = '';
    table.clear();
  }

  goto(odrId: number): void {
    this.router.navigate(['/edit', odrId]);
  }
}
