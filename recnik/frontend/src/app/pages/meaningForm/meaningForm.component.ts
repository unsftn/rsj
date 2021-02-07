import { Component, OnInit, Input } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

@Component({
  selector: 'meaning',
  templateUrl: './meaningForm.component.html',
  styleUrls: ['./meaningForm.component.scss'],
})
export class MeaningFormComponent implements OnInit {
  constructor(private primengConfig: PrimeNGConfig) {}

  @Input() meanings: any[] = [];

  add(): void {
    this.meanings.push({ value: '', submeanings: [], qualificators: [], collocations: [], expressions: [] });
  }

  remove(meaning): void {
    this.meanings.splice(this.meanings.indexOf(meaning), 1);
  }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
  }
}
