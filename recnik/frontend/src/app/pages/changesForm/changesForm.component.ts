import {Component, Input, OnInit} from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

export interface Change {
  user: any;
  operacija_izmene: any;
  vreme: Date;
}

@Component({
  selector: 'changesForm',
  templateUrl: './changesForm.component.html',
  styleUrls: ['./changesForm.component.scss']
})
export class ChangesFormComponent implements OnInit {
  constructor(private primengConfig: PrimeNGConfig) {}
  @Input() changes: Change[];

  ngOnInit(): void {
    this.primengConfig.ripple = true;
  }
}
