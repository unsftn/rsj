import { Component, OnInit, Input, OnChanges, SimpleChanges, Output, EventEmitter } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';
import { of } from 'rxjs';
import { PublikacijaService } from '../../services/publikacije';

interface Concordance {
  concordance: string;
  bookId?: number;
  searchText: string;
}

@Component({
  selector: 'concordance',
  templateUrl: './concordance.component.html',
  styleUrls: ['./concordance.component.scss'],
})
export class ConcordanceComponent implements OnInit, OnChanges {
  constructor(private primengConfig: PrimeNGConfig, private publikacijaService: PublikacijaService) {}

  @Input() concordances;
  @Output() concordancesChange = new EventEmitter();

  showQuotesDialog = false;
  caretPos: number;
  caretIndex: number;
  caretTarget: HTMLTextAreaElement;
  searchResults: any[];
  dirty: boolean;

  add(): void {
    this.concordances.push({ concordance: '', bookId: null, searchText: '', naslov$: of(''), skracenica$: of('') });
    this.concordancesChange.emit();
  }

  remove(concordance): void {
    this.concordances.splice(this.concordances.indexOf(concordance), 1);
    this.concordancesChange.emit();
  }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
    this.dirty = false;
  }

  ngOnChanges(changes: SimpleChanges): void {
    this.concordances.forEach((c) => {
      if (c.bookId)
        this.publikacijaService.get(c.bookId).subscribe((pub) => {
          c.naslov$ = of(pub.naslov);
          c.skracenica$ = of(pub.skracenica);
        });
      });
  }

  insertQuote(char: string): void {
    const text = this.concordances[this.caretIndex].concordance;
    const newText = text.slice(0, this.caretPos) + char + text.slice(this.caretPos);
    this.concordances[this.caretIndex].concordance = newText;
    this.showQuotesDialog = false;
    this.caretTarget.focus();
    setTimeout(() => { this.caretTarget.setSelectionRange(this.caretPos + 1, this.caretPos + 1, 'none')});
  }

  keyup(event, index: number): void {
    if (event.key === 'F1') {
      this.caretPos = event.target.selectionStart;
      this.caretIndex = index;
      this.caretTarget = event.target;
      this.showQuotesDialog = true;
    }
  }

  search(event): void {
    this.publikacijaService.search(event.query).subscribe(
      (data) => {
        this.searchResults = data;
      },
      (error) => {
        console.log(error);
      }
    );
  }

  select(event, index): void {
    this.concordances[index].bookId = event.pk;
    this.publikacijaService.get(event.pk).subscribe((pub) => {
      this.concordances[index].naslov$ = of(pub.naslov);
      this.concordances[index].skracenica$ = of(pub.skracenica);
    });
    this.concordances[index].searchText = '';
    this.concordancesChange.emit();
  }

  removePub(concordance): void {
    concordance.bookId = null;
    concordance.naslov$ = of('');
    concordance.skracenica$ = of('');
    this.concordancesChange.emit();
  }

  onValueChange(value: any): void {
    this.dirty = true;
  }

  onFocusLeave(): void {
    if (this.dirty) {
      this.dirty = false;
      this.concordancesChange.emit();
    }
  }
}
