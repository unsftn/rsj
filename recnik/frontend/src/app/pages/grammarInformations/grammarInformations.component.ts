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
  @Output() selectVerbKindChanged: EventEmitter<VerbKind> = new EventEmitter();
  @Output() selectVerbFormChanged: EventEmitter<VerbForm> = new EventEmitter();
  @Output() extensionChanged: EventEmitter<string> = new EventEmitter();
  @Output() presentChanged: EventEmitter<string> = new EventEmitter();
  @Output() detailsChanged: EventEmitter<string> = new EventEmitter();

  @Input() selectedKind: Kind;
  @Input() selectedVerbKind: VerbKind;
  @Input() selectedVerbForm: VerbForm;
  @Input() extension: string;
  @Input() present: string;
  @Input() details;

  constructor(private primengConfig: PrimeNGConfig) {}

  changeKind() {
    this.selectKindChanged.emit(this.selectedKind);
  }

  changeVerbKind() {
    this.selectVerbKindChanged.emit(this.selectedVerbKind);
  }

  changeVerbForm() {
    this.selectVerbFormChanged.emit(this.selectedVerbForm);
  }

  changeExtension() {
    this.extensionChanged.emit(this.extension);
  }

  changePresent() {
    this.presentChanged.emit(this.present);
  }

  changeDetails() {
    this.detailsChanged.emit(this.details);
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
