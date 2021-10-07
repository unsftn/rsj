import { Component, OnInit } from '@angular/core';
import { SafeHtml } from '@angular/platform-browser';
import { ActivatedRoute, Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import { PublikacijaService } from '../../services/publikacije/publikacija.service';

@Component({
  selector: 'app-pub-text',
  templateUrl: './pub-text.component.html',
  styleUrls: ['./pub-text.component.scss']
})
export class PubTextComponent implements OnInit {

  pub: any;
  pubId: number;
  fragmentNr: number;
  title: SafeHtml;
  paragraphs: string[];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private messageService: MessageService,
    private publikacijaService: PublikacijaService,
  ) {
    this.pub = {};
    this.paragraphs = [];
  }

  ngOnInit(): void {
    this.route.params.subscribe((params) => {
      this.pubId = +params.pid;
      this.fragmentNr = +params.fid;
      this.publikacijaService.get(this.pubId).subscribe((value) => {
        this.pub = value;
        this.title = this.publikacijaService.getOpis(this.pub);
        this.pub.autori = this.pub.autor_set.map((item, index) => ({ index, ime: item.ime, prezime: item.prezime}));
        this.pub.vrsta = this.publikacijaService.getPubType(this.pub.vrsta?.id);
        delete this.pub.autor_set;
        this.publikacijaService.getFragment(this.pubId, this.fragmentNr).subscribe(
          (tekst) => {
            this.paragraphs = tekst.tekst.split('\n');
          },
          (error) => {
            console.log(error);
          });
      });
    });
  }

  next(): void {
    this.router.navigate(['/publikacija', this.pubId, 'fragment', this.fragmentNr + 1]);
  }

  prev(): void {
    if (this.fragmentNr > 1)
      this.router.navigate(['/publikacija', this.pubId, 'fragment', this.fragmentNr - 1]);
  }
}
