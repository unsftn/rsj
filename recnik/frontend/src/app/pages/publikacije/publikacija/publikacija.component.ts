import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import { Table } from 'primeng/table';
import { PublikacijaService } from '../../../services/publikacije';

@Component({
  selector: 'app-publikacije',
  templateUrl: './publikacija.component.html',
  styleUrls: ['./publikacija.component.scss']
})
export class PublikacijaComponent implements OnInit {

  @Input() id: number;
  @ViewChild('authorTable', {static: false}) authorTable: Table;
  editMode: boolean;
  pub: any;
  pubTypes: any[];
  clonedAuthors: { [s: string]: any; } = {};

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private messageService: MessageService,
    private publikacijaService: PublikacijaService,
  ) {
    this.pub = {};
  }

  getPubType(id: number): any {
    for (const pub of this.pubTypes)
      if (pub.id === id)
        return pub;
    return undefined;
  }

  save(): void {
    const pub = this.makePub();
    this.publikacijaService.save(pub).subscribe((value) => {
      console.log(value);
    },(error) => {
      console.log(error);
    });
  }

  onRowEditInit(author: any): void {
    this.clonedAuthors[author.index] = {...author};
  }

  onRowEditSave(author: any): void {
    if (author.prezime.trim().length > 0) {
      delete this.clonedAuthors[author.index];
      this.messageService.add({severity:'success', summary: 'Успех', detail:'Аутор је ажуриран'});
      console.log(this.pub.autori);
    } else {
      this.messageService.add({severity:'error', summary: 'Грешка', detail:'Презиме је обавезно'});
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

  ngOnInit(): void {
    this.publikacijaService.getAllTypes().subscribe((value) => {
      this.pubTypes = value;
    });
    this.route.data.subscribe((data) => {
      switch (data.mode) {
        case 'add':
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
            vrsta_id: 1, // TODO
            user_id: 1,  // TODO
          };
          break;
        case 'edit':
          this.editMode = true;
          this.route.params.subscribe((params) => {
            this.id = +params.id;
            this.publikacijaService.get(this.id).subscribe((value) => {
              this.pub = value;
              this.pub.autori = this.pub.autor_set.map((item, index) => ({ index, ime: item.ime, prezime: item.prezime}));
            });
          });
          break;
      }
    });
  }

  makePub(): any {
    delete this.pub.autor_set;
    return this.pub;
  };

}
