import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';
import { of } from 'rxjs';
import { OdrednicaService } from '../../services/odrednice';

@Component({
  selector: 'determinant',
  templateUrl: './determinant.component.html',
  styleUrls: ['./determinant.component.scss'],
})
export class DeterminantComponent implements OnInit, OnChanges {
  constructor(
    private primengConfig: PrimeNGConfig,
    private odrednicaService: OdrednicaService,
  ) {}

  searchResults: any[];
  @Input() determinants: any[];

  add(): void {
    this.determinants.push({ searchText: '', determinantId: null, rec$: of('') });
  }

  remove(index: number): void {
    this.determinants.splice(index, 1);
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
    this.determinants[index].determinantId = event.pk;
    this.odrednicaService.get(event.pk).subscribe((odr) => {
      this.determinants[index].rec$ = of(odr.rec);
    });
    this.determinants[index].searchText = '';
  }

  removeDeterminant(index): void {
    this.determinants[index].determinantId = null;
    this.determinants[index].rec$ = of('');
  }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
  }

  ngOnChanges(changes: SimpleChanges): void {
    this.determinants.forEach((d) => {
      if (d.determinantId) {
        this.odrednicaService.get(d.determinantId).subscribe((odr) => {
          d.rec$ = of(odr.rec);
        });
      }
    });
  }

}
