import { Component, OnInit, ViewChild } from '@angular/core';
import { SafeHtml } from '@angular/platform-browser';
import { ActivatedRoute, Router } from '@angular/router';
import { MessageService, PrimeIcons } from 'primeng/api';
import { PublikacijaService } from '../../../services/publikacije/publikacija.service';
import { FileUpload } from 'primeng/fileupload';

@Component({
  selector: 'app-select-files',
  templateUrl: './select-files.component.html',
  styleUrls: ['./select-files.component.scss']
})
export class SelectFilesComponent implements OnInit {

  id: number;
  timelineEvents: any[];
  pub: any;
  pubFiles: any[];
  selectedPubFile: any;
  @ViewChild(FileUpload) fileUpload: FileUpload;

  constructor(
      private route: ActivatedRoute,
      private router: Router,
      private messageService: MessageService,
      private publikacijaService: PublikacijaService,
  ) {
  }

  fetchData(): void {
    this.publikacijaService.get(this.id).subscribe((value) => {
      this.pub = value;
      this.id = value.id;
      this.pubFiles = this.pub.fajlpublikacije_set;
      console.log(this.pub);
    });
  }

  ngOnInit(): void {
    this.timelineEvents = [
      {operation: 'Датотеке', icon: PrimeIcons.FILE_PDF, color: '#9C27B0', active: true},
      {operation: 'Обрада', icon: PrimeIcons.FILTER, color: '#9C27B0', active: false},
      {operation: 'Завршетак', icon: PrimeIcons.CHECK, color: '#9C27B0', active: false},
    ];
    this.route.params.subscribe((params) => {
      this.id = +params.pid;
      this.fetchData();
    });
  }

  opis(): SafeHtml {
    return this.publikacijaService.getOpis(this.pub);
  }

  formatSize(bytes): string {
    if (bytes === 0) {
      return '0 B';
    }
    const k = 1000;
    const dm = 3;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
  }

  remove(event: Event, index: number): void {
    this.fileUpload.clearInputElement();
    this.fileUpload.onRemove.emit({originalEvent: event, file: this.fileUpload.files[index]});
    this.fileUpload.files.splice(index, 1);
  }

  next(): void {

  }

  delete(): void {
    if (this.selectedPubFile.length > 0) {
      const fileIds = this.selectedPubFile.map((item) => item.id);
      console.log(fileIds);
      this.publikacijaService.deleteFiles(this.id, fileIds).subscribe({
        next: (res) => {
          this.fetchData();
        },
        error: (error) => {
          console.log(error);
        }
      });
    }
  }

  uploadHandler(event): void {
    this.publikacijaService.uploadFiles(this.id, event.files).subscribe((res) => {
      this.fileUpload.clear();
      this.fetchData();
    }, (error) => {
      console.log(error);
    });
  }

}
