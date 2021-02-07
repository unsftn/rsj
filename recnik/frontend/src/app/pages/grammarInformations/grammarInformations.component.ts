import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';
import { Gender, VerbForm, VerbKind } from '../../models';
import { EnumService } from '../../services/odrednice/enum.service';

@Component({
  selector: 'grammarInformations',
  templateUrl: './grammarInformations.component.html',
  styleUrls: ['./grammarInformations.component.scss'],
})
export class GrammarInformationsComponent implements OnInit {
  @Input() isNoun: boolean;
  @Input() isVerb: boolean;
  genders: Gender[];
  verbKinds: VerbKind[];
  verbForms: VerbForm[];

  @Output() selectedGenderChange: EventEmitter<Gender> = new EventEmitter();
  @Output() selectedVerbKindChange: EventEmitter<VerbKind> = new EventEmitter();
  @Output() selectedVerbFormChange: EventEmitter<VerbForm> = new EventEmitter();
  @Output() extensionChange: EventEmitter<string> = new EventEmitter();
  @Output() presentChange: EventEmitter<string> = new EventEmitter();
  @Output() detailsChange: EventEmitter<string> = new EventEmitter();

  @Input() selectedGender: Gender;
  @Input() selectedVerbKind: VerbKind;
  @Input() selectedVerbForm: VerbForm;
  @Input() extension: string;
  @Input() present: string;
  @Input() details;

  constructor(private primengConfig: PrimeNGConfig, private enumService: EnumService) {}

  changeKind(): void {
    this.selectedGenderChange.emit(this.selectedGender);
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
    this.genders = this.enumService.getAllGenders();
    this.verbKinds = this.enumService.getAllVerbKinds();
    this.verbForms = this.enumService.getAllVerbForms();
  }
}
