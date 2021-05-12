import { Component, Injectable, HostListener, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { PrimeNGConfig } from 'primeng/api';
import { Table } from 'primeng/table';
import { OdrednicaService } from '../../services/odrednice';

@Component({
  selector: 'home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
@Injectable({providedIn: 'root'})
export class HomeComponent implements OnInit {

  // data1 = {
  //   labels: ['именице', 'глаголи', 'придеви', 'прилози', 'заменице', 'речце', 'узвици', 'предлози', 'везници', 'бројеви'],
  //   datasets: [{
  //     data: [75, 82, 49, 12, 11, 7, 9, 12, 5, 8],
  //     backgroundColor: ['#AA3939', '#AA6C39', '#2D882D', '#226666', '#FFAAAA', '#552700', '#88CC88', '#003333', '#D46A6A', '#804515']
  //   }],
  // };
  // options1 = {
  //   title: { display: true, text: 'Број одредница по врсти речи [fake]', fontSize: 16, fontFamily: 'Fira Sans', fontColor: '#999b9b' },
  //   legend: { position: 'left', labels: { fontFamily: 'Fira Sans' } },
  //   tooltips: { bodyFontFamily: 'Fira Sans' },
  // };
  // data2 = {
  //   labels: ['2021-01-01', '2021-01-08', '2021-01-15', '2021-01-22', '2021-01-29', '2021-02-05', '2021-02-12'],
  //   datasets: [{
  //     label: 'Број унетих одредница по недељи [fake]',
  //     data: [28, 34, 45, 51, 72, 84, 95],
  //     fill: true,
  //     borderColor: '#AA3939'
  //   }],
  // };
  // options2 = {
  //   legend: { labels: { fontColor: '#999b9b', fontFamily: 'Fira Sans', fontSize: 16 } },
  //   scales: {
  //     xAxes: [{
  //       ticks: { fontColor: '#999b9b', fontFamily: 'Fira Sans' },
  //       gridLines: { color: 'rgba(255,255,255,0.4)' }
  //     }],
  //     yAxes: [{
  //       ticks: { fontColor: '#999b9b', fontFamily: 'Fira Sans' },
  //       gridLines: { color: 'rgba(255,255,255,0.4)' }
  //     }]
  //   }
  // };
  //
  // data3 = {
  //   labels: ['2021-01-01', '2021-01-08', '2021-01-15', '2021-01-22', '2021-01-29', '2021-02-05', '2021-02-12'],
  //   datasets: [{
  //     label: 'Број конкорданци по недељи [fake]',
  //     data: [28, 34, 45, 51, 72, 84, 95],
  //     fill: true,
  //     borderColor: '#2D882D'
  //   }],
  // };
  // options3 = {
  //   legend: { labels: { fontColor: '#999b9b', fontFamily: 'Fira Sans', fontSize: 16 } },
  //   scales: {
  //     xAxes: [{
  //       ticks: { fontColor: '#999b9b', fontFamily: 'Fira Sans' },
  //       gridLines: { color: 'rgba(255,255,255,0.4)' }
  //     }],
  //     yAxes: [{
  //       ticks: { fontColor: '#999b9b', fontFamily: 'Fira Sans' },
  //       gridLines: { color: 'rgba(255,255,255,0.4)' }
  //     }]
  //   }
  // };

  myDeterminants: any[];
  users: any[] = [];

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
      (data) => this.users = data,
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
