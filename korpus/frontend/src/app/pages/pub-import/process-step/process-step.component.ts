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
  filters: any[];
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
    this.publikacijaService.getFilterList().subscribe({
      next: (res) => {
        this.filters = res;
      },
      error: (error) => {
        console.log(error);
      }
    });
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
    console.log(this.selected);
    this.running = true;
    const filterList = this.selected.map((item) => ({
      vrsta: item.code,
      params: item.params.map((i2) => ({ naziv: i2.name, vrednost: i2.value}))
    }));
    this.publikacijaService.saveFilters(this.id, filterList).subscribe({
      next: (res) => {
        this.publikacijaService.applyFilters(this.id).subscribe({
          next: (res2) => {
            console.log(res, res2);
            this.running = false;
          },
          error: (error) => {
            console.log(error);
          }
        });
      },
      error: (error) => {
        console.log(error);
      }
    });
  }

}
