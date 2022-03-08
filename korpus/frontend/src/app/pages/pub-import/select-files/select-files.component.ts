import { Component, OnInit } from '@angular/core';
import { SafeHtml } from '@angular/platform-browser';
import { ActivatedRoute, Router } from '@angular/router';
import { MessageService, PrimeIcons } from 'primeng/api';
import { PublikacijaService } from '../../../services/publikacije/publikacija.service';

@Component({
  selector: 'app-select-files',
  templateUrl: './select-files.component.html',
  styleUrls: ['./select-files.component.scss']
})
export class SelectFilesComponent implements OnInit {

  id: number;
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
      this.pub = value;
      console.log(value);
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
      this.fetchData();
    });
  }

  opis(): SafeHtml {
    return this.publikacijaService.getOpis(this.pub);
  }

}
