import { Component, OnInit, Input } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

@Component({
  selector: 'submeaning',
  templateUrl: './submeaning.component.html',
  styleUrls: ['./submeaning.component.scss'],
})
export class SubmeaningComponent implements OnInit {
  submeanings = [{ value: ' ' }];
  constructor(private primengConfig: PrimeNGConfig) {}

  add() {
    this.submeanings.push({ value: '' });
  }

  ngOnInit() {
    this.primengConfig.ripple = true;
  }
}
