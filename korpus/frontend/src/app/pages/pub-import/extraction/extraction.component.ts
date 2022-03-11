import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { ActivatedRoute, Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import { PublikacijaService } from '../../../services/publikacije/publikacija.service';

@Component({
  selector: 'app-extraction',
  templateUrl: './extraction.component.html',
  styleUrls: ['./extraction.component.scss']
})
export class ExtractionComponent implements OnInit {

  constructor(
      private route: ActivatedRoute,
      private router: Router,
      private messageService: MessageService,
      private titleService: Title,
      private publikacijaService: PublikacijaService,
  ) { }

  ngOnInit(): void {
    this.route.data.subscribe((data) => {
      this.titleService.setTitle(data.title);
    });
  }

}
