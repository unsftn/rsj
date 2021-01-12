import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

interface Kind {
  name: string;
  id: number;
}

interface VerbKind {
  name: string;
  id: number;
}

interface VerbForm {
  name: string;
  id: number;
}

@Component({
  selector: 'grammarInformations',
  templateUrl: './grammarInformations.component.html',
  styleUrls: ['./grammarInformations.component.scss'],
})
export class GrammarInformationsComponent implements OnInit {
  @Input() isNoun: boolean;
  @Input() isVerb: boolean;
  kinds: Kind[];
  verbKind: VerbKind[];
  verbForm: VerbForm[];

  @Output() selectKindChanged: EventEmitter<Kind> = new EventEmitter();

  @Input() selectedKind: Kind;
  @Output() selectedVerbKind: VerbKind;
  @Output() selectedVerbForm: VerbForm;
  @Output() present: string;
  @Output() details;
  constructor(private primengConfig: PrimeNGConfig) {}

  changeKind() {
    this.selectKindChanged.emit(this.selectedKind);
  }

  ngOnInit() {
    this.primengConfig.ripple = true;
    this.kinds = [
      { name: 'Мушки', id: 1 },
      { name: 'Женски', id: 2 },
      { name: 'Средњи', id: 3 },
    ];
    this.verbKind = [
      { name: 'Прелазни', id: 1 },
      { name: 'Непрелазни', id: 2 },
      { name: 'Повратни', id: 3 },
      { name: 'Узајамно повратни', id: 4 },
    ];
    this.verbForm = [
      { name: 'Свршен', id: 1 },
      { name: 'Несвршен', id: 2 },
      { name: 'Двовидски', id: 3 },
    ];
  }
}
