import { Component, Input, OnInit, Output, EventEmitter, OnChanges, SimpleChanges } from '@angular/core';
import { PrimeNGConfig } from "primeng/api";

@Component({
  selector: 'short-collocations',
  templateUrl: './short-collocation.component.html',
  styleUrls: ['./short-collocation.component.scss']
})
export class ShortCollocationComponent implements OnInit, OnChanges {

  @Input() shortCollocations: any[];
  @Output() shortCollocationsChange = new EventEmitter();

  showQuotesDialog = false;
  caretPos: number;
  caretIndex: number;
  caretTarget: HTMLTextAreaElement;
  baseChar = 'a';
  dirty: boolean;

  constructor(private primengConfig: PrimeNGConfig) { }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
  }

  onValueChange(value: any): void {
    this.dirty = true;
  }

  onFocusLeave(): void {
    if (this.dirty) {
      this.dirty = false;
      this.shortCollocationsChange.emit();
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
  }

  add(): void {
    this.shortCollocations.push({tekst: ''});
    this.shortCollocationsChange.emit();
  }

  remove(collocation): void {
    this.shortCollocations.splice(this.shortCollocations.indexOf(collocation), 1);
    this.shortCollocationsChange.emit();
  }

  insertQuote(char: string): void {
    const text = this.shortCollocations[this.caretIndex].tekst;
    const newText = text.slice(0, this.caretPos) + char + text.slice(this.caretPos);
    this.shortCollocations[this.caretIndex].tekst = newText;
    this.showQuotesDialog = false;
    this.caretTarget.focus();
    setTimeout(() => {this.caretTarget.setSelectionRange(this.caretPos + 1, this.caretPos + 1, 'none')});
  }

  keyup(event, index: number): void {
    if (event.key === 'F1' || event.key === 'F4') {
      this.caretPos = event.target.selectionStart;
      this.caretIndex = index;
      this.caretTarget = event.target;
      this.showQuotesDialog = true;
      this.baseChar = event.target.value[this.caretPos - 1];
    }
  }
}
