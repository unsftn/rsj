import { Component, OnDestroy, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { ActivatedRoute, Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import { PublikacijaService } from '../../../services/publikacije/publikacija.service';

@Component({
  selector: 'app-extraction',
  templateUrl: './extraction.component.html',
  styleUrls: ['./extraction.component.scss']
})
export class ExtractionComponent implements OnInit, OnDestroy {

  id: number;
  pub: any;
  pubFiles: any[];
  running: boolean;
  activeIndex: number;
  extractionUpdateTimer: any;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private messageService: MessageService,
    private titleService: Title,
    private publikacijaService: PublikacijaService,
  ) { }

  ngOnInit(): void {
    this.publikacijaService.importStep.emit(2);
    this.running = false;
    this.route.data.subscribe((data) => {
      this.titleService.setTitle(data.title);
    });
    this.publikacijaService.changed = false;
    this.route.pathFromRoot[2].params.subscribe((params) => {
      this.id = +params.pid;
      this.fetchData();
    });
  }

  ngOnDestroy(): void {
    if (this.extractionUpdateTimer)
      clearInterval(this.extractionUpdateTimer);
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
      this.publikacijaService.deleteTextsForPub(this.id).subscribe({
        next: () => {
          this.publikacijaService.extractTextForPub(this.id).subscribe({
            next: () => {
              this.extractionUpdateTimer = setInterval(() => {
                this.updateFileStatuses();
              }, 1000);
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

  updateFileStatuses(): void {
    this.publikacijaService.getFilesForPub(this.id).subscribe({
      next: (data) => {
        console.log(data);
        data.forEach((item, index) => {
          const pubFile = this.pubFiles[index];
          switch (item.extraction_status) {
            case 0:
              pubFile.status = 'спремна';
              pubFile.severity = 'info';
              break;
            case 1:
              pubFile.status = 'у обради';
              pubFile.severity = 'warning';
              break;
            case 2:
              pubFile.status = 'завршен';
              pubFile.severity = 'success';
              break;
            case 3:
              pubFile.status = 'грешка';
              pubFile.severity = 'error';
              break;
          }
        });
        if (data.every((elem) => elem.extraction_status > 1)) {
          clearInterval(this.extractionUpdateTimer);
          this.running = false;
          this.publikacijaService.publicationChanged.emit(true);
        }
      },
      error: (error) => {
        console.log(error);
      }
    });
  }

  // process2(): void {
  //   if (this.activeIndex >= this.pubFiles.length) {
  //     for (const pf of this.pubFiles) {
  //       pf.status = 'спремна';
  //       pf.severity = 'info';
  //     }
  //     this.running = false;
  //     this.publikacijaService.publicationChanged.emit(true);
  //     return;
  //   }
  //   this.moveStatus(this.pubFiles[this.activeIndex]);
  //   switch (this.pubFiles[this.activeIndex].status) {
  //     case 'у обради':
  //       this.publikacijaService.extractTextForPub(this.id).subscribe({
  //         next: (res) => {
  //           this.process2();
  //         },
  //         error: (error) => {
  //           console.log(error);
  //           this.pubFiles[this.activeIndex].status = 'грешка';
  //           this.pubFiles[this.activeIndex].severity = 'error';
  //           this.activeIndex++;
  //           this.process2();
  //         }
  //       });
  //       break;
  //     case 'завршен':
  //       this.activeIndex++;
  //       this.process2();
  //   }
  // }

  // moveStatus(pubFile): void {
  //   switch (pubFile.status) {
  //     case 'спремна':
  //       pubFile.status = 'у обради';
  //       pubFile.severity = 'warning';
  //       break;
  //     case 'у обради':
  //       pubFile.status = 'завршен';
  //       pubFile.severity = 'success';
  //       break;
  //     case 'завршен':
  //       pubFile.status = 'спремна';
  //       pubFile.severity = 'info';
  //       break;
  //     case 'грешка':
  //       pubFile.status = 'спремна';
  //       pubFile.severity = 'info';
  //       break;
  //   }
  // }
}
