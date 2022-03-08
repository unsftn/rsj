import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MessageService, PrimeIcons } from 'primeng/api';
import { PublikacijaService } from '../../../services/publikacije/publikacija.service';

@Component({
  selector: 'app-process-step',
  templateUrl: './process-step.component.html',
  styleUrls: ['./process-step.component.scss']
})
export class ProcessStepComponent implements OnInit {

  id: number;
  step: number;
  timelineEvents: any[];
  pub: any;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private messageService: MessageService,
    private publikacijaService: PublikacijaService,
  ) { }

  fetchData(): void {
    this.publikacijaService.get(this.id).subscribe((value) => {
      console.log(value);
      this.pub = value;
    });
  }

  ngOnInit(): void {
    this.timelineEvents = [
      { operation: 'Датотеке', icon: PrimeIcons.FILE_PDF, color: '#9C27B0' },
      { operation: 'Обрада', icon: PrimeIcons.FILTER, color: '#9C27B0' },
      { operation: 'Завршетак', icon: PrimeIcons.CHECK, color: '#9C27B0' },
    ];
    this.route.params.subscribe((params) => {
      this.id = +params.pid;
      this.step = +params.step;
      this.fetchData();
    });
  }

}
