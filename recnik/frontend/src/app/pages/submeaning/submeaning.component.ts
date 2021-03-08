import { Component, Input, OnInit } from '@angular/core';
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

  showQuotesDialog = false;
  caretPos: number;
  caretIndex: number;
  caretTarget: HTMLTextAreaElement;

  constructor(private primengConfig: PrimeNGConfig) {}

  add(): void {
    this.submeanings.push({ value: '', qualificators: [], expressions: [], concordances: [] });
  }

  remove(submeaning): void {
    this.submeanings.splice(this.submeanings.indexOf(submeaning), 1);
  }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
  }

  insertQuote(char: string): void {
    const text = this.submeanings[this.caretIndex].value;
    const newText = text.slice(0, this.caretPos) + char + text.slice(this.caretPos);
    this.submeanings[this.caretIndex].value = newText;
    this.showQuotesDialog = false;
    this.caretTarget.focus();
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
