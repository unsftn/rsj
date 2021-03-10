import { Component, OnInit, Input, HostListener } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

@Component({
  selector: 'meaning',
  templateUrl: './meaningForm.component.html',
  styleUrls: ['./meaningForm.component.scss'],
})
export class MeaningFormComponent implements OnInit {
  constructor(private primengConfig: PrimeNGConfig) {}

  @Input() meanings: any[] = [];

  showQuotesDialog = false;
  caretPos: number;
  caretIndex: number;
  caretTarget: HTMLTextAreaElement;

  add(): void {
    this.meanings.push({ value: '', submeanings: [], qualificators: [], concordances: [], expressions: [] });
  }

  remove(meaning): void {
    this.meanings.splice(this.meanings.indexOf(meaning), 1);
  }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
  }

  // show(obj): void {
  //   console.log(obj);
  // }

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
    }
  }

}
