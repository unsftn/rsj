import { Component, Input, OnInit } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

@Component({
  selector: 'submeaning',
  templateUrl: './submeaning.component.html',
})
export class SubmeaningComponent implements OnInit {

  @Input() submeanings = [{ value: '', qualificators: [], collocations: [], expressions: [] }];

  constructor(private primengConfig: PrimeNGConfig) {}

  add(): void {
    this.submeanings.push({ value: '', qualificators: [], collocations: [], expressions: []  });
  }

  remove(submeaning): void {
    this.submeanings.splice(this.submeanings.indexOf(submeaning), 1);
  }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
  }
}
