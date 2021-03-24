import { Component, Input, OnInit } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';
import { of } from 'rxjs';

@Component({
  selector: 'antonym',
  templateUrl: './antonym.component.html',
})
export class AntonymComponent implements OnInit {
  constructor(
    private primengConfig: PrimeNGConfig,
  ) {}

  @Input() antonyms: any[];

  ngOnInit(): void {
    this.primengConfig.ripple = true;
  }
}
