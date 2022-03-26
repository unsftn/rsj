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
    this.publikacijaService.importStep.subscribe((value) => {
      this.activeStep = value;
      this.markActiveStep();
    });
    this.timelineEvents = [
      {operation: 'Метаподаци', icon: PrimeIcons.FILE_PDF, color: '#9C27B0', active: true},
      {operation: 'Датотеке', icon: PrimeIcons.FILE_PDF, color: '#9C27B0', active: true},
      {operation: 'Екстракција', icon: PrimeIcons.FILTER, color: '#9C27B0', active: false},
      {operation: 'Филтери', icon: PrimeIcons.FILTER, color: '#9C27B0', active: false},
      {operation: 'Завршетак', icon: PrimeIcons.CHECK, color: '#9C27B0', active: false},
    ];
    this.markActiveStep();
    this.route.params.subscribe((params) => {
      this.id = +params.pid;
      if (!isNaN(this.id))
        this.fetchData();
    });
    this.publikacijaService.publicationChanged.subscribe((value) => {
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

  prev(): void {
    if (this.changed()) {
      this.confirmationService.confirm({
        message: 'Направљене су измене у подацима. Да ли желите да наставите?',
        accept: () => {
          this.prevStep();
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
      this.prevStep();
    }
  }

  nextStep(): void {
    const currentStep = this.activeStep++;
    this.markActiveStep();
    switch (currentStep) {
      case 0:
        this.router.navigate(['/import', this.id, 'datoteke']);
        break;
      case 1:
        this.router.navigate(['/import', this.id, 'ekstrakcija']);
        break;
      case 2:
        this.router.navigate(['/import', this.id, 'filteri']);
        break;
      default:
        this.router.navigate(['/publikacije']);
        break;
    }
  }

  prevStep(): void {
    const currentStep = this.activeStep--;
    this.markActiveStep();
    switch (currentStep) {
      case 1:
        this.router.navigate(['/import', this.id, 'metapodaci']);
        break;
      case 2:
        this.router.navigate(['/import', this.id, 'datoteke']);
        break;
      case 3:
        this.router.navigate(['/import', this.id, 'ekstrakcija']);
        break;
      case 4:
        this.router.navigate(['/import', this.id, 'filteri']);
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
    for (let i = 0; i < this.timelineEvents.length; i++)
      this.timelineEvents[i].active = i === this.activeStep;
  }
}
