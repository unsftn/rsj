import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

@Component({
  selector: 'antonym',
  templateUrl: './antonym.component.html',
})
export class AntonymComponent implements OnInit {
  constructor(
    private primengConfig: PrimeNGConfig,
  ) {}

  @Input() antonyms: any[];
  @Output() antonymsChange = new EventEmitter();

  onChange(): void {
    this.antonymsChange.emit();
  }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
  }
}
