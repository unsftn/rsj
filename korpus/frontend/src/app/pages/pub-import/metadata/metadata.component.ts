import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import { PublikacijaService } from '../../../services/publikacije/publikacija.service';
import { Table } from 'primeng/table';
import { PubType } from '../../../models/reci';

@Component({
  selector: 'app-metadata',
  templateUrl: './metadata.component.html',
  styleUrls: ['./metadata.component.scss']
})
export class MetadataComponent implements OnInit {

  id: number;
  @ViewChild('authorTable', {static: false}) authorTable: Table;
  editMode: boolean;
  pub: any;
  pubTypes: PubType[];
  clonedAuthors: { [s: string]: any; } = {};

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private messageService: MessageService,
    private publikacijaService: PublikacijaService,
  ) {
    this.pub = {};
  }

  ngOnInit(): void {
    this.publikacijaService.importStep.emit(0);
    this.publikacijaService.fetchAllPubTypes().subscribe((data) => { this.pubTypes = data; });
    this.route.pathFromRoot[2].params.subscribe((params) => {
      if (params.pid === 'nova') {
        this.editMode = false;
        this.id = null;
        this.pub = {
          autori: [],
          naslov: '',
          naslov_izdanja: '',
          isbn: '',
          issn: '',
          godina: '',
          volumen: '',
          url: '',
          izdavac: '',
          prevodilac: '',
          prvo_izdanje: '',
          napomena: '',
          zanr: '',
          vrsta: this.publikacijaService.getFirstPubType(),
        };
      } else {
        this.editMode = true;
        this.id = +params.pid;
        this.publikacijaService.get(this.id).subscribe((value) => {
          this.pub = value;
          this.pub.autori = this.pub.autor_set.map((item, index) => ({ index, ime: item.ime, prezime: item.prezime}));
          this.pub.vrsta = this.publikacijaService.getPubType(this.pub.vrsta?.id);
          delete this.pub.autor_set;
        });
      }
    });
  }

  check(): boolean {
    let msg = '';
    if (this.pub.skracenica.trim().length === 0)
      msg += 'Скраћеница је обавезна.';
    if (this.pub.naslov.trim().length === 0)
      msg += ' Наслов је обавезан.';
    if (msg.length > 0) {
      this.messageService.add({ severity: 'error', summary: 'Грешка', detail: msg });
      return false;
    }
    return true;
  }

  getPubType(id: number): any {
    for (const pub of this.pubTypes)
      if (pub.id === id)
        return pub;
    return undefined;
  }

  save(): void {
    if (!this.check()) return;
    const pub = this.makePub();
    if (this.editMode) {
      this.publikacijaService.save(pub).subscribe({
        next: (value) => {
          this.publikacijaService.publicationChanged.emit(true);
          this.messageService.add({
            severity: 'success',
            summary: 'Метаподаци су сачувани',
            life: 3000,
            detail: ''
          });
        },
        error: (error) => {
          console.log(error);
        }});
    } else {
      this.publikacijaService.add(pub).subscribe({
        next: (value) => {
          this.id = value.id;
          this.messageService.add({
            severity: 'success',
            summary: 'Додата је нова публикација',
            life: 3000,
            detail: ''
          });
          this.router.navigate(['/import', this.id, 'metapodaci']);
        },
        error: (error) => {
          console.log(error);
        }});
    }
  }

  onRowEditInit(author: any): void {
    this.clonedAuthors[author.index] = {...author};
  }

  onRowEditSave(author: any): void {
    if (author.prezime.trim().length > 0) {
      delete this.clonedAuthors[author.index];
      this.messageService.add({ severity: 'success', summary: 'Успех', detail: 'Аутор је ажуриран' });
    } else {
      this.messageService.add({ severity: 'error', summary: 'Грешка', detail: 'Презиме је обавезно' });
    }
  }

  onDeleteRow(rowIndex: number): void {
    this.pub.autori.splice(rowIndex, 1);
  }

  onAddRow(): void {
    const newAuthor = {index: this.pub.autori.length, ime: '', prezime: ''};
    this.pub.autori.push(newAuthor);
    this.authorTable.initRowEdit(newAuthor);
  }

  onRowEditCancel(author: any, index: number): void {
    this.pub.autori[index] = this.clonedAuthors[author.index];
    delete this.clonedAuthors[author.index];
  }

  makePub(): any {
    this.pub.vrsta_id = this.pub.vrsta ? this.pub.vrsta.id : null;
    delete this.pub.vrsta;
    return this.pub;
  }

}
