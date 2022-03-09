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
      this.pubFiles = this.pub.fajlpublikacije_set;
      console.log(value);
    });
  }

  ngOnInit(): void {
    this.timelineEvents = [
      {operation: 'Датотеке', icon: PrimeIcons.FILE_PDF, color: '#9C27B0'},
      {operation: 'Обрада', icon: PrimeIcons.FILTER, color: '#9C27B0'},
      {operation: 'Завршетак', icon: PrimeIcons.CHECK, color: '#9C27B0'},
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

}
