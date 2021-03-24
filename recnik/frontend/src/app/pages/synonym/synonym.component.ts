import { Component, Input, OnInit } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';
import { of } from 'rxjs';
import { OdrednicaService } from '../../services/odrednice';

@Component({
  selector: 'synonym',
  templateUrl: './synonym.component.html',
})
export class SynonymComponent implements OnInit {
  constructor(
    private primengConfig: PrimeNGConfig,
    private odrednicaService: OdrednicaService,
  ) {}

  @Input() synonyms;

  add(): void {
    this.synonyms.push({ determinantId: null, searchText: '', rec$: of('') });
  }

  remove(index: number): void {
    this.synonyms.splice(index, 1);
  }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
  }
}
