import { Component, OnInit, Input } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

@Component({
  selector: 'meaningForm',
  templateUrl: './meaningForm.component.html',
  styleUrls: ['./meaningForm.component.scss'],
})
export class MeaningFormComponent implements OnInit {
  constructor(private primengConfig: PrimeNGConfig) {}

  meanings = [{ value: '' }];

  add() {
    this.meanings.push({ value: '' });
  }

  ngOnInit() {
    this.primengConfig.ripple = true;
  }
}
