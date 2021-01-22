import { Component, OnInit } from '@angular/core';
import { Injectable } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

declare var $: any;

@Component({
  selector: 'home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
@Injectable({ providedIn: 'root' })
export class HomeComponent implements OnInit {

  selection = '';

  constructor(private primengConfig: PrimeNGConfig) {}

  ngOnInit(): void {
    this.primengConfig.ripple = true;
    $('fieldset p').lettering('lines');
  }

  onClick(event: MouseEvent) {
    let element = event.target as HTMLElement;
    if (element.nodeName.toLowerCase() === 'span' && element.parentNode.nodeName.toLowerCase() === 'p')
      this.selection = (event.target as HTMLElement).textContent;
  }
}
