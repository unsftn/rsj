import { Component, OnInit, Input } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

interface Concordance {
  concordance: string;
  book?: string;
  // pageNumber: number;
}

@Component({
  selector: 'concordance',
  templateUrl: './concordance.component.html',
  styleUrls: ['./concordance.component.scss'],
})
export class ConcordanceComponent implements OnInit {
  constructor(private primengConfig: PrimeNGConfig) {}

  @Input() concordances;
  books = [];

  add(): void {
    console.log(this.concordances);
    this.concordances.push({ concordance: '', book: this.books[0] });
  }

  remove(concordance): void {
    this.concordances.splice(this.concordances.indexOf(concordance), 1);
  }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
    this.books = ['Књига 1', 'Књига 2', 'Књига 3'];
  }
}
