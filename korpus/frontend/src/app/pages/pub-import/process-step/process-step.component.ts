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
      this.publikacijaService.getFilterList().subscribe({
        next: (res) => {
          console.log(res);
          this.filters = res;
          this.initSelectedFilters();
        },
        error: (error) => {
          console.log(error);
        }
      });
    });
  }

  initSelectedFilters(): void {
    for (const f of this.pub.filterpublikacije_set) {
      const pos = this.filters.findIndex((x) => x.code === f.vrsta_filtera);
      const filter = this.filters[pos];
      for (const [i, pf] of f.parametarfiltera_set.entries()) {
        filter.params[i].value = pf.vrednost;
      }
      this.selected.push(filter);
      console.log(filter);
      this.filters.splice(pos, 1);
    }
  }

  ngOnInit(): void {
    this.publikacijaService.importStep.emit(3);
    this.running = false;
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
    const filterList = this.selected.map((item) => ({
      vrsta: item.code,
      params: item.params.map((i2) => ({ naziv: i2.name, vrednost: i2.value}))
    }));
    console.log(filterList);
    this.publikacijaService.saveFilters(this.id, filterList).subscribe({
      next: (res) => {
        this.publikacijaService.applyFilters(this.id).subscribe({
          next: (res2) => {
            this.publikacijaService.publicationChanged.emit(true);
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
