import { Component, OnInit } from '@angular/core';
import { SafeHtml, Title } from '@angular/platform-browser';
import { Router } from '@angular/router';
import { LazyLoadEvent, MessageService } from 'primeng/api';
import { PublikacijaService } from '../../services/publikacije/publikacija.service';

@Component({
  selector: 'app-pub-list',
  templateUrl: './pub-list.component.html',
  styleUrls: ['./pub-list.component.scss']
})
export class PubListComponent implements OnInit {

  publikacije: any[];
  message: SafeHtml;
  showDeleteWarningDialog = false;
  first: number = null;
  rows: number = null;
  total: number = null;
  loading: boolean = true;
  filter: string;

  constructor(
    private publikacijaService: PublikacijaService,
    private router: Router,
    private titleService: Title) { }

  ngOnInit(): void {
    this.titleService.setTitle('Извори');
  }

  loadPubs(): void {
    if (!this.filter) {
      this.publikacijaService.getAllPaged(this.first, this.rows).subscribe({
        next: (response: any) => { 
          this.publikacije = response.results; 
          this.total = response.count;
          this.loading = false;
        }, 
        error: (error) => console.log(error)
      });  
    } else {
      this.publikacijaService.searchIzvor(this.filter, this.first, this.rows).subscribe({
        next: (response: any) => { 
          this.publikacije = response.results; 
          this.total = response.count;
          this.loading = false;
        }, 
        error: (error) => console.log(error)
      });
    }
  }

  onLazyLoad(event: LazyLoadEvent): void {
    this.first = event.first;
    this.rows = event.rows;
    this.loadPubs();
  }

  deleteYes(): void {
    // pozovi delete
    this.showDeleteWarningDialog = false;
  }

  deleteNo(): void {
    this.showDeleteWarningDialog = false;
  }

  add(): void {
    this.router.navigate(['/import/nova/metapodaci']);
  }

  opis(pub: any): SafeHtml {
    return this.publikacijaService.getOpis(pub);
  }

  delete(pub: any): void {
    this.message = 'Да ли сте сигурни да желите да обришете ову публикацију?';
    this.showDeleteWarningDialog = true;
  }

  configure(pub: any): void {
    this.router.navigate(['/import', pub.id]);
  }

  annotate(pub: any): void {
    // this.router.navigate(['/publikacija', pub.id, 'fragment', 1]);
    window.alert('Ručna anotacija teksta još nije u funkciji.');
  }

  clear(): void {
    this.filter = '';
    this.loadPubs();
  }

  setFilter(): void {
    this.loadPubs();
  }
}
