import { Component, OnInit, Output, EventEmitter, Input } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

interface Collocation {
  note: string;
  determinants: any[];
}

@Component({
  selector: 'collocations',
  templateUrl: './collocations.component.html',
  styleUrls: ['./collocations.component.scss'],
})
export class CollocationsComponent implements OnInit {
  @Input() collocations: Collocation[];

  constructor(private primengConfig: PrimeNGConfig) {}

  add(): void {
    this.collocations.push({ determinants: [], note: '' });
  }

  remove(index: number): void {
    this.collocations.splice(index, 1);
  }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
  }
}
