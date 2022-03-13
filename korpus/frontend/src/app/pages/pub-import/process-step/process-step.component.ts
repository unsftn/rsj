import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MessageService, PrimeIcons } from 'primeng/api';
import { PublikacijaService } from '../../../services/publikacije/publikacija.service';
import { Title } from '@angular/platform-browser';

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
  operations: any[];
  selected: any[];
  running: boolean;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private messageService: MessageService,
    private titleService: Title,
    private publikacijaService: PublikacijaService,
  ) { }

  fetchData(): void {
    this.publikacijaService.get(this.id).subscribe((value) => {
      console.log(value);
      this.pub = value;
    });
  }

  ngOnInit(): void {
    this.running = false;
    this.operations = [{
      title: 'Уклони фиксан садржај',
      code: 0,
      params: [{
        name: 'Текст',
        value: ''
      }]
    }, {
      title: 'Уклони хифенацију',
      code: 1,
      params: []
    }, {
      title: 'Уклони број странице на дну',
      code: 2,
      params: []
    }, {
      title: 'Спој линије које се завршавају размаком',
      code: 3,
      params: []
    }, {
      title: 'Уклони почетне странице',
      code: 4,
      params: [{
        name: 'Број страница',
        value: ''
      }]
    }];
    this.selected = [];
    this.route.data.subscribe((data) => {
      this.titleService.setTitle(data.title);
    });
    this.route.pathFromRoot[2].params.subscribe((params) => {
      this.id = +params.pid;
      this.fetchData();
    });
  }

  start(): void {
    this.running = true;
  }

}
