import { Component, Input, OnInit } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'expressions',
  templateUrl: './expressions.component.html',
  styleUrls: ['./expressions.component.scss'],
})
export class ExpressionsComponent implements OnInit {
  filteredKeywords: any[];
  keyWords = [];
  selectedKeyWord: string;

  @Input() isTopLevel: boolean;
  @Input() expressions = [];

  showQuotesDialog = false;
  caretPos: number;
  caretIndex: number;
  caretTarget: HTMLTextAreaElement;

  constructor(
    private primengConfig: PrimeNGConfig,
    private httpClient: HttpClient,
  ) {}

  add(): void {
    this.expressions.push({ value: '', tekst: '', keywords: [], qualificators: [] });
  }

  remove(expression): void {
    this.expressions.splice(this.expressions.indexOf(expression), 1);
  }

  async fetch(): Promise<void> {
    const response: any = await this.httpClient
      .get('api/odrednice/odrednica')
      .toPromise();

    if (response) {
      this.keyWords = response.map((item) => {
        return item.rec;
      });
    }
  }

  filterKeyword(event): void {
    const query = event.query;
    this.filteredKeywords = this.keyWords.filter((kw) =>
      kw.toLowerCase().startsWith(query.toLowerCase()),
    );
  }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
    this.fetch();
  }

  insertQuote(char: string): void {
    const text = this.expressions[this.caretIndex].value;
    const newText = text.slice(0, this.caretPos) + char + text.slice(this.caretPos);
    this.expressions[this.caretIndex].value = newText;
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
