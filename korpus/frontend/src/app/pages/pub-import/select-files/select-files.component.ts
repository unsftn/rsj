import { Component, EventEmitter, OnInit, Output, ViewChild } from '@angular/core';
import { SafeHtml, Title } from '@angular/platform-browser';
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
  pub: any;
  pubFiles: any[];
  selectedPubFile: any;

  @ViewChild(FileUpload) fileUpload: FileUpload;

  constructor(
      private route: ActivatedRoute,
      private router: Router,
      private messageService: MessageService,
      private titleService: Title,
      private publikacijaService: PublikacijaService,
  ) {
  }

  fetchData(): void {
    this.publikacijaService.get(this.id).subscribe((value) => {
      this.pub = value;
      this.id = value.id;
      this.pubFiles = this.pub.fajlpublikacije_set;
    });
  }

  ngOnInit(): void {
    this.publikacijaService.changed = false;
    this.route.pathFromRoot[2].params.subscribe((params) => {
      this.id = +params.pid;
      this.fetchData();
    });
    this.route.data.subscribe((data) => {
      this.titleService.setTitle(data.title);
    });
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

  delete(): void {
    if (this.selectedPubFile.length > 0) {
      const fileIds = this.selectedPubFile.map((item) => item.id);
      this.publikacijaService.deleteFiles(this.id, fileIds).subscribe({
        next: (res) => {
          this.fetchData();
        },
        error: (error) => {
          console.log(error);
        }
      });
      this.publikacijaService.changed = true;
    }
  }

  reorder(event): void {
    for (let i = 0; i < this.pubFiles.length; i++) {
      this.pubFiles[i].redni_broj = i + 1;
    }
    const fileIds = this.pubFiles.map((item) => item.id);
    this.publikacijaService.reorderFiles(this.id, fileIds).subscribe({
      next: (res) => {
      },
      error: (error) => {
        console.log(error);
      }
    });
    this.publikacijaService.changed = true;
  }

  upload(event): void {
    this.publikacijaService.uploadFiles(this.id, event.files).subscribe((res) => {
      this.fileUpload.clear();
      this.fetchData();
      this.publikacijaService.changed = true;
    }, (error) => {
      console.log(error);
    });
  }
}
