import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { OdrednicaService } from '../../services/odrednice';

@Component({
  selector: 'referenca',
  templateUrl: './referenca.component.html',
  styleUrls: ['./referenca.component.scss']
})
export class ReferencaComponent implements OnInit {

  @Input() reference: any[];
  searchText: string;
  searchResults: any[];
  @Output() referenceChange = new EventEmitter();

  constructor(
    private odrednicaService: OdrednicaService,
    private domSanitizer: DomSanitizer,
  ) {}

  ngOnInit(): void {
    this.searchText = '';
    this.searchResults = [];
  }

  search(event: any): void {
    this.odrednicaService.searchWithMeanings(event.query).subscribe({
      next: (data) => {
        data.forEach((item: any) => {item.odr = this.domSanitizer.bypassSecurityTrustHtml(item.odr)});
        this.searchResults = data; 
      },
      error: (error) => console.log(error),
    });
  }

  select(obj: any): void {
    this.searchText = '';
    for (const r of this.reference)
      if (r.vrsta === obj.vrsta && r.ident === obj.ident)
        return;
    switch (obj.vrsta) {
      case 1:
        if (obj.tekst)
          this.reference.push({ vrsta: 2, ident: obj.ident, odr: obj.odr, rbr: obj.rbr, tekst: obj.tekst});
        else
          this.reference.push(obj);
        break;
      case 2:
        this.reference.push(obj);
        break;
      case 3:
        this.reference.push(obj);
        break;
    }
  }

  moveUp(index: number): void {
    if (index === 0)
      return;
    const ref = this.reference.splice(index, 1)[0];
    this.reference.splice(index - 1, 0, ref);
    this.referenceChange.emit();

  }

  moveDown(index: number): void {
    if (index === this.reference.length - 1)
      return;
    const ref = this.reference.splice(index, 1)[0];
    this.reference.splice(index + 1, 0, ref);
    this.referenceChange.emit();
  }

  remove(index: number): void {
    this.reference.splice(index, 1);
    this.referenceChange.emit();
  }

}
