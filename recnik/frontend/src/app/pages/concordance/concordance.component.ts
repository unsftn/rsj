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

  showQuotesDialog = false;
  caretPos: number;
  caretIndex: number;
  caretTarget: HTMLTextAreaElement;

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

  insertQuote(char: string): void {
    const text = this.concordances[this.caretIndex].concordance;
    const newText = text.slice(0, this.caretPos) + char + text.slice(this.caretPos);
    this.concordances[this.caretIndex].concordance = newText;
    this.showQuotesDialog = false;
    this.caretTarget.focus();
    setTimeout(() => {this.caretTarget.setSelectionRange(this.caretPos + 1, this.caretPos + 1, 'none')});
  }

  keyup(event, index: number): void {
    if (event.key === 'F1') {
      this.caretPos = event.target.selectionStart;
      this.caretIndex = index;
      this.caretTarget = event.target;
      this.showQuotesDialog = true;
    }
  }
}
