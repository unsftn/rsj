import { Component, HostListener, OnInit } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { Router } from '@angular/router';
import { RenderService } from '../../../services/render';

@Component({
  selector: 'app-all',
  templateUrl: './all.component.html',
  styleUrls: ['./all.component.scss']
})
export class AllComponent implements OnInit {

  odrednice: string[] = [];

  constructor(
    private router: Router,
    private renderService: RenderService,
    private domSanitizer: DomSanitizer
  ) { }

  ngOnInit(): void {
    this.renderService.getRenderiSvi().subscribe(
      (data) => this.odrednice = data.map((item) => this.domSanitizer.bypassSecurityTrustHtml(item)),
      (error) => console.log(error)
    );
  }

  @HostListener('document:click', ['$event'])
  public handleClick(event: Event): void {
    let targetDiv = event.target;
    if (!(targetDiv instanceof HTMLDivElement))
      targetDiv = (targetDiv as HTMLElement).parentElement;
    if (targetDiv instanceof HTMLDivElement) {
      const element = targetDiv as HTMLDivElement;
      if (element.className === 'odrednica') {
        const odrednicaId = element?.getAttribute('data-id');
        if (odrednicaId) {
          const url = this.router.serializeUrl(this.router.createUrlTree([`/edit/${odrednicaId}`]));
          window.open(url, '_blank');
        }
      }
    }
  }
}
