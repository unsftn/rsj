import { Component, HostListener, OnInit } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { Router } from '@angular/router';
import { UserService } from '../../../services/auth/user.service';
import { RenderService } from '../../../services/render';

@Component({
  selector: 'app-person',
  templateUrl: './person.component.html',
  styleUrls: ['./person.component.scss']
})
export class PersonComponent implements OnInit {

  obradjivaci: any[] = [];
  selected: any = {};
  odrednice: string[] = [];

  constructor(
    private userService: UserService,
    private router: Router,
    private renderService: RenderService,
    private domSanitizer: DomSanitizer) { }

  ngOnInit(): void {
    this.obradjivaci = this.userService.getObradjivaci();
    // console.log(this.obradjivaci);
  }

  showUser(user: any): void {
    this.selected = user;
    this.renderService.getRenderiZaObradjivaca(user.id).subscribe(
      (data) => {
        this.odrednice = data.map((item) => this.domSanitizer.bypassSecurityTrustHtml(item));
      },
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
