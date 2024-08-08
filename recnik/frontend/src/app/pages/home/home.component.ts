import { Component, Injectable, HostListener, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { PrimeNGConfig } from 'primeng/api';
import { Table } from 'primeng/table';
import { OdrednicaService } from '../../services/odrednice';
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

  myDeterminants: any[];
  nobodysDeterminants: any[];
  odredniceZaProbnuSvesku: any[];
  users: UserCollection;
  graphDataChars = {
    labels: [],
    datasets: []
  };
  graphDataDeterminants = {
    labels: [],
    datasets: []
  };
  graphDataLetters = {
    labels: ['А', 'Б', 'В', 'Г', 'Д', 'Ђ', 'Е', 'Ж', 'З', 'И', 'Ј', 'К', 'Л', 'Љ', 'М', 'Н', 'Њ', 'О', 'П', 'Р', 'С', 'Т', 'Ћ', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Џ', 'Ш'],
    datasets: [{
      data: [],
      backgroundColor: '#42A5F5'
    }]
  };
  optionsNoLegend = { plugins: { legend: { display: false } } };
  colors = ['#ffbe0b', '#fb5607', '#8338ec', '#06d6a0', '#ff006e', '#3a86ff', '#ef476f', '#118ab2', '#073b4c'];

  constructor(
    private primengConfig: PrimeNGConfig,
    private odrednicaService: OdrednicaService,
    private tokenStorageService: TokenStorageService,
    private titleService: Title,
    private router: Router) {}

  ngOnInit(): void {
    this.titleService.setTitle('Речник');
    this.primengConfig.ripple = true;
    this.odrednicaService.my(200).subscribe({
      next: (data) => this.myDeterminants = data,
      error: (error) => console.log(error)
    });
    this.odrednicaService.nobodys(1000).subscribe({
      next: (data) => {
        this.nobodysDeterminants = data;
        const indexOfNobody = this.nobodysDeterminants.map((item) => item.id).indexOf(null);
        this.nobodysDeterminants.push(this.nobodysDeterminants.splice(indexOfNobody, 1)[0]);
      },
      error: (error) => console.log(error)
    });
    this.odrednicaService.statObradjivaca().subscribe({
      next: (data) => {
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
      error: (error) => console.log(error)
    });
    this.odrednicaService.grafikon(1).subscribe({
      next: (data) => {
        this.graphDataChars = data;
        this.graphDataChars.datasets.forEach((dataset, index) => {
          dataset.data = dataset.data.map(item => item.broj_znakova);
          dataset.borderColor = this.colors[index % this.colors.length];
          dataset.fill = false;
        });
      }, 
      error: (error) => console.log(error)
    });
    this.odrednicaService.grafikon(1).subscribe({
      next: (data) => {
        this.graphDataDeterminants = data;
        this.graphDataDeterminants.datasets.forEach((dataset, index) => {
          dataset.data = dataset.data.map(item => item.broj_odrednica);
          dataset.borderColor = this.colors[index % this.colors.length];
          dataset.fill = false;
        });
      }, 
      error: (error) => console.log(error)
    });
    this.odrednicaService.grafikon(9).subscribe({
      next: (data) => {
        this.graphDataLetters = {
          labels: ['А', 'Б', 'В', 'Г', 'Д', 'Ђ', 'Е', 'Ж', 'З', 'И', 'Ј', 'К', 'Л', 'Љ', 'М', 'Н', 'Њ', 'О', 'П', 'Р', 'С', 'Т', 'Ћ', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Џ', 'Ш'],
          datasets: [{
            data,
            backgroundColor: '#42A5F5'
          }]
        };
      }, 
      error: (error) => console.log(error)
    });
    this.odrednicaService.odredniceZaStatus(9).subscribe({
      next: (data) => {
        this.odredniceZaProbnuSvesku = data.map((item) => { 
          switch (item.stanje) {
            case 1: item.stanje_text = 'у обради'; break;
            case 2: item.stanje_text = 'код редактора'; break;
            case 3: item.stanje_text = 'код уредника'; break;
            case 4: item.stanje_text = 'затворена'; break;
          }
          return item;
        });
      },
      error: (error) => {console.log(error)}
    });
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

  isLoggedIn(): boolean {
    return this.tokenStorageService.isLoggedIn();
  }
}
