import { Component, Input, OnInit } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

@Component({
  selector: 'submeaning',
  templateUrl: './submeaning.component.html',
})
export class SubmeaningComponent implements OnInit {

  @Input() submeanings;

  constructor(private primengConfig: PrimeNGConfig) {}

  add(): void {
    this.submeanings.push({ value: '', qualificators: [], expressions: [], concordances: [] });
  }

  remove(submeaning): void {
    this.submeanings.splice(this.submeanings.indexOf(submeaning), 1);
  }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
  }
}
