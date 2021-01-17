import { Component, OnInit } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

@Component({
  selector: 'submeaning',
  templateUrl: './submeaning.component.html',
})
export class SubmeaningComponent implements OnInit {
  submeanings = [{ value: ' ' }];
  constructor(private primengConfig: PrimeNGConfig) {}

  add() {
    this.submeanings.push({ value: '' });
  }

  remove(submeaning) {
    this.submeanings.splice(this.submeanings.indexOf(submeaning), 1);
  }

  ngOnInit() {
    this.primengConfig.ripple = true;
  }
}
