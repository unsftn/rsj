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

  determinants: string[];
  selectedDeterminant: string;
  filteredDeterminants: any[];

  add(): void {
    this.antonyms.push({ determinantId: null, searchText: '', rec$: of('') });
  }

  remove(index: number): void {
    this.antonyms.splice(index, 1);
  }

  ngOnInit() {
    this.primengConfig.ripple = true;
  }
}
