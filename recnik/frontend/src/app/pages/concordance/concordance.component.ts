import { Component, OnInit, Input, OnChanges, SimpleChanges, Output, EventEmitter } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';
import { of } from 'rxjs';
import { PublikacijaService, KorpusService } from '../../services/publikacije';

@Component({
  selector: 'concordance',
  templateUrl: './concordance.component.html',
  styleUrls: ['./concordance.component.scss'],
})
export class ConcordanceComponent implements OnInit, OnChanges {
  constructor(
    private primengConfig: PrimeNGConfig, 
    private publikacijaService: PublikacijaService,
    private korpusService: KorpusService) {}

  @Input() concordances;
  @Output() concordancesChange = new EventEmitter();

  showQuotesDialog = false;
  caretPos: number;
  caretIndex: number;
  caretTarget: HTMLTextAreaElement;
  searchResults: any[];
  dirty: boolean;

  add(): void {
    this.concordances.push({ concordance: '', izvorId: null, searchText: '', opis: '', skracenica: '' });
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
    this.concordances.forEach((c: any) => {
      if (c.izvorId) {
        this.korpusService.loadIzvor(c.izvorId).subscribe({
          next: (data: any) => c.opis = data.opis,
          error: (error: any) => console.log(error)
        });
      }
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
    if (event.key === 'F1' || event.key === 'F4') {
      this.caretPos = event.target.selectionStart;
      this.caretIndex = index;
      this.caretTarget = event.target;
      this.showQuotesDialog = true;
    }
  }

  search(event): void {
    this.korpusService.searchIzvor(event.query).subscribe({
      next: (data: any[]) => this.searchResults = data,
      error: (error: any) => console.log(error)
    });
  }

  select(event, index): void {
    this.concordances[index].izvorId = event.pub_id;
    this.concordances[index].opis = event.opis;
    this.concordances[index].searchText = '';
    console.log(this.concordances[index]);
    this.concordancesChange.emit();
  }

  removePub(concordance): void {
    concordance.izvorId = null;
    concordance.opis = '';
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
