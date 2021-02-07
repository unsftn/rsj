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

  @Output() selectedKindChange: EventEmitter<Kind> = new EventEmitter();
  @Output() selectedVerbKindChange: EventEmitter<VerbKind> = new EventEmitter();
  @Output() selectedVerbFormChange: EventEmitter<VerbForm> = new EventEmitter();
  @Output() extensionChange: EventEmitter<string> = new EventEmitter();
  @Output() presentChange: EventEmitter<string> = new EventEmitter();
  @Output() detailsChange: EventEmitter<string> = new EventEmitter();

  @Input() selectedKind: Kind;
  @Input() selectedVerbKind: VerbKind;
  @Input() selectedVerbForm: VerbForm;
  @Input() extension: string;
  @Input() present: string;
  @Input() details;

  constructor(private primengConfig: PrimeNGConfig) {}

  changeKind(): void {
    this.selectedKindChange.emit(this.selectedKind);
  }

  changeVerbKind(): void {
    this.selectedVerbKindChange.emit(this.selectedVerbKind);
  }

  changeVerbForm(): void {
    this.selectedVerbFormChange.emit(this.selectedVerbForm);
  }

  changeExtension(): void {
    this.extensionChange.emit(this.extension);
  }

  changePresent(): void {
    this.presentChange.emit(this.present);
  }

  changeDetails(): void {
    this.detailsChange.emit(this.details);
  }

  ngOnInit(): void {
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
