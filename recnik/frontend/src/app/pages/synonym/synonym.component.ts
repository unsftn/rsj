import { Component, Input, OnInit, Output, EventEmitter } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

@Component({
  selector: 'synonym',
  templateUrl: './synonym.component.html',
})
export class SynonymComponent implements OnInit {
  constructor(
    private primengConfig: PrimeNGConfig,
  ) {}

  @Input() synonyms;
  @Output() synonymsChange = new EventEmitter();

  onChange(): void {
    this.synonymsChange.emit();
  }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
  }
}
