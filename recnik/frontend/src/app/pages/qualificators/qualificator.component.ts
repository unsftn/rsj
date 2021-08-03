import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';
import { HttpClient } from '@angular/common/http';
import { Qualificator } from '../../models/qualificator';
import { QualificatorService } from '../../services/odrednice';

@Component({
  selector: 'qualificator',
  templateUrl: './qualificator.component.html',
  styleUrls: ['./qualificator.component.scss'],
})
export class QualificatorComponent implements OnInit {
  constructor(
    private primengConfig: PrimeNGConfig,
    private httpClient: HttpClient,
    private qualificatorService: QualificatorService,
  ) {}

  allQualificators: Qualificator[];
  @Input() selectedQualificators: Qualificator[];

  selectedLeft: Qualificator;
  selectedRight: Qualificator;

  @Output() selectedLeftChange: EventEmitter<Qualificator> = new EventEmitter();
  @Output() selectedRightChange: EventEmitter<Qualificator> = new EventEmitter();
  @Output() selectedQualificatorsChange: EventEmitter<Qualificator[]> = new EventEmitter();

  selectLeftQualificator(): void {
    this.selectedLeftChange.emit(this.selectedLeft);
  }

  selectRightQualificator(): void {
    this.selectedRightChange.emit(this.selectedRight);
  }

  moveRight(): void {
    if (this.selectedLeft) {
      if (!this.selectedQualificators.includes(this.selectedLeft)) {
        // this.selectedQualificators.push(this.selectedLeft); // <-- Listbox ne detektuje izmene u options ???
        this.selectedQualificators = [...this.selectedQualificators, this.selectedLeft];  // ludi fix
        this.selectedQualificatorsChange.emit(this.selectedQualificators);
      }
    }
  }

  moveLeft(): void {
    if (this.selectedRight) {
      if (this.selectedQualificators.includes(this.selectedRight)) {
        this.selectedQualificators = this.selectedQualificators.filter((value) => value !== this.selectedRight);
        this.selectedQualificatorsChange.emit(this.selectedQualificators);
      }
    }
  }

  moveUp(): void {
    if (this.selectedRight) {
      const origPos = this.selectedQualificators.indexOf(this.selectedRight);
      if (origPos === 0) { return; }
      const copy = [...this.selectedQualificators];
      const otherItem = copy[origPos - 1];
      copy.splice(origPos - 1, 2, this.selectedRight, otherItem);
      this.selectedQualificators = copy;
      this.selectedQualificatorsChange.emit(this.selectedQualificators);
    }
  }

  moveDown(): void {
    if (this.selectedRight) {
      const origPos = this.selectedQualificators.indexOf(this.selectedRight);
      if (origPos === this.selectedQualificators.length - 1) { return; }
      const copy = [...this.selectedQualificators];
      const otherItem = copy[origPos + 1];
      copy.splice(origPos, 2, otherItem, this.selectedRight);
      this.selectedQualificators = copy;
      this.selectedQualificatorsChange.emit(this.selectedQualificators);
    }
  }

  handleEnter(event) {
    if (event.key === 'Enter') {
      this.moveRight();
    }
  }

  ngOnInit(): void {
    this.primengConfig.ripple = true;
    this.qualificatorService.fetchAllQualificators().subscribe((q) => this.allQualificators = q);
  }
}
