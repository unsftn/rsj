import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { PublikacijaService } from '../../../services/publikacije/publikacija.service';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Component({
  selector: 'app-preview',
  templateUrl: './preview.component.html',
  styleUrls: ['./preview.component.scss']
})
export class PreviewComponent implements OnInit {

  pubId: number;
  fragmentNr: number;
  paragraphs: SafeHtml[];

  constructor(
    private route: ActivatedRoute,
    private domSanitizer: DomSanitizer,
    private publikacijaService: PublikacijaService,
  ) { }

  ngOnInit(): void {
    this.route.pathFromRoot[2].params.subscribe((params) => {
      this.pubId = +params.pid;
      this.fragmentNr = 1;
      this.fetchPage();
    });
    this.publikacijaService.publicationChanged.subscribe((value) => {
      this.fetchPage();
    });
  }

  fetchPage(): void {
    this.publikacijaService.getFragment(this.pubId, this.fragmentNr).subscribe({
      next: (tekst) => {
        this.paragraphs = this.split(tekst.tekst);
      },
      error: (error) => {
        console.log(error);
      }});
  }

  split(text: string): SafeHtml[] {
    const retval: SafeHtml[] = [];
    const paras = text.split('\n');
    for (const para of paras) {
      const finalText = this.domSanitizer.bypassSecurityTrustHtml(para);
      retval.push(finalText);
    }
    return retval;
  }

  next(): void {
    this.fragmentNr++;
    this.fetchPage();
  }

  prev(): void {
    if (this.fragmentNr > 1) {
      this.fragmentNr--;
      this.fetchPage();
    }
  }
}
