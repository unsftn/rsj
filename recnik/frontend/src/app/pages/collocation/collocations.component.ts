import { Component, OnInit, Output, EventEmitter, Input } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

interface Collocation {
  note: string;
  selectedKeywords: string[];
}

@Component({
  selector: 'collocations',
  templateUrl: './collocations.component.html',
  styleUrls: ['./collocations.component.scss'],
})
export class CollocationsComponent implements OnInit {
  @Input() collocations: Collocation[];

  @Output() collocationChanged: EventEmitter<
    Collocation[]
  > = new EventEmitter();

  constructor(private primengConfig: PrimeNGConfig) {}

  changeCollocation() {
    this.collocationChanged.emit(this.collocations);
  }

  async add() {
    this.collocations.push({ selectedKeywords: [], note: '' });
  }

  ngOnInit() {
    this.primengConfig.ripple = true;
    this.collocations = [];
    this.add();
  }
}
