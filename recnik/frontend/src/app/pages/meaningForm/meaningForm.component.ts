import { Component, OnInit, Input, HostListener, Output, EventEmitter } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

@Component({
  selector: 'meaning',
  templateUrl: './meaningForm.component.html',
  styleUrls: ['./meaningForm.component.scss'],
})
export class MeaningFormComponent implements OnInit {
  constructor(private primengConfig: PrimeNGConfig) {}

  @Input() meanings: any[] = [];
  @Output() meaningsChange = new EventEmitter();

  showQuotesDialog = false;
  caretPos: number;
  caretIndex: number;
  caretTarget: HTMLTextAreaElement;
  baseChar = 'a';
  dirty: boolean;

  add(scrollToBottom: boolean = false): void {
    this.meanings.push({ value: '', submeanings: [], qualificators: [], concordances: [], expressions: [], collocations: [] });
    this.meaningsChange.emit();
    if (scrollToBottom) {
      setTimeout(() => { scrollTo(0, document.body.scrollHeight); });
    }
  }

  remove(meaning): void {
    this.meanings.splice(this.meanings.indexOf(meaning), 1);
    this.meaningsChange.emit();
  }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
    this.dirty = false;
  }

  onChange(): void {
    this.meaningsChange.emit();
  }

  onValueChange(value: any): void {
    this.dirty = true;
  }

  onFocusLeave(): void {
    if (this.dirty) {
      this.dirty = false;
      this.meaningsChange.emit();
    }
  }

  moveMeaningUp(index: number): void {
    if (index === 0)
      return;
    const meaning = this.meanings.splice(index, 1)[0];
    this.meanings.splice(index - 1, 0, meaning);
    this.meaningsChange.emit();
  }

  moveMeaningDown(index: number): void {
    if (index === this.meanings.length - 1)
      return;
    const meaning = this.meanings.splice(index, 1)[0];
    this.meanings.splice(index + 1, 0, meaning);
    this.meaningsChange.emit();
  }

  insertQuote(char: string): void {
    const text = this.meanings[this.caretIndex].value;
    const newText = text.slice(0, this.caretPos) + char + text.slice(this.caretPos);
    this.meanings[this.caretIndex].value = newText;
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
      this.baseChar = event.target.value[this.caretPos - 1];
    }
  }
}
