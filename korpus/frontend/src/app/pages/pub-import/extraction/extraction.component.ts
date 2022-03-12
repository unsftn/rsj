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

  id: number;
  pub: any;
  pubFiles: any[];
  running: boolean;
  activeIndex: number;

  constructor(
      private route: ActivatedRoute,
      private router: Router,
      private messageService: MessageService,
      private titleService: Title,
      private publikacijaService: PublikacijaService,
  ) { }

  ngOnInit(): void {
    this.running = false;
    this.route.data.subscribe((data) => {
      this.titleService.setTitle(data.title);
    });
    this.publikacijaService.changed = false;
    this.route.pathFromRoot[2].params.subscribe((params) => {
      this.id = +params.pid;
      this.fetchData();
    });
    this.route.data.subscribe((data) => {
      this.titleService.setTitle(data.title);
    });
  }

  fetchData(): void {
    this.publikacijaService.get(this.id).subscribe((value) => {
      this.pub = value;
      this.id = value.id;
      this.pubFiles = this.pub.fajlpublikacije_set.map((item) => {
        item.status = 'спремна';
        item.severity = 'info';
        return item;
      });
    });
  }

  start(): void {
    if (this.pubFiles.length > 0) {
      this.running = true;
      this.activeIndex = 0;
      this.process();
    }
  }

  process(): void {
    if (this.activeIndex >= this.pubFiles.length) {
      this.running = false;
      return;
    }
    this.moveStatus(this.pubFiles[this.activeIndex]);
    switch (this.pubFiles[this.activeIndex].status) {
      case 'у обради':
        setTimeout(() => {
          this.process();
        }, 3000);
        break;
      case 'завршен':
        this.activeIndex++;
        this.process();
    }
  }

  moveStatus(pubFile): void {
    switch (pubFile.status) {
      case 'спремна':
        pubFile.status = 'у обради';
        pubFile.severity = 'warning';
        break;
      case 'у обради':
        pubFile.status = 'завршен';
        pubFile.severity = 'success';
        break;
      case 'завршен':
        pubFile.status = 'спремна';
        pubFile.severity = 'info';
        break;
    }
  }
}
