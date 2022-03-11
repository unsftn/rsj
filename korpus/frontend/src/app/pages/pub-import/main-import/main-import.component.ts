import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ConfirmationService, ConfirmEventType, MessageService, PrimeIcons } from 'primeng/api';
import { PublikacijaService } from '../../../services/publikacije/publikacija.service';
import { SafeHtml, Title } from '@angular/platform-browser';

@Component({
  selector: 'app-main-import',
  templateUrl: './main-import.component.html',
  styleUrls: ['./main-import.component.scss']
})
export class MainImportComponent implements OnInit {

  id: number;
  pub: any;
  timelineEvents: any[];
  activeStep: number;

  constructor(
      private route: ActivatedRoute,
      private router: Router,
      private messageService: MessageService,
      private confirmationService: ConfirmationService,
      private publikacijaService: PublikacijaService,
  ) {
    this.activeStep = 0;
  }

  ngOnInit(): void {
    this.timelineEvents = [
      {operation: 'Датотеке', icon: PrimeIcons.FILE_PDF, color: '#9C27B0', active: true},
      {operation: 'Екстракција', icon: PrimeIcons.FILTER, color: '#9C27B0', active: false},
      {operation: 'Завршетак', icon: PrimeIcons.CHECK, color: '#9C27B0', active: false},
    ];
    this.markActiveStep();
    this.route.params.subscribe((params) => {
      this.id = +params.pid;
      this.fetchData();
    });
  }

  fetchData(): void {
    this.publikacijaService.get(this.id).subscribe((value) => {
      this.pub = value;
      this.id = value.id;
    });
  }

  opis(): SafeHtml {
    return this.publikacijaService.getOpis(this.pub);
  }

  next(): void {
    if (this.changed()) {
      this.confirmationService.confirm({
        message: 'Направљене су измене у подацима. Да ли желите да наставите?',
        accept: () => {
          this.nextStep();
        },
        reject: (type) => {
          switch (type) {
            case ConfirmEventType.CANCEL:
              break;
            case ConfirmEventType.REJECT:
              break;
          }
        }
      });
    } else {
      this.nextStep();
    }
  }

  nextStep(): void {
    const currentStep = this.activeStep++;
    switch (currentStep) {
      case 0:
        this.router.navigate(['/import', this.id, 'ekstrakcija']);
        break;
      default:
        this.router.navigate(['/publikacije']);
        break;
    }
  }

  changed(): boolean {
    return this.publikacijaService.changed;
  }

  markActiveStep(): void {
    console.log(this.activeStep);
    for (let i = 0; i < this.timelineEvents.length; i++)
      this.timelineEvents[i].active = i === this.activeStep;
  }
}
