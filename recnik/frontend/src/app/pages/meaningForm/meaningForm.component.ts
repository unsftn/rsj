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

  remove(meaning) {
    this.meanings.splice(this.meanings.indexOf(meaning), 1);
  }

  ngOnInit() {
    this.primengConfig.ripple = true;
  }
}
