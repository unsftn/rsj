import { Component, OnInit } from '@angular/core';
import { PrimeNGConfig } from 'primeng/api';

export interface Change {
  user: string;
  role: string;
  date: string;
  operation: string;
}

@Component({
  selector: 'changesForm',
  templateUrl: './changesForm.component.html',
})
export class ChangesFormComponent implements OnInit {
  constructor(private primengConfig: PrimeNGConfig) {}
  changes: Change[];

  ngOnInit() {
    this.primengConfig.ripple = true;
    this.changes = [
      {
        user: 'Пера Перић',
        role: 'лексикограф',
        date: '11.11.2020.',
        operation: 'Први унос',
      },
      {
        user: 'Жика Жикић',
        role: 'редактор',
        date: '15.11.2020.',
        operation: 'Завршена редакција 1',
      },
      {
        user: 'Мика Микић',
        role: 'уредник',
        date: '17.11.2020.',
        operation: 'Враћено на редакцију 1',
      },
      {
        user: 'Жика Жикић',
        role: 'редактор',
        date: '19.11.2020.',
        operation: 'Завршена редакција 1',
      },
      {
        user: 'Мика Микић',
        role: 'уредник',
        date: '22.11.2020.',
        operation: 'Завршена редакција 2',
      },
    ];
  }
}
