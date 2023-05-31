import { Component, Input, OnInit, Output, EventEmitter } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

@Component({
  selector: 'submeaning',
  templateUrl: './submeaning.component.html',
  styleUrls: ['./submeaning.component.scss'],
})
export class SubmeaningComponent implements OnInit {
  azbuka = 'абвгдђежзијклљмнњопрстћуфхцчџш';
  @Input() znacenjeRbr: number;
  @Input() submeanings;
  @Output() submeaningsChange = new EventEmitter();

  showQuotesDialog = false;
  caretPos: number;
  caretIndex: number;
  caretTarget: HTMLTextAreaElement;
  baseChar = 'a';
  dirty: boolean;

  constructor(private primengConfig: PrimeNGConfig) {}

  add(): void {
    this.submeanings.push({ value: '', qualificators: [], expressions: [], concordances: [], collocations: [], synonyms: [], antonyms: [] });
    this.submeaningsChange.emit();
    const last = this.submeanings.length - 1;
    setTimeout(() => { document.getElementById(`meaning${this.znacenjeRbr}submeaningtext${last}`).focus(); });
  }

  remove(submeaning): void {
    this.submeanings.splice(this.submeanings.indexOf(submeaning), 1);
    this.submeaningsChange.emit();
  }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
    this.dirty = false;
  }

  insertQuote(char: string): void {
    const text = this.submeanings[this.caretIndex].value;
    const newText = text.slice(0, this.caretPos) + char + text.slice(this.caretPos);
    this.submeanings[this.caretIndex].value = newText;
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

  moveSubmeaningUp(index: number): void {
    if (index === 0)
      return;
    const submeaning = this.submeanings.splice(index, 1)[0];
    this.submeanings.splice(index - 1, 0, submeaning);
    setTimeout(() => {
      // angular 15 ne azurira pravilno sadrzaj textarea polja prilikom premestanja, pa to rucno radimo
      (<HTMLTextAreaElement>document.getElementById('meaning'+this.znacenjeRbr+'submeaningtext'+index)).value = this.submeanings[index].value;
      (<HTMLTextAreaElement>document.getElementById('meaning'+this.znacenjeRbr+'submeaningtext'+(index-1))).value = this.submeanings[index-1].value;
    });
    this.submeaningsChange.emit();
  }

  moveSubmeaningDown(index: number): void {
    if (index === this.submeanings.length - 1)
      return;
    const meaning = this.submeanings.splice(index, 1)[0];
    this.submeanings.splice(index + 1, 0, meaning);
    setTimeout(() => {
      // angular 15 ne azurira pravilno sadrzaj textarea polja prilikom premestanja, pa to rucno radimo
      (<HTMLTextAreaElement>document.getElementById('meaning'+this.znacenjeRbr+'submeaningtext'+index)).value = this.submeanings[index].value;
      (<HTMLTextAreaElement>document.getElementById('meaning'+this.znacenjeRbr+'submeaningtext'+(index+1))).value = this.submeanings[index+1].value;
    });
    this.submeaningsChange.emit();
  }

  onChange(): void {
    this.submeaningsChange.emit();
  }

  onValueChange(value: any): void {
    this.dirty = true;
  }

  onFocusLeave(): void {
    if (this.dirty) {
      this.dirty = false;
      this.submeaningsChange.emit();
    }
  }
}
