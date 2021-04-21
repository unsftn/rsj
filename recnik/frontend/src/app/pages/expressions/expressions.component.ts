import { Component, Input, OnChanges, OnInit, Output, SimpleChanges, EventEmitter } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';
import { of } from 'rxjs';
import { OdrednicaService } from '../../services/odrednice';

@Component({
  selector: 'expressions',
  templateUrl: './expressions.component.html',
  styleUrls: ['./expressions.component.scss'],
})
export class ExpressionsComponent implements OnInit, OnChanges {
  filteredKeywords: any[];
  keyWords = [];
  selectedKeyWord: string;

  // @Input() isTopLevel: boolean;
  @Input() expressions;
  @Output() expressionsChange = new EventEmitter();

  showQuotesDialog = false;
  caretPos: number;
  caretIndex: number;
  caretTarget: HTMLTextAreaElement;
  caretInOpis: boolean;
  searchResults: any[];
  dirty: boolean;

  constructor(
    private primengConfig: PrimeNGConfig,
    private odrednicaService: OdrednicaService,
  ) {}

  add(): void {
    this.expressions.push({ value: '', tekst: '', searchText: '', determinantId: null, rec$: of(''), qualificators: [] });
    this.expressionsChange.emit();
  }

  remove(expression): void {
    this.expressions.splice(this.expressions.indexOf(expression), 1);
    this.expressionsChange.emit();
  }

  search(event): void {
    this.odrednicaService.search(event.query).subscribe(
      (data) => {
        this.searchResults = data;
      },
      (error) => {
        console.log(error);
      }
    );
  }

  select(event, index): void {
    this.expressions[index].determinantId = event.pk;
    this.odrednicaService.get(event.pk).subscribe((odr) => {
      this.expressions[index].rec$ = of(odr.rec);
    });
    this.expressions[index].searchText = '';
    this.expressionsChange.emit();
  }

  removeDeterminant(expression): void {
    expression.determinantId = null;
    expression.rec$ = of('');
    this.expressionsChange.emit();
  }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
  }

  ngOnChanges(changes: SimpleChanges): void {
    this.expressions.forEach((e) => {
      if (e.determinantId) {
        this.odrednicaService.get(e.determinantId).subscribe((odr) => {
          e.rec$ = of(odr.rec);
        });
      }
    });
  }

  onChange(): void {
    this.expressionsChange.emit();
  }

  insertQuote(char: string): void {
    if (this.caretInOpis) {
      const text = this.expressions[this.caretIndex].value;
      const newText = text.slice(0, this.caretPos) + char + text.slice(this.caretPos);
      this.expressions[this.caretIndex].value = newText;
    } else {
      const text = this.expressions[this.caretIndex].tekst;
      const newText = text.slice(0, this.caretPos) + char + text.slice(this.caretPos);
      this.expressions[this.caretIndex].tekst = newText;
    }
    this.showQuotesDialog = false;
    this.caretTarget.focus();
    setTimeout(() => {this.caretTarget.setSelectionRange(this.caretPos + 1, this.caretPos + 1, 'none')});
  }

  keyup(event, index: number, opis: boolean): void {
    if (event.key === 'F1') {
      this.caretInOpis = opis;
      this.caretPos = event.target.selectionStart;
      this.caretIndex = index;
      this.caretTarget = event.target;
      this.showQuotesDialog = true;
    }
  }

  onValueChange(value: any): void {
    this.dirty = true;
  }

  onFocusLeave(): void {
    if (this.dirty) {
      this.dirty = false;
      this.expressionsChange.emit();
    }
  }

}
