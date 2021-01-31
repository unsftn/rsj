import { Component, OnInit } from '@angular/core';
import { Injectable } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';
import { Router } from '@angular/router';

declare var $: any;

@Component({
  selector: 'home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
@Injectable({ providedIn: 'root' })
export class HomeComponent implements OnInit {

  selection = '';

  constructor(private primengConfig: PrimeNGConfig, private router: Router) {}

  ngOnInit(): void {
    this.primengConfig.ripple = true;
    $('fieldset p').lettering('lines');
  }

  onClick(event: MouseEvent) {
    let element = event.target as HTMLElement;
    if (element.className.startsWith('line'))
      this.router.navigate(['tekst/1']);
  }
}
