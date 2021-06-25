import { Component, OnInit } from '@angular/core';
import { SafeHtml, Title } from '@angular/platform-browser';
import { Router } from '@angular/router';
import { Table } from 'primeng/table';
import { PublikacijaService } from '../../../services/publikacije';

@Component({
  selector: 'app-publikacija-list',
  templateUrl: './publikacija-list.component.html',
  styleUrls: ['./publikacija-list.component.scss']
})
export class PublikacijaListComponent implements OnInit {

  publikacije: any[];
  message: SafeHtml;
  showDeleteWarningDialog = false;

  constructor(
    private publikacijaService: PublikacijaService,
    private router: Router,
    private titleService: Title) { }

  ngOnInit(): void {
    this.titleService.setTitle('Публикације');
    this.publikacijaService.getAll().subscribe((value) => {
      this.publikacije = value;
    });
  }

  deleteYes(): void {
    // pozovi delete
    this.showDeleteWarningDialog = false;
  }

  deleteNo(): void {
    this.showDeleteWarningDialog = false;
  }

  add(): void {
    this.router.navigate(['/pubs/add']);
  }

  opis(pub: any): SafeHtml {
    return this.publikacijaService.getOpis(pub);
  }

  edit(pub: any): void {
    this.router.navigate(['/pubs/edit', pub.id]);
  }

  delete(pub: any): void {
    this.message = 'Да ли сте сигурни да желите да обришете ову публикацију?';
    this.showDeleteWarningDialog = true;
  }

  clear(table: Table, filter: HTMLInputElement): void {
    filter.value = '';
    table.clear();
  }
}
